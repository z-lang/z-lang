from unittest import TestCase
from Compiler import Compiler

class ComplerTest(TestCase):

    def testCompileVariable(self):
        (code, errors) = Compiler().compile("def x = y")

        # assert that no error occured
        self.assertEqual(errors, [])

        # assert correct parsing
        self.assertEqual(code.strip(), "x = y")


    def testCompileFunction(self):
        (code, errors) = Compiler().compile("def f(x) = x")

        # assert that no error occured
        self.assertEqual(errors, [])

        # assert correct parsing
        self.assertEqual(code.strip(), "f x = x")


    def testCompileTuple(self):
        (code, errors) = Compiler().compile("def t = (a, b)")

        # assert that no error occured
        self.assertEqual(errors, [])

        # assert correct parsing
        self.assertEqual(code.strip(), "t = (a, b)")


    def testCompileLambda(self):
        (code, errors) = Compiler().compile("def f(x) = lambda(y) x")

        # assert that no error occured
        self.assertEqual(errors, [])

        # assert correct parsing
        self.assertEqual(code.strip(), "f x = \y -> x")

