import argparse
import collections
import functools
import logging
import math
import multiprocessing
import os
import re
import sys
from typing import List, Callable, DefaultDict

from tabulate import tabulate

from rozental_as_a_service.common_types import TypoInfo, BackendsConfig
from rozental_as_a_service.config import (
    DEFAULT_WORDS_CHUNK_SIZE, DEFAULT_VOCABULARY_FILENAME, DEFAULT_SQLITE_DB_FILENAME,
)
from rozental_as_a_service.list_utils import chunks, flat
from rozental_as_a_service.typos_backends import (
    process_with_vocabulary, process_with_ya_speller,
    process_with_db_with_cache,
)
from rozental_as_a_service.files_utils import get_all_filepathes_recursively
from rozental_as_a_service.strings_extractors import (
    extract_from_python_src, extract_from_markdown, extract_from_html,
    extract_from_js,
)

log = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
logging.getLogger('urllib3').setLevel(logging.INFO)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('path', type=str)
    parser.add_argument('--vocabulary_path', default=None)
    parser.add_argument('--exclude', default='')
    parser.add_argument('--db_path', default=None)
    parser.add_argument('--exit_zero', action='store_true')
    parser.add_argument('--processes', type=int, default=None)
    parser.add_argument('-v', action='count', default=0)

    return parser.parse_args()


def extract_all_constants_from_path(path: str, exclude: List[str], processes_amount: int) -> List[str]:
    extractors = [
        (extract_from_python_src, ['py']),
        (extract_from_markdown, ['md']),
        (extract_from_html, ['html']),
        (extract_from_js, ['js', 'ts', 'tsx']),
    ]

    extension_to_extractor_mapping: DefaultDict[str, List[Callable]] = collections.defaultdict(list)
    for extractor, extensions in extractors:
        for extension in extensions:
            extension_to_extractor_mapping[extension].append(extractor)

    string_constants: List[str] = []

    for extension, extension_extractors in extension_to_extractor_mapping.items():
        all_files = get_all_filepathes_recursively(path, exclude, extension)
        if not all_files:
            continue
        chunk_size = math.ceil(len(all_files) / processes_amount)
        new_strings = multiprocessing.Pool(processes_amount).map(
            functools.partial(extract_all_constants_from_files, extractors=extension_extractors),
            chunks(all_files, chunk_size),
        )
        string_constants += flat(new_strings)
    return list(set(string_constants))


def extract_all_constants_from_files(files_pathes: List[str], extractors: List[Callable]) -> List[str]:
    string_constants: List[str] = []
    for filepath in files_pathes:
        for extractor_callable in extractors:
            log.debug(f'Start reading {filepath}...')
            with open(filepath, 'r') as file_handler:
                raw_content = file_handler.read()
            log.debug(f'Start processing {filepath}...')
            string_constants += extractor_callable(raw_content)
    return extract_words(list(set(string_constants)))


def fetch_typos_info(string_constants: List[str], vocabulary_path: str = None, db_path: str = None) -> List[TypoInfo]:
    typos_info: List[TypoInfo] = []

    backends = [
        process_with_vocabulary,
        process_with_db_with_cache,
        process_with_ya_speller,
    ]
    backend_config: BackendsConfig = {
        'vocabulary_path': vocabulary_path,
        'db_path': db_path,
        'speller_chunk_size': DEFAULT_WORDS_CHUNK_SIZE,
    }
    for words_chunk in chunks(string_constants, backend_config['speller_chunk_size']):
        for words_processor in backends:
            sure_correct, sure_with_typo_info, unknown = words_processor(words_chunk, backend_config)
            typos_info += sure_with_typo_info
            # переопределяем переменную цикла так, чтобы следующему процессору доставались
            # только слова, по которым не известно, ок ли они
            words_chunk = unknown

    return typos_info


def extract_words(raw_constants: List[str], min_word_length: int = 3, only_russian: bool = True) -> List[str]:
    processed_words: List[str] = []
    for constant in raw_constants:
        processed_words += list({
            w.strip().lower() for w in re.findall(r'\w+', constant)
            if len(w.strip()) >= min_word_length
        })
    processed_words = list(set(processed_words))
    if only_russian:
        processed_words = [w for w in processed_words if re.match(r'[а-я-]+', w)]
    return processed_words


def main() -> None:
    arguments = parse_args()
    processes_amount = arguments.processes or multiprocessing.cpu_count()
    vocabulary_path = arguments.vocabulary_path or os.path.join(arguments.path, DEFAULT_VOCABULARY_FILENAME)
    db_path = arguments.db_path or os.path.join(arguments.path, DEFAULT_SQLITE_DB_FILENAME)
    exclude = arguments.exclude.split(',') if arguments.exclude else []
    log.setLevel(max(3 - arguments.v, 0) * 10)

    unique_words = extract_all_constants_from_path(arguments.path, exclude, processes_amount)
    typos_info = fetch_typos_info(unique_words, vocabulary_path, db_path)

    if typos_info:
        table = [(t['original'], ', '.join(t['possible_options'])) for t in typos_info]
        print(tabulate(table, headers=('Найденное слово', 'Возможные исправления')))  # noqa
        if not arguments.exit_zero:
            exit(1)


if __name__ == '__main__':
    main()
