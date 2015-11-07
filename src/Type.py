
def alphabet(x):
    if x < 26:
        return chr(x + ord('a'))
    else:
        return chr((x % 26) + ord('a')) + alphabet(x-26)

class Type:
    def __init__(self, name, types):
        self.name = name
        self.types = types

    def str(self, mapping):
        if self.isVariable():
            if self in mapping:
                return mapping[self]
            else:
                var = alphabet(len(mapping))
                mapping[self] = var
                return var
        elif self.isTuple():
            subnodes = map(lambda x: x.str(mapping), self.types)
            return "(%s)" % ', '.join(subnodes)
        elif self.isList():
            subnodes = map(lambda x: x.str(mapping), self.types)
            return "[%s]" % ', '.join(subnodes)
        elif self.isInteger():
            return "Int"
        elif self.isBoolean():
            return "Bool"
        #elif self.isConcrete():
        #    if len(self.types) == 0:
        #        return "%s" % self.name
        #    else:
        #        subnodes = map(lambda x: x.str(mapping), self.types)
        #        return "(%s)" % ', '.join(subnodes)
        elif self.isFunction():
            return self.types[0].str(mapping) + " -> " + self.types[1].str(mapping)
        else:
            return "?"

    def __str__(self, mapping={}):
        return self.str({})

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

    #def isConcrete(self):
    #    return not ( self.isFunction() or self.isVariable() )

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
