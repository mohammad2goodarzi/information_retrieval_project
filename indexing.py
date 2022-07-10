import os
import re
from collections import defaultdict
import json


def get_processed_document_id():
    """
    return the name of processed documents.
    """
    with open('processed_document.txt') as file:
        doc_ids = file.read()
        return doc_ids.strip().split('\n')


def get_unprocessed_doc_id():
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


def convert_to_str_line(doc_id: int):
    return str(doc_id) + '\n'


def process_documents():
    """
    process unprocessed documents.
    add the names to processed documents file.
    save new posting lists in the file.
    """
    unprocessed_doc_id = get_unprocessed_doc_id()
    postingList = get_dictionary(unprocessed_doc_id)
    with open('processed_document.txt', 'a') as file:
        file.writelines(map(convert_to_str_line, unprocessed_doc_id))
    # ToDo: save posting list
    storePostings(postingList)
    print(postingList)
    return postingList


def eliminate(data: str, eliminator: list):
    return re.sub('|'.join(eliminator), '', data)


def get_dictionary(unprocessed_doc_id):
    """
    :param unprocessed_doc_id: list of unprocessed documents id
    :return: dictionary of tokens.
    """
    with open('project_files/elim.txt') as eliminator_file:
        eliminator = eliminator_file.read().strip().split()
        postingList = defaultdict(list)
        for doc_id in unprocessed_doc_id:
            file = open(f'txtfiles/{doc_id}.txt', encoding="utf-8")
            data = file.read().strip()
            data = eliminate(data, eliminator)
            postingList = tokenize_document(data, int(doc_id), postingList)

    return postingList


def tokenize_document(data: str, doc_id: int, postingList: defaultdict):
    """
    :param data: content of a document.
    :param doc_id: ID of a document
    :param postingList: the whole dictionary of tokens.
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

    tokens = set(filter(is_not_stop_word, map(normalize_prefix_suffix, data.split())))
    for token in tokens:
        postingList[token].append(doc_id)
    return postingList


def storePostings(postingList:defaultdict):
    with open("store.json", "w", encoding="utf-8") as outfile:
        json.dump(postingList, outfile, ensure_ascii=False)

