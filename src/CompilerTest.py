from unittest import TestCase
from Compiler import Compiler

class ComplerTest(TestCase):

    def testCompileVariable(self):
        (code, errors) = Compiler().compile("def x = y")

        # assert that no error occured
        self.assertEqual(errors, [])

        # assert correct parsing
        self.assertEqual(code.strip(), "z_x = z_y")


    def testCompileFunction(self):
        (code, errors) = Compiler().compile("def f(x) = x")

        # assert that no error occured
        self.assertEqual(errors, [])

        # assert correct parsing
        self.assertEqual(code.strip(), "z_f (z_x) = z_x")


    def testCompileTuple(self):
        (code, errors) = Compiler().compile("def t = (a, lambda(x) x, 9)")

        # assert that no error occured
        self.assertEqual(errors, [])

        # assert correct parsing
        self.assertEqual(code.strip(), "z_t = (z_a, \\(z_x) -> z_x, 9)")


    def testCompileList(self):
        (code, errors) = Compiler().compile("def t = [a, b, c]")

        # assert that no error occured
        self.assertEqual(errors, [])

        # assert correct parsing
        self.assertEqual(code.strip(), "z_t = [z_a, z_b, z_c]")



    def testCompileLambda(self):
        (code, errors) = Compiler().compile("def f(x) = lambda(y) x")

        # assert that no error occured
        self.assertEqual(errors, [])

        # assert correct parsing
        self.assertEqual(code.strip(), "z_f (z_x) = \\(z_y) -> z_x")


