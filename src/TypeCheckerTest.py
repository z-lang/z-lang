from Environment import Environment

from unittest import TestCase
from Parser import Parser
from TypeChecker import TypeChecker

class TypeCheckerTest(TestCase):

    def testVariableType(self):
        (definitions, errors) = Parser().parse("def x = 10")
        type = TypeChecker().check(errors, Environment(), definitions[0])

        # assert that no error occured
        self.assertEqual(errors, [])

        # assert correct parsing
        self.assertEqual(str(type), "Int")


    def testFunctionType(self):
        (definitions, errors) = Parser().parse("def f(x) = x")
        type = TypeChecker().check(errors, Environment(), definitions[0])

        # assert that no error occured
        self.assertEqual(errors, [])

        # assert correct parsing
        self.assertEqual(str(type), "a -> a")


    def testTupleType(self):
        (definitions, errors) = Parser().parse("def t = (1, 5)")
        type = TypeChecker().check(errors, Environment(), definitions[0])

        # assert that no error occured
        self.assertEqual(errors, [])

        # assert correct parsing
        self.assertEqual(str(type), "(Int, Int)")


    def testListType(self):
        (definitions, errors) = Parser().parse("def t = [1, 5, 6]")
        type = TypeChecker().check(errors, Environment(), definitions[0])

        # assert that no error occured
        self.assertEqual(errors, [])

        # assert correct parsing
        self.assertEqual(str(type), "[Int]")


    def testLambdaType(self):
        (definitions, errors) = Parser().parse("def f(x) = lambda(y) x")
        type = TypeChecker().check(errors, Environment(), definitions[0])

        # assert that no error occured
        self.assertEqual(errors, [])

        # assert correct parsing
        self.assertEqual(str(type), "a -> b -> a")


    def testPositiveIntegerTest(self):
        (definitions, errors) = Parser().parse("def number = 42")
        type = TypeChecker().check(errors, Environment(), definitions[0])

        # assert that no error occured
        self.assertEqual(errors, [])

        # assert correct parsing
        self.assertEqual(str(type), "Int")


    def testNegativeIntegerTest(self):
        (definitions, errors) = Parser().parse("def number = -103")
        type = TypeChecker().check(errors, Environment(), definitions[0])

        # assert that no error occured
        self.assertEqual(errors, [])

        # assert correct parsing
        self.assertEqual(str(type), "Int")


    def testTrueType(self):
        (definitions, errors) = Parser().parse("def boolean = true")
        type = TypeChecker().check(errors, Environment(), definitions[0])

        # assert that no error occured
        self.assertEqual(errors, [])

        # assert correct parsing
        self.assertEqual(str(type), "Bool")


    def testFalseTest(self):
        (definitions, errors) = Parser().parse("def boolean = false")
        type = TypeChecker().check(errors, Environment(), definitions[0])

        # assert that no error occured
        self.assertEqual(errors, [])

        # assert correct parsing
        self.assertEqual(str(type), "Bool")


    def testFunctionApplication(self):
        (definitions, errors) = Parser().parse("""
            def id(x) = x
            def value = id(11)
        """)
        env = Environment()
        id_type = TypeChecker().check(errors, env, definitions[0])
        value_type = TypeChecker().check(errors, env, definitions[1])

        # assert that no error occured
        self.assertEqual(errors, [])

        # assert correct parsing
        self.assertEqual(str(id_type), "a -> a")

        # assert correct parsing
        self.assertEqual(str(value_type), "Int")


    def testFunctionApplicationWithTwoArguments(self):
        (definitions, errors) = Parser().parse("""
            def id(x,y) = y
            def value = id(11, true)
        """)
        env = Environment()
        id_type = TypeChecker().check(errors, env, definitions[0])
        value_type = TypeChecker().check(errors, env, definitions[1])

        # assert that no error occured
        self.assertEqual(errors, [])

        # assert correct parsing
        self.assertEqual(str(id_type), "(a, b) -> b")

        # assert correct parsing
        self.assertEqual(str(value_type), "Bool")


    def testFunctionApplicationWithConstantExpression(self):
        (definitions, errors) = Parser().parse("""
            def id(x,y) = 20
            def value = id(false, true)
        """)
        env = Environment()
        id_type = TypeChecker().check(errors, env, definitions[0])
        value_type = TypeChecker().check(errors, env, definitions[1])

        # assert that no error occured
        self.assertEqual(errors, [])

        # assert correct parsing
        self.assertEqual(str(id_type), "(a, b) -> Int")

        # assert correct parsing
        self.assertEqual(str(value_type), "Int")

    def testPartialFunctionApplication(self):
        (definitions, errors) = Parser().parse("""
            def sum(a) = lambda(b) a + b
            def inc = sum(1)
        """)
        env = Environment()
        sum_type = TypeChecker().check(errors, env, definitions[0])
        inc_type = TypeChecker().check(errors, env, definitions[1])

        # assert that no error occured
        self.assertEqual(errors, [])

        # assert correct parsing
        self.assertEqual(str(sum_type), "Int -> Int -> Int")

        # assert correct parsing
        self.assertEqual(str(inc_type), "Int -> Int")

    def testMultipleFunctionApplication(self):
        (definitions, errors) = Parser().parse("""
            def prod = lambda(x) lambda(y) lambda(z) z * y * x
            def value = prod(8)(5)(3)
        """)
        env = Environment()
        prod_type = TypeChecker().check(errors, env, definitions[0])
        value_type = TypeChecker().check(errors, env, definitions[1])

        # assert that no error occured
        self.assertEqual(errors, [])

        # assert correct parsing
        self.assertEqual(str(prod_type), "Int -> Int -> Int -> Int")

        # assert correct parsing
        self.assertEqual(str(value_type), "Int")

    def testFunctionComposition(self):
        (definitions, errors) = Parser().parse("""
            def composition(f, g) = lambda(x) f( g(x) )
            def app = composition(lambda(x) x + 3, lambda(x) x - 4)(10)
        """)
        env = Environment()
        composition_type = TypeChecker().check(errors, env, definitions[0])
        app_type = TypeChecker().check(errors, env, definitions[1])

        # assert that no error occured
        self.assertEqual(errors, [])

        # assert correct parsing
        self.assertEqual(str(composition_type), "(a -> b, c -> a) -> c -> b")

        # assert correct parsing
        self.assertEqual(str(app_type), "Int")

    def testFirstElementFunction(self):
        (definitions, errors) = Parser().parse("""
            def first(x) = get(x, 0)
            def value = first([5, 6, 6])
        """)
        env = Environment()
        first_type = TypeChecker().check(errors, env, definitions[0])
        value_type = TypeChecker().check(errors, env, definitions[1])

        # assert that no error occured
        self.assertEqual(errors, [])

        # assert correct parsing
        self.assertEqual(str(first_type), "[a] -> a")

        # assert correct parsing
        self.assertEqual(str(value_type), "Int")

    def testRecursiveFunction(self):
        (definitions, errors) = Parser().parse("""
            def rec(x) = rec(x)
            def value = rec(5)
        """)
        env = Environment()
        id_type = TypeChecker().check(errors, env, definitions[0])
        value_type = TypeChecker().check(errors, env, definitions[1])

        # assert that no error occured
        self.assertEqual(errors, [])

        # assert correct parsing
        self.assertEqual(str(id_type), "a -> b")

        # assert correct parsing
        self.assertEqual(str(value_type), "a")

