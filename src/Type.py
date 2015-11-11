from UniqueLetter import UniqueLetter

seq = 0

class TypeInstance:
    def __init__(self, name, types):
        global seq
        self.seq = seq
        self.name = name
        self.types = types
        seq += 1

    #def __hash__(self):
    #    #return hash((self.seq, str(self.name), self.types.__hash__()))
    #    return self.seq.__hash__()

    #def __eq__(self, other):
    #    return self.__hash__() == other.__hash__()

class Type:
    def __init__(self, name, types):
        self.instance = TypeInstance(name, types)

    def __str__(self):
        unique = UniqueLetter()

        def typestr(type):
            if type.isVariable():
                return unique[type.instance.seq]
            elif type.isTuple():
                subnodes = map(lambda x: typestr(x), type.getTypes())
                return "(%s)" % ', '.join(subnodes)
            elif type.isList():
                return "[%s]" % typestr(type.getTypes()[0])
            elif type.isInteger():
                return "Int"
            elif type.isBoolean():
                return "Bool"
            elif type.isFunction():
                return typestr(type.getTypes()[0]) + " -> " + typestr(type.getTypes()[1])
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
            if type.instance.seq in mapping:
                copy = mapping[type.instance.seq]
            else:
                copy = Type(type.getName(), [])
                mapping[type.instance.seq] = copy
                for subtype in type.getTypes():
                    copy.getTypes().append(typecopy(subtype))
            return copy

        return typecopy(self)



    def getName(self):
        return self.instance.name

    def getTypes(self):
        return self.instance.types

    def getSeq(self):
        return self.instance.seq

    def isVariable(self):
        return self.getName() == None

    def isTuple(self):
        return self.getName() == "tuple"

    def isList(self):
        return self.getName() == "list"

    def isFunction(self):
        return self.getName() == "function"

    def isInteger(self):
        return self.getName() == "Int"

    def isBoolean(self):
        return self.getName() == "Bool"

    
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
