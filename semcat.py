import os


class SemCat:
    """
    Wraps vocab and converter dictionaries
    """
    def __init__(self, path: str):
        self._vocab = {}
        self.read(path)

    @property
    def vocab(self) -> dict:
        """
        Returns a dictionary where keys are the categories and the values are the lists of the words related to them
        Returns
        -------
        dict:
            key -> [List]
        """
        return self._vocab

    def __delitem__(self, key):
        del self._vocab[key]

    def __getitem__(self, key):
        return self._vocab[key]

    def __setitem__(self, key, value):
        self._vocab[key] = value

    def read(self, path):
        for file in os.listdir(path):
            if file.endswith(".txt"):
                category_name = file.rstrip('.txt').split('-')[0]
                with open(os.path.join(path, file), mode='r', encoding='utf8') as f:
                    words = f.read().splitlines()
                    self._vocab[category_name] = words
