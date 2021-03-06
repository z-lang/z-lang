from Environment import Environment
from Node import VariableNode
from Type import Type, TypeVariable, Function, Integer, Boolean, Tuple, List
from functools import reduce

class TypeError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg

class TypeChecker:
    def check(self, errors, env, node):
        if node.isVariable():
            if node.value() in env:
                return env.getType(node.value())
            else:
                raise TypeError("Undefined symbol '%s'" % node.value())

        elif node.isTuple():
            return Tuple(list(map(lambda n: self.check(errors, env, n), node)))

        elif node.isList():
            types = map(lambda x: self.check(errors, env, x), node)
            unified = reduce(lambda a, b: self.unify(errors, a, b), types, TypeVariable())
            return List(unified)

        elif node.isApplication():
            fun_type = self.check(errors, env, node[0])
            arg_type = self.check(errors, env, node[1])
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
            try:
                new_type = TypeVariable()
                env.add(node[0].value(), new_type, node, True)
                def_type = self.check(errors, env, node[1])
                result_type = self.unify(errors, new_type, def_type).copy()
                env.add(node[0].value(), result_type, node, False)
                return result_type
            except TypeError as e:
                raise TypeError("In definition of '%s': %s" % (node[0].value(), e.msg))
        else:
            raise TypeError("Unknown syntax construct '%s'" % str(node))

    def unify(self, errors, type_a, type_b):
        type_a = type_a.prune()
        type_b = type_b.prune()

        if type_a.seq == type_b.seq:
            return type_a
        elif type_b.isVariable():
            type_b.set(type_a)
            return type_a
        elif type_a.isVariable():
            return self.unify(errors, type_b, type_a)
        else:
            if (type_a.getName() != type_b.getName() or len(type_a.getTypes()) != len(type_b.getTypes())):
                raise TypeError("Type mismatch: cannot unify '%s' and '%s'" % (str(type_a), str(type_b)))
            else:
                for subtype_a, subtype_b in zip(type_a.getTypes(), type_b.getTypes()):
                    self.unify(errors, subtype_a, subtype_b)
                return type_a
