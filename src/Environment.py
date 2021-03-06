from Type import TypeVariable, Function, Tuple, List, Integer, Boolean
from re import match

class Environment:
    def __init__(self):
        self.elements = {
            # boolean functions
            "true"      : (Boolean, None, False),
            "false"     : (Boolean, None, False),
            "and"       : (Function(Tuple([Boolean, Boolean]), Boolean), None, False),
            "or"        : (Function(Tuple([Boolean, Boolean]), Boolean), None, False),
            "not"       : (Function(Tuple([Boolean]), Boolean), None, False),

            # integer functions
            "add"       : (Function(Tuple([Integer, Integer]), Integer), None, False),
            "sub"       : (Function(Tuple([Integer, Integer]), Integer), None, False),
            "mul"       : (Function(Tuple([Integer, Integer]), Integer), None, False),
            "div"       : (Function(Tuple([Integer, Integer]), Integer), None, False),
            "mod"       : (Function(Tuple([Integer, Integer]), Integer), None, False),

            # comparision functions
            "eq"        : (Function(Tuple([Integer, Integer]), Boolean), None, False),
            "ne"        : (Function(Tuple([Integer, Integer]), Boolean), None, False),
            "le"        : (Function(Tuple([Integer, Integer]), Boolean), None, False),
            "ge"        : (Function(Tuple([Integer, Integer]), Boolean), None, False),
            "lt"        : (Function(Tuple([Integer, Integer]), Boolean), None, False),
            "gt"        : (Function(Tuple([Integer, Integer]), Boolean), None, False),

            # list functions
            "len"        : (Function(List(TypeVariable()), Integer), None, False),
        }

        case_var = TypeVariable()
        self.elements["case"] = (Function(Tuple([Boolean, case_var, case_var]), case_var), None, False)

        get_var = TypeVariable()
        self.elements["get"] = (Function(Tuple([List(get_var), Integer]), get_var), None, False)

        join_var = TypeVariable()
        self.elements["join"] = (Function(Tuple([List(join_var), List(join_var)]), List(join_var)), None, False)

        tail_var = TypeVariable()
        self.elements["tail"] = (Function(List(tail_var), List(tail_var)), None, False)

    def get(self, name):
        if name in self.elements:
            return self.elements[name]
        return None

    def add(self, name, type, node, local):
        self.elements[name] = (type, node, local)

    def copy(self):
        copy = Environment()
        copy.elements = self.elements.copy()
        return copy

    def getType(self, name):
        if self.isInteger(name):
            return Integer
        elif self.isBoolean(name):
            return Boolean
        elif self.isString(name):
            return List(Integer)
        elif name in self.elements:
            (type, node, local) = self.elements.get(name)
            if local:
                return type.prune()
            else:
                return type.copy().prune()
        else:
            return None

    def __contains__(self, name):
        return self.isInteger(name) or \
               self.isBoolean(name) or \
               self.isString(name)  or \
               self.elements.__contains__(name)

    def isInteger(self, name):
        return match('^-?[0-9]+$', name) != None

    def isBoolean(self, name):
        return match('^(true|false)$', name) != None

    def isString(self, name):
        return match('^"[^"]+"$', name) != None

