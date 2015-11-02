from unittest import main, TestCase
from Lexer import Lexer

def types(tokens):
    return ' '.join(map(lambda x: x.type, tokens))


class LexerTest(TestCase):

    def testScanVariable(self):
        lexer = Lexer()
        lexer.input("def x = y")
        (tokens, errors) = lexer.allTokens()

        # assert that no error occured
        self.assertEqual(errors, [])

        # assert correct token scanning
        self.assertEqual(types(tokens), 'DEF ID = ID')


    def testScanFunction(self):
        lexer = Lexer()
        lexer.input("def f(x) = x")
        (tokens, errors) = lexer.allTokens()

        # assert that no error occured
        self.assertEqual(errors, [])

        # assert correct token scanning
        self.assertEqual(types(tokens), 'DEF ID ( ID ) = ID')


    def testScanTuple(self):
        lexer = Lexer()
        lexer.input("def t = (a, b)")
        (tokens, errors) = lexer.allTokens()

        # assert that no error occured
        self.assertEqual(errors, [])

        # assert correct token scanning
        self.assertEqual(types(tokens), 'DEF ID = ( ID , ID )')

    def testScanList(self):
        lexer = Lexer()
        lexer.input("def t = [a, b]")
        (tokens, errors) = lexer.allTokens()

        # assert that no error occured
        self.assertEqual(errors, [])

        # assert correct token scanning
        self.assertEqual(types(tokens), 'DEF ID = [ ID , ID ]')


    def testScanLambda(self):
        lexer = Lexer()
        lexer.input("def f(x) = lambda(y) x")
        (tokens, errors) = lexer.allTokens()

        # assert that no error occured
        self.assertEqual(errors, [])

        # assert correct token scanning
        self.assertEqual(types(tokens), 'DEF ID ( ID ) = LAMBDA ( ID ) ID')


    def testScanPositiveInteger(self):
        lexer = Lexer()
        lexer.input("def number = 42")
        (tokens, errors) = lexer.allTokens()

        # assert that no error occured
        self.assertEqual(errors, [])

        # assert correct token scanning
        self.assertEqual(types(tokens), 'DEF ID = INT')


    def testScanNegativeInteger(self):
        lexer = Lexer()
        lexer.input("def number = -102")
        (tokens, errors) = lexer.allTokens()

        # assert that no error occured
        self.assertEqual(errors, [])

        # assert correct token scanning
        self.assertEqual(types(tokens), 'DEF ID = INT')


    def testScanBooleanTrue(self):
        lexer = Lexer()
        lexer.input("def boolean = true")
        (tokens, errors) = lexer.allTokens()

        # assert that no error occured
        self.assertEqual(errors, [])

        # assert correct token scanning
        self.assertEqual(types(tokens), 'DEF ID = BOOL')


    def testScanBooleanFalse(self):
        lexer = Lexer()
        lexer.input("def boolean = false")
        (tokens, errors) = lexer.allTokens()

        # assert that no error occured
        self.assertEqual(errors, [])

        # assert correct token scanning
        self.assertEqual(types(tokens), 'DEF ID = BOOL')

    def testScanString(self):
        lexer = Lexer()
        lexer.input("def string = \"hello, world!\"")
        (tokens, errors) = lexer.allTokens()

        # assert that no error occured
        self.assertEqual(errors, [])

        # assert correct token scanning
        self.assertEqual(types(tokens), 'DEF ID = STRING')


