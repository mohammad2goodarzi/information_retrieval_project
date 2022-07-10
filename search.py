from indexing import process_documents
import os
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
    results = posting_lists[word]
    return results


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
    else:
        return search(query)


process_documents()
if __name__ == '__main__':
    print("مدیسون", process_query("مدیسون"))
    print("ستایش", process_query("ستایش"))
    print("جهان and بهداشت", process_query("جهان and بهداشت"))
