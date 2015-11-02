import ply.yacc as yacc
from Lexer import Lexer
from SyntaxTreeFactory import SyntaxTreeFactory

class Grammer:
    def __init__(self, factory, lexer):
        self.factory = factory
        self.lexer = lexer
        self.tokens = lexer.tokens
        self.errors = lexer.errors

    def p_lines(self, p):
        '''lines : lines definition
                 | definition'''
        if len(p) > 2:
            p[0] = p[1]
            p[0].append(p[2])
        else:
            p[0] = [ p[1] ]
            
    def p_definition(self, p):
        '''definition : DEF ID parameters EQ value
                    | DEF ID EQ value'''
        if len(p) == 6:
            p[0] = self.factory.createFunctionDefinition(p[1], p[2], p[3], p[5])
        else:
            p[0] = self.factory.createVariableDefinition(p[1], p[2], p[4])

    def p_parameters(self, p):
        '''parameters : LP parameter RP'''
        p[0] = p[2]

    def p_parameter(self, p):
        '''parameter : parameter COMMA ID
                 | ID'''
        if len(p) > 3:
            p[0] = p[1]
            p[0].append(p[3])
        else:
            p[0] = [ p[1] ]

    def p_value(self, p):
        '''value : LAMBDA parameters value
               | tuple
               | ID arguments
               | ID
               | INT
               | BOOL'''
        if len(p) == 4:
            p[0] = self.factory.createLambda(p[1], p[2], p[3])
        elif len(p) == 3:
            p[0] = self.factory.createCall(p[1], p[2])
        elif type(p[1]) is list:
            p[0] = self.factory.createTuple(p[1])
        elif p[1].type == 'INT':
            p[0] = self.factory.createInteger(p[1])
        elif p[1].type == 'BOOL':
            p[0] = self.factory.createBoolean(p[1])
        elif p[1].type == 'ID':
            p[0] = self.factory.createVariable(p[1])

    def p_arguments(self, p):
        '''arguments : arguments tuple
                     | tuple'''
        if len(p) > 2:
            p[0] = p[1] + p[2]
        else:
            p[0] = p[1]

    def p_tuple(self, p):
        '''tuple : LP argument RP'''
        p[0] = p[2]

    def p_argument(self, p):
        '''argument : argument COMMA value
                    | value'''
        if len(p) > 3:
            p[0] = p[1]
            p[0].append(p[3])
        else:
            p[0] = [ p[1] ]

    def p_error(self, p):
        self.errors.append("Unexpected token " + repr(str(p.value.value)))

class Parser:
    def parse(self, input):
        lexer = Lexer()
        grammer = Grammer(SyntaxTreeFactory(), lexer)
        parser = yacc.yacc(module=grammer)

        return ( parser.parse(input, lexer=lexer), lexer.errors )
