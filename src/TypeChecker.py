from Environment import Environment
from Node import variableNode
from Type import Type, TypeVariable, ConcreteType, Function, Integer, Boolean, Tuple

class TypeError(Type):
    def __init__(self):
        super().__init__("error", [])

class TypeChecker:
    concreteTypes = {
        'INT'   : Integer,
        'BOOL'  : Boolean
    }

    def check(self, errors, env, node):
        if node.isVariable():
            return self.getType(errors, env, node)
        elif node.isApplication():
            fun_type = self.check(errors, env, variableNode(node.token, [])).copy()
            arg_type = Tuple(list(map(lambda child: self.check(errors, env, child), node)))
            result_type = TypeVariable()
            self.unify(Function(arg_type, result_type), fun_type)
            return result_type
        elif node.isLambda():
            args = list(map(lambda x: TypeVariable(), node[0]))
            arg_type = Tuple(args)
            new_env = env.copy()
            [new_env.add(n.value(), t, n) for n, t in zip(node[0], args)]
            result_type = self.check(errors, new_env, node[1])
            return Function(arg_type, result_type)
        elif node.isLet():
            new_type = TypeVariable()
            env.add(node[0].value(), new_type, node[1])
            def_type = self.check(errors, env, node[1])
            self.unify(new_type, def_type)
            return self.check(errors, env, node[1])
        else:
            print("type error: (" + str(node) + ")")
            return TypeError()


    def getType(self, errors, env, node):
        if len(node) == 0:
            if node.tokenId() in self.concreteTypes:
                return self.concreteTypes[node.tokenId()]
            elif env.get(node.value()) != None:
                (type, node) = env.get(node.value())
                return type
            else:
                errors += "error unknown: " + str(node) + " tokenid " + node.tokenId()
                return TypeError()
        else:
            return Tuple(list(map(lambda n: self.getType(errors, env, n), node)))


    def unify(self, type_a, type_b):
        errors = []

        if type_b.isVariable():
            type_b.name = type_a.name
            type_b.types = type_a.types
        elif type_a.isVariable():
            self.unify(type_b, type_a)
        else:
            if (type_a.name != type_b.name or len(type_a.types) != len(type_b.types)):
                return "type mismatch error"
            else:
                for subtype_a, subtype_b in zip(type_a.types, type_b.types):
                    errors += self.unify(subtype_a, subtype_b)
        return errors
