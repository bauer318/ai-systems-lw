def find_self(lst, key):
    for elem in lst:
        if key(elem):
            return elem
    return None
