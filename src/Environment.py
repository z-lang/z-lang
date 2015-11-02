class Environment:
    def __init__(self):
        self.elements = {}

    def get(self, name):
        if name in self.elements:
            return self.elements[name]
        return None

    def add(self, name, type, node):
        self.elements[name] = (type, node)

    def copy(self):
        copy = Environment()
        copy.elements = self.elements.copy()
        return copy
