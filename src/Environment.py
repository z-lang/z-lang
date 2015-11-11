from Type import TypeVariable, Function, Tuple, List, Integer, Boolean

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

        ifelse_var = TypeVariable()
        self.elements["ifelse"] = (Function(Tuple([Boolean, ifelse_var, ifelse_var]), ifelse_var), None, False)

        get_var = TypeVariable()
        self.elements["get"] = (Function(Tuple([List(get_var), Integer]), get_var), None, False)

        join_var = TypeVariable()
        self.elements["join"] = (Function(Tuple([List(join_var), List(join_var)]), List(join_var)), None, False)

        tail_var = TypeVariable()
        self.elements["tail"] = (Function(List(tail_var), List(join_var)), None, False)

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
