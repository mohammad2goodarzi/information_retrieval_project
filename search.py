from collections import defaultdict
from math import log10
from typing import Dict

from indexing import process_documents, get_processed_document_id
import json


NOT_FOUND = 'no result found.'


def normalize_prefix_suffix(word: str):
    """
    Take a word and remove its prefix and suffix.
    """
    prefix_file = open('project_files/normal_prefix.txt', encoding='utf-8')
    prefix = prefix_file.read().strip().split()
    prefix_file.close()
    suffix_file = open('project_files/normal_suffix.txt', encoding='utf-8')
    suffix = suffix_file.read().strip().split()
    suffix_file.close()

    for pre in prefix:
        if word.startswith(pre):
            word = word.lstrip(pre)
            break
    for suf in suffix:
        if word.endswith(suf):
            word = word.rstrip(suf)
            break
    return word


def search(word):
    """
    Take a word and return the list of document IDs containing that word.
    """
    with open("store.json", "r", encoding='utf-8') as read_file:
        posting_lists = json.load(read_file)
    word = normalize_prefix_suffix(word)
    if word not in posting_lists:
        return NOT_FOUND
    this_word_posting_list = posting_lists[word]

    def get_document_id():
        document_id = []
        for i in this_word_posting_list:
            document_id.append(i[0])
        return document_id

    results = get_document_id()
    return results


def calculate_tf_idf(query):

    def normalize_vector(vector: Dict[str, float]) -> Dict[str, float]:
        total = sum(map(lambda x: x ** 2, vector.values())) ** 0.5
        norm = {k: vector[k] / total for k in vector}
        return norm

    with open("store.json", "r", encoding='utf-8') as read_file:
        posting_lists = json.load(read_file)
    document_number = len(get_processed_document_id())

    query_weight = {}
    query_terms = query.split()
    for term in set(query_terms):
        normalized_term = normalize_prefix_suffix(term)
        df = len(posting_lists[normalized_term])
        idf = log10(document_number/df)
        tf = query_terms.count(term)
        if tf == 0:
            weight_tf = 0
        else:
            weight_tf = 1 + log10(tf)
        weight = weight_tf * idf
        query_weight[normalized_term] = weight

    document_weight = defaultdict(dict)
    for term in set(query_terms):
        normalized_term = normalize_prefix_suffix(term)
        this_term_posting_list = posting_lists[normalized_term]
        for document_id, tf in this_term_posting_list:
            if tf == 0:
                weight_tf = 0
            else:
                weight_tf = 1 + log10(tf)
            document_weight[document_id].update({term: weight_tf})

    normalized_query_weight = normalize_vector(query_weight)
    score = {}
    for document_id in document_weight:
        normalized_document_weight = normalize_vector(document_weight[document_id])
        tf_idf = {k: normalized_query_weight[k] * normalized_document_weight.get(k, 0) for k in normalized_query_weight}
        score[document_id] = sum(tf_idf.values())
    score = dict(sorted(score.items(), key=lambda item: item[1], reverse=True))
    return list(score.keys())[:10]


def process_query(query):
    """
    Take a query and return a list of document IDs containing that word.
    A query can contain one word or two words along with the keyword "and" or "or".
    """
    if 'and' in query:
        word1, word2 = query.split('and')
        word1 = word1.strip()
        word2 = word2.strip()
        result1 = search(word1)
        result2 = search(word2)
        final_result = list(set(result1).intersection(set(result2)))
        if result1 == NOT_FOUND or result2 == NOT_FOUND or not final_result:
            return NOT_FOUND
        else:
            return final_result
    if 'or' in query:
        word1, word2 = query.split('or')
        word1 = word1.strip()
        word2 = word2.strip()
        result1 = search(word1)
        result2 = search(word2)
        final_result = list(set(result1).union(set(result2)))
        if (not final_result) or (result1 == NOT_FOUND and result2 == NOT_FOUND):
            return NOT_FOUND
        else:
            return final_result
    if ' ' not in query:
        return search(query)
    else:
        return calculate_tf_idf(query)


process_documents()
if __name__ == '__main__':
    # print("اعتراض", process_query("اعتراض"))
    # print("ستایش", process_query("ستایش"))
    print("جهان ستایش بهداشت", process_query("جهان ستایش بهداشت"))
    print("اعتراض زهرا محسن", process_query("اعتراض زهرا محسن"))
    print("ناصرالدین زهرا محسن", process_query("ناصرالدین زهرا محسن"))


