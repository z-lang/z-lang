
class Node:
    def __init__(self, token, children):
        self.token = token
        self.children = children

    def __getitem__(self, key):
        return self.children.__getitem__(key)

    def __len__(self):
        return len(self.children)

    def __iter__(self):
        return self.children.__iter__()

    def __str__(self):
        if self.token:
            return self.value()
        return ""

    def value(self):
        if self.token:
            return self.token.value
        return None

    def type(self):
        if self.token:
            return self.token.type
        return None
