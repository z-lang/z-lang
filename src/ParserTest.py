from unittest import TestCase
from Parser import Parser

def flatten(node):
    string = str(node)
    if len(node) > 0:
        subnodes = map(lambda x: flatten(x), node)
        string += "(%s)" % ' '.join(subnodes)
    return string

class ParserTest(TestCase):

    def testParseVariable(self):
        (definitions, errors) = Parser().parse("def x = y")

        # assert that no error occured
        self.assertEqual(errors, [])

        # assert correct parsing
        self.assertEqual(
            flatten(definitions[0]),
            "def(x y)")


    def testParseFunction(self):
        (definitions, errors) = Parser().parse("def f(x) = x")

        # assert that no error occured
        self.assertEqual(errors, [])

        # assert correct parsing
        self.assertEqual(
            flatten(definitions[0]),
            "def(f lambda((x) x))")


    def testParseTuple(self):
        (definitions, errors) = Parser().parse("def t = (a, b)")

        # assert that no error occured
        self.assertEqual(errors, [])

        # assert correct parsing
        self.assertEqual(
            flatten(definitions[0]),
            "def(t (a b))")

    def testParseList(self):
        (definitions, errors) = Parser().parse("def list = [a, b]")

        # assert that no error occured
        self.assertEqual(errors, [])

        # assert correct parsing
        self.assertEqual(
            flatten(definitions[0]),
            "def(list (a b))")

    def testParseLambda(self):
        (definitions, errors) = Parser().parse("def f(x) = lambda(y) x")

        # assert that no error occured
        self.assertEqual(errors, [])

        # assert correct parsing
        self.assertEqual(
            flatten(definitions[0]),
            "def(f lambda((x) lambda((y) x)))")


    def testParsePositiveInteger(self):
        (definitions, errors) = Parser().parse("def number = 42")

        # assert that no error occured
        self.assertEqual(errors, [])

        # assert correct parsing
        self.assertEqual(
            flatten(definitions[0]),
            "def(number 42)")


    def testParseNegativeInteger(self):
        (definitions, errors) = Parser().parse("def number = -103")

        # assert that no error occured
        self.assertEqual(errors, [])

        # assert correct parsing
        self.assertEqual(
            flatten(definitions[0]),
            "def(number -103)")


    def testParseTrue(self):
        (definitions, errors) = Parser().parse("def boolean = true")

        # assert that no error occured
        self.assertEqual(errors, [])

        # assert correct parsing
        self.assertEqual(
            flatten(definitions[0]),
            "def(boolean true)")


    def testParseFalse(self):
        (definitions, errors) = Parser().parse("def boolean = false")

        # assert that no error occured
        self.assertEqual(errors, [])

        # assert correct parsing
        self.assertEqual(
            flatten(definitions[0]),
            "def(boolean false)")


    def testParseString(self):
        (definitions, errors) = Parser().parse("def string = \"Hello, World!\"")

        # assert that no error occured
        self.assertEqual(errors, [])

        # assert correct parsing
        self.assertEqual(
            flatten(definitions[0]),
            "def(string \"Hello, World!\")")



