class TagDictionary(dict):
    def __int__(self):
        self = dict()

    def add(self, key, value):
        self[key] = value
