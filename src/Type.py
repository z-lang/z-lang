from UniqueLetter import UniqueLetter

seq = 0

class Type:
    def __init__(self, name, types):
        global seq
        self.seq = seq
        self.name = name
        self.types = types
        seq += 1

    def __str__(self):
        unique = UniqueLetter()

        def typestr(type):
            if type.isVariable():
                return unique[type]
            elif type.isTuple():
                subnodes = map(lambda x: typestr(x), type.types)
                return "(%s)" % ', '.join(subnodes)
            elif type.isList():
                return "[%s]" % type.types[0]
            elif type.isInteger():
                return "Int"
            elif type.isBoolean():
                return "Bool"
            elif type.isFunction():
                return typestr(type.types[0]) + " -> " + typestr(type.types[1])
            else:
                return "?"

        return typestr(self)

    def copy(self):
        mapping = {}

        def typecopy(type):
            if self.isInteger():
                return self
            elif self.isBoolean():
                return self
            if type in mapping:
                copy = mapping[type]
            else:
                copy = Type(type.name, [])
                mapping[type] = copy
                for subtype in type.types:
                    copy.types.append(typecopy(subtype))
            return copy

        return typecopy(self)

    def __hash__(self):
        #return hash((self.seq, str(self.name), self.types.__hash__()))
        return self.seq.__hash__()

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()

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
