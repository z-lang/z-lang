from Environment import Environment
from Node import VariableNode
from Type import TypeVariable, Function, Integer, Boolean, Tuple, List

class TypeError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg

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
            fun_type = self.check(errors, env, node[0])
            arg_type = Tuple(list(map(lambda child: self.check(errors, env, child), node[1])))
            result_type = TypeVariable()
            self.unify(errors, Function(arg_type, result_type), fun_type)
            return result_type
        elif node.isLambda():
            args = list(map(lambda x: TypeVariable(), node[0]))
            arg_type = Tuple(args)
            new_env = env.copy()
            for n, t in zip(node[0], args):
                new_env.add(n.value(), t, n, True)
            result_type = self.check(errors, new_env, node[1])
            return Function(arg_type, result_type)
        elif node.isLet():
            new_type = TypeVariable()
            env.add(node[0].value(), new_type, node[1], False)
            def_type = self.check(errors, env, node[1])
            self.unify(errors, new_type, def_type)
            return self.check(errors, env, node[1])
        else:
            raise "type error: (" + str(node) + ")"


    def getType(self, errors, env, node):
        if env.get(node.value()) != None:
            (type, n, local) = env.get(node.value())
            if local:
                return type
            else:
                return type.copy()
        elif node.tokenId() in self.concreteTypes:
            return self.concreteTypes[node.tokenId()]
        else:
            raise TypeError("error " + str(node.token.lineno) + ": unknown variable or function: '" + str(node) + "'"
)

    def unify(self, errors, type_a, type_b):
        if type_b.isVariable():
            type_b.instance.seq = type_a.instance.seq
            type_b.instance.name = type_a.instance.name
            type_b.instance.types = type_a.instance.types
            type_b.instance = type_a.instance
            type_b = type_a
            return type_a
        elif type_a.isVariable():
            return self.unify(errors, type_b, type_a)
        else:
            if (type_a.getName() != type_b.getName() or len(type_a.getTypes()) != len(type_b.getTypes())):
                raise TypeError("error:" + "type mismatch '" + str(type_a) + "' != '" + str(type_b) + "'")
            else:
                for subtype_a, subtype_b in zip(type_a.getTypes(), type_b.getTypes()):
                    self.unify(errors, subtype_a, subtype_b)
                return type_a
        raise "type mismatch error2"
