from unittest import TestCase
from src.Parser import Parser

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
            "def(f(x) x)")


    def testParseTuple(self):
        (definitions, errors) = Parser().parse("def t = (a, b)")

        # assert that no error occured
        self.assertEqual(errors, [])

        # assert correct parsing
        self.assertEqual(
            flatten(definitions[0]),
            "def(t (a b))")


    def testParseLambda(self):
        (definitions, errors) = Parser().parse("def f(x) = lambda(y) x")

        # assert that no error occured
        self.assertEqual(errors, [])

        # assert correct parsing
        self.assertEqual(
            flatten(definitions[0]),
            "def(f(x) lambda((y) x))")

