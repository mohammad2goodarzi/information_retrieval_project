import os
import re
from collections import defaultdict
import json
from typing import Dict, List


def get_processed_document_id() -> List[str]:
    """
    return the name of processed documents.
    """
    with open('processed_document.txt') as file:
        doc_ids = file.read()
        return doc_ids.strip().split('\n')


def get_unprocessed_doc_id() -> List[str]:
    """
    return the name of unprocessed documents.
    """
    dir_path = os.path.dirname(os.path.realpath(__file__))
    path = os.path.join(dir_path, 'txtfiles')
    files = os.listdir(path)
    processed_doc_id = get_processed_document_id()
    unprocessed_doc_id = []
    for file in files:
        if file.endswith('.txt'):
            if file[:-4] not in processed_doc_id:
                unprocessed_doc_id.append(file[:-4])
    return unprocessed_doc_id


def convert_to_str_line(doc_id: int) -> str:
    """convert an integer to a string and append a newline character to the end"""
    return str(doc_id) + '\n'


def process_documents():
    """
    process unprocessed documents.
    add the names to processed documents file.
    save new posting lists in the file.
    """
    unprocessed_doc_id = get_unprocessed_doc_id()
    posting_list = get_dictionary(unprocessed_doc_id)
    with open('processed_document.txt', 'a') as file:
        file.writelines(map(convert_to_str_line, unprocessed_doc_id))
    store_postings(posting_list)


def eliminate(data: str, eliminator: list) -> str:
    """Find all the elements in the eliminator list and replace them with an empty string"""
    return re.sub('|'.join(eliminator), '', data)


def get_dictionary(unprocessed_doc_id: List[str]) -> Dict[str, list]:
    """
    :param unprocessed_doc_id: list of unprocessed documents id
    :return: dictionary of tokens.
    """
    with open('project_files/elim.txt') as eliminator_file:
        eliminator = eliminator_file.read().strip().split()
        posting_list = defaultdict(list)
        for doc_id in unprocessed_doc_id:
            file = open(f'txtfiles/{doc_id}.txt', encoding="utf-8")
            data = file.read().strip()
            data = eliminate(data, eliminator)
            posting_list = tokenize_document(data, int(doc_id), posting_list)

    return posting_list


def tokenize_document(data: str, doc_id: int, posting_list: Dict[str, list]) -> Dict[str, list]:
    """
    :param data: content of a document.
    :param doc_id: ID of a document
    :param posting_list: the whole dictionary of tokens.
    :return: updated dictionary.
    """
    prefix_file = open('project_files/normal_prefix.txt', encoding='utf-8')
    prefix = prefix_file.read().strip().split()
    prefix_file.close()
    suffix_file = open('project_files/normal_suffix.txt', encoding='utf-8')
    suffix = suffix_file.read().strip().split()
    suffix_file.close()
    stop_words_file = open('project_files/stop.txt', encoding='utf-8')
    stop_words = stop_words_file.read().strip().split()
    stop_words_file.close()

    def normalize_prefix_suffix(word: str):
        for pre in prefix:
            if word.startswith(pre):
                word = word.lstrip(pre)
                break
        for suf in suffix:
            if word.endswith(suf):
                word = word.rstrip(suf)
                break
        return word

    def is_not_stop_word(word):
        return word not in stop_words

    tf=0
    tokens = set(filter(is_not_stop_word, map(normalize_prefix_suffix, data.split())))
    for token in tokens:
        posting_list[token].append(doc_id)
        for data in data.split():
            if token == data:
                tf=tf+1
        computeTf(doc_id, token, tf)

    return posting_list


def store_postings(posting_list: Dict[str, list]):
    """Save new posting list"""
    with open("store.json", "r+", encoding="utf-8") as outfile:
        old_posting_list = json.load(outfile)
        update_posting_list(old_posting_list, posting_list)
        outfile.seek(0)  # to clear old data
        json.dump(posting_list, outfile, ensure_ascii=False)


def update_posting_list(old_posting_list: Dict[str, list], posting_list: Dict[str, list]):
    """
    Update the shared key values in the given dictionaries
    Add the non-shared key values to the old posting list
    """
    common_keys = set(old_posting_list.keys()).intersection(set(posting_list.keys()))
    for key in common_keys:
        posting_list[key].extend(old_posting_list[key])
    posting_list.update(old_posting_list)

def computeTf(doc_id,token,count):
    doc{doc_id} = defaultdict
    doc_id.update(token,count)
    return doc_id