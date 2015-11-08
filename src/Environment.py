from Type import TypeVariable, Function, Tuple, List, Integer, Boolean

class Environment:
    def __init__(self):
        self.elements = {
            "true"      : (Boolean, None),
            "false"     : (Boolean, None),
            "and"       : (Function(Tuple([Boolean, Boolean]), Boolean), None),
            "or"        : (Function(Tuple([Boolean, Boolean]), Boolean), None),
            "not"       : (Function(Tuple([Boolean]), Boolean), None),
            "ifelse"    : (Function(Tuple([Boolean, TypeVariable(), TypeVariable(),]), TypeVariable()), None),
            "add"       : (Function(Tuple([Integer, Integer]), Integer), None),
            "sub"       : (Function(Tuple([Integer, Integer]), Integer), None),
            "mul"       : (Function(Tuple([Integer, Integer]), Integer), None),
            "div"       : (Function(Tuple([Integer, Integer]), Integer), None),
            "eq"        : (Function(Tuple([Integer, Integer]), Boolean), None),
            "ne"        : (Function(Tuple([Integer, Integer]), Boolean), None),
            "le"        : (Function(Tuple([Integer, Integer]), Boolean), None),
            "ge"        : (Function(Tuple([Integer, Integer]), Boolean), None),
            "lt"        : (Function(Tuple([Integer, Integer]), Boolean), None),
            "gt"        : (Function(Tuple([Integer, Integer]), Boolean), None),
        }

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
