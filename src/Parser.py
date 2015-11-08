import ply.yacc as yacc
from Lexer import Lexer
from SyntaxTreeFactory import SyntaxTreeFactory

class Grammer:
    def __init__(self, factory, lexer):
        self.factory = factory
        self.lexer = lexer
        self.literals = lexer.literals
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
        '''definition : DEF ID parameters '=' lambda
                      | DEF ID '=' lambda'''
        if len(p) == 6:
            p[0] = self.factory.createFunctionDefinition(p[1], p[2], p[3], p[5])
        else:
            p[0] = self.factory.createVariableDefinition(p[1], p[2], p[4])

    def p_parameters(self, p):
        '''parameters : '(' parameter ')' '''
        p[0] = p[2]

    def p_parameter(self, p):
        '''parameter : parameter ',' ID
                 | ID'''
        if len(p) > 3:
            p[0] = p[1]
            p[0].append(p[3])
        else:
            p[0] = [ p[1] ]

    def p_lambda(self, p):
        '''lambda : LAMBDA parameters lambda
                  | logical_or'''
        if len(p) == 4:
            p[0] = self.factory.createLambda(p[1], p[2], p[3])
        else:
            p[0] = p[1]

    def p_logical_or(self, p):
        '''logical_or : logical_or OR logical_and
                      | logical_and'''
        if len(p) == 4:
            p[0] = self.factory.createCall(p[2], [ p[1], p[3] ])
        else:
            p[0] = p[1]

    def p_logical_and(self, p):
        '''logical_and : logical_and AND logical_not
                       | logical_not'''
        if len(p) == 4:
            p[0] = self.factory.createCall(p[2], [ p[1], p[3] ])
        else:
            p[0] = p[1]

    def p_logical_not(self, p):
        '''logical_not : NOT logical_not
                       | equality'''
        if len(p) == 3:
            p[0] = self.factory.createCall(p[1], [ p[2] ])
        else:
            p[0] = p[1]

    def p_equality(self, p):
        '''equality : equality EQ cmp
                    | equality NE cmp
                    | cmp'''
        if len(p) > 2:
            p[0] = self.factory.createCall(p[2], [ p[1], p[3] ])
        else:
            p[0] = p[1]

    def p_cmp(self, p):
        '''cmp  : expr LE  expr
                | expr GE  expr
                | expr '<' expr
                | expr '>' expr
                | expr'''
        if len(p) > 2:
            p[0] = self.factory.createCall(p[2], [ p[1], p[3] ])
        else:
            p[0] = p[1]

    def p_expr(self, p):
        '''expr : expr '+' term
                | expr '-' term
                | term'''
        if len(p) > 2:
            p[0] = self.factory.createCall(p[2], [ p[1], p[3] ])
        else:
            p[0] = p[1]

    def p_term(self, p):
        '''term : term '*' factor
                | term '/' factor
                | factor'''
        if len(p) > 2:
            p[0] = self.factory.createCall(p[2], [ p[1], p[3] ])
        else:
            p[0] = p[1]

    def p_factor(self, p):
        '''factor : tuple
                 | list
                 | string
                 | call
                 | variable
                 | integer
                 | boolean'''
        p[0] = p[1]

    def p_arguments(self, p):
        '''arguments : arguments tuple
                     | tuple'''
        if len(p) > 2:
            p[0] = self.factory.createTuple(p[1].children + p[2].children)
        else:
            p[0] = p[1]

    def p_call(self, p):
        '''call : ID arguments'''
        p[0] = self.factory.createCall(p[1], p[2])

    def p_tuple(self, p):
        '''tuple : '(' argument ')' '''
        p[0] = self.factory.createTuple(p[2])

    def p_list(self, p):
        '''list : '[' argument ']' '''
 
        p[0] = self.factory.createList(p[2])

    def p_string(self, p):
        '''string : STRING'''
        p[0] = self.factory.createString(p[1])

    def p_variable(self, p):
        '''variable : ID'''
        p[0] = self.factory.createVariable(p[1])

    def p_integer(self, p):
        '''integer : INT'''
        p[0] = self.factory.createInteger(p[1])

    def p_boolean(self, p):
        '''boolean : BOOL'''
        p[0] = self.factory.createBoolean(p[1])

    def p_argument(self, p):
        '''argument : argument ',' lambda
                    | lambda'''
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
