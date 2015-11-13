from UniqueLetter import UniqueLetter

seq = 0

class TypeNature:
    VARIABLE = 0
    CONCRETE = 1
    COMPLEX  = 2

class Type:
    def __init__(self, nature, name, types):
        global seq
        self.instance = None
        self.seq = seq
        self.nature = nature
        self.name = name
        self.types = types
        seq += 1

    def __str__(self):
        unique = UniqueLetter()

        def typestr(type):
            type = type.prune()

            if type.isVariable():
                return unique[type.seq]
            elif type.isConcrete():
                return type.name
            elif type.isTuple():
                return "(%s)" % ', '.join(map(lambda x: typestr(x), type.getTypes()))
            elif type.isList():
                return "[%s]" % typestr(type.getTypes()[0])
            elif type.isFunction():
                return typestr(type.getTypes()[0]) + " -> " + typestr(type.getTypes()[1])
            else:
                return "?"
        return typestr(self)

    def copy(self):
        mapping = {}

        def typecopy(type):
            type = type.prune()

            if type.isInteger():
                return type
            elif type.isBoolean():
                return type
            if type.getSeq() in mapping:
                return mapping[type.getSeq()]
            else:
                copy = Type(type.nature, type.getName(), [])
                mapping[type.getSeq()] = copy
                copy.types = list(map(typecopy, type.getTypes()))
                return copy
        return typecopy(self)

    def prune(self):
        if self.instance != None:
            return self.instance.prune()
        return self

    def set(self, type):
        if not self.isVariable():
            raise "type set not variable"
        self.instance = type

    def getName(self):
        return self.name

    def getTypes(self):
        return self.types

    def getSeq(self):
        return self.seq

    def isVariable(self):
        return self.nature == TypeNature.VARIABLE

    def isConcrete(self):
        return self.nature == TypeNature.CONCRETE

    def isComplex(self):
        return self.nature == TypeNature.COMPLEX

    def isTuple(self):
        return self.name == "tuple"

    def isList(self):
        return self.name == "list"

    def isFunction(self):
        return self.name == "function"

    def isInteger(self):
        return self.name == "Int"

    def isBoolean(self):
        return self.getName() == "Bool"


def TypeVariable():
    return Type(TypeNature.VARIABLE, "var", [])
   
def Function(arg_type, ret_type):
    return Type(TypeNature.COMPLEX, "function", [arg_type, ret_type])


Integer = Type(TypeNature.CONCRETE, "Int", [])
Boolean = Type(TypeNature.CONCRETE, "Bool", [])

def Tuple(types):
    if len(types) == 1:
        return types[0]
    return Type(TypeNature.COMPLEX, "tuple", types)

def List(type):
    return Type(TypeNature.COMPLEX, "list", [type])
