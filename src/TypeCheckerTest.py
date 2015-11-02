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
        self.assertEqual(str(type), "[int]")


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
        self.assertEqual(str(type), "([int], [int])")


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
        self.assertEqual(str(type), "[int]")


    def testNegativeIntegerTest(self):
        (definitions, errors) = Parser().parse("def number = -103")
        type = TypeChecker().check(errors, Environment(), definitions[0])

        # assert that no error occured
        self.assertEqual(errors, [])

        # assert correct parsing
        self.assertEqual(str(type), "[int]")


    def testTrueType(self):
        (definitions, errors) = Parser().parse("def boolean = true")
        type = TypeChecker().check(errors, Environment(), definitions[0])

        # assert that no error occured
        self.assertEqual(errors, [])

        # assert correct parsing
        self.assertEqual(str(type), "[bool]")


    def testFalseTest(self):
        (definitions, errors) = Parser().parse("def boolean = false")
        type = TypeChecker().check(errors, Environment(), definitions[0])

        # assert that no error occured
        self.assertEqual(errors, [])

        # assert correct parsing
        self.assertEqual(str(type), "[bool]")


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
        self.assertEqual(str(value_type), "[int]")


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
        self.assertEqual(str(value_type), "[bool]")


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
        self.assertEqual(str(id_type), "(a, b) -> [int]")

        # assert correct parsing
        self.assertEqual(str(value_type), "[int]")

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


