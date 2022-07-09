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
    # posting_lists = process_documents()
    posting_lists = {}
    word = normalize_prefix_suffix(word)
    if word not in posting_lists:
        return 'no result found.'
    results = posting_lists[word]
    return results


def process_query(query):
    """
    Take a query and return the list of document IDs containing that word.
    """
    return search(query)


if __name__ == '__main__':
    print("جهان", process_query("چهان"))
    print("بهداشت", process_query("بهداشت"))
