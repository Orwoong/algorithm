import string

def check_duplicates(text):
    hash = {}

    for i in range(len(text)):
        hash.update({text[i]: i})

    return len(hash.keys())

assert check_duplicates(string.ascii_lowercase) == 26
assert check_duplicates('abcabcbb') == 3
assert check_duplicates('bbbb') == 1