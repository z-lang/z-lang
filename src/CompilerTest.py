from unittest import TestCase
from Compiler import Compiler

class ComplerTest(TestCase):

    def testCompileVariable(self):
        (code, errors) = Compiler().compile("def x = 12")

        # assert that no error occured
        self.assertEqual(errors, [])

        # assert correct parsing
        self.assertEqual(code.strip(), "z_x = 12")


    def testCompileFunction(self):
        (code, errors) = Compiler().compile("def f(x) = x")

        # assert that no error occured
        self.assertEqual(errors, [])

        # assert correct parsing
        self.assertEqual(code.strip(), "z_f (z_x) = z_x")


    def testCompileTuple(self):
        (code, errors) = Compiler().compile("def t = (true, lambda(x) x, 9)")

        # assert that no error occured
        self.assertEqual(errors, [])

        # assert correct parsing
        self.assertEqual(code.strip(), "z_t = (z_true, \\(z_x) -> z_x, 9)")


    def testCompileList(self):
        (code, errors) = Compiler().compile("def t = [1, 2, 3]")

        # assert that no error occured
        self.assertEqual(errors, [])

        # assert correct parsing
        self.assertEqual(code.strip(), "z_t = [1, 2, 3]")



    def testCompileLambda(self):
        (code, errors) = Compiler().compile("def f(x) = lambda(y) x")

        # assert that no error occured
        self.assertEqual(errors, [])

        # assert correct parsing
        self.assertEqual(code.strip(), "z_f (z_x) = \\(z_y) -> z_x")


