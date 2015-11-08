from Environment import Environment
from Node import VariableNode
from Type import Type, TypeVariable, ConcreteType, Function, Integer, Boolean, Tuple, List
from functools import reduce

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
        elif node.isTuple():
            return Tuple(list(map(lambda n: self.check(errors, env, n), node)))
        elif node.isList():
            type_a = TypeVariable()
            for child in node:
                type_b = self.check(errors, env, child)
                self.unify(errors, type_a, type_b)
                type_a = type_b
            return List(type_a)
        elif node.isApplication():
            fun_type = self.check(errors, env, VariableNode(node.token, [])).copy()
            arg_type = Tuple(list(map(lambda child: self.check(errors, env, child), node)))
            result_type = TypeVariable()
            self.unify(errors, Function(arg_type, result_type), fun_type)
            return result_type
        elif node.isLambda():
            args = list(map(lambda x: TypeVariable(), node[0]))
            arg_type = Tuple(args)
            new_env = env.copy()
            for n, t in zip(node[0], args):
                new_env.add(n.value(), t, n)
            result_type = self.check(errors, new_env, node[1])
            return Function(arg_type, result_type)
        elif node.isLet():
            new_type = TypeVariable()
            env.add(node[0].value(), new_type, node[1])
            def_type = self.check(errors, env, node[1])
            self.unify(errors, new_type, def_type)
            return self.check(errors, env, node[1])
        else:
            errors.append("type error: (" + str(node) + ")")
            return TypeError()


    def getType(self, errors, env, node):
        if node.tokenId() in self.concreteTypes:
            return self.concreteTypes[node.tokenId()]
        elif env.get(node.value()) != None:
            (type, n) = env.get(node.value())
            return type
        else:
            errors.append("error " + str(node.token.lineno) + ": unknown variable or function: '" + str(node) + "'")
            return TypeError()


    def unify(self, errors, type_a, type_b):
        if type_b.isVariable():
            type_b.name = type_a.name
            type_b.types = type_a.types
            return type_a
        elif type_a.isVariable():
            return self.unify(errors, type_b, type_a)
        else:
            if (type_a.name != type_b.name or len(type_a.types) != len(type_b.types)):
                errors.append("error:" + "type mismatch '" + str(type_a) + "' != '" + str(type_b) + "'")
                return TypeError()
            else:
                for subtype_a, subtype_b in zip(type_a.types, type_b.types):
                    self.unify(errors, subtype_a, subtype_b)
                return type_a
        errors.append("type mismatch error2")
        return TypeError()
