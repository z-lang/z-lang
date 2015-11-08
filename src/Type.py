from UniqueLetter import UniqueLetter

class Type:
    def __init__(self, name, types):
        self.name = name
        self.types = types

    def str(self, unique):
        if self.isVariable():
            return unique[self]
        elif self.isTuple():
            subnodes = map(lambda x: x.str(unique), self.types)
            return "(%s)" % ', '.join(subnodes)
        elif self.isList():
            subnodes = map(lambda x: x.str(unique), self.types)
            return "[%s]" % ', '.join(subnodes)
        elif self.isInteger():
            return "Int"
        elif self.isBoolean():
            return "Bool"
        elif self.isFunction():
            return self.types[0].str(unique) + " -> " + self.types[1].str(unique)
        else:
            return "?"

    def __str__(self, mapping={}):
        return self.str(UniqueLetter())

    def copy(self, mapping={}):
        copy = Type(self.name, [])
        if self in mapping:
            copy = mapping[self]
        else:
            mapping[self] = copy
            if self.types != None:
                if isinstance(self.types, Type):
                    raise "error"
                for type in self.types:
                    copy.types.append(type.copy(mapping))
        return copy

    def isVariable(self):
        return self.name == None

    def isTuple(self):
        return self.name == "tuple"

    def isList(self):
        return self.name == "list"

    def isFunction(self):
        return self.name == "function"

    def isInteger(self):
        return self.name == "Int"

    def isBoolean(self):
        return self.name == "Bool"

    
class TypeVariable(Type):
    def __init__(self):
        super().__init__(None, [])


class ConcreteType(Type):
    def __init__(self, name, types):
        super().__init__(name, types)


class Function(Type):
    def __init__(self, arg_type, ret_type):
        super().__init__("function", [arg_type, ret_type]) 


Integer = ConcreteType("Int", [])
Boolean = ConcreteType("Bool", [])

def Tuple(types):
        if len(types) == 1:
            return types[0]
        return ConcreteType("tuple", types)

def List(type):
        return ConcreteType("list", [type])
