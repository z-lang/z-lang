import ply.lex as lex

# The Scanner class defines how to parse the tokens
class Scanner:
    # Language literals
    literals = [ '(', ')', '[', ']', ',', '=', '+', '-', '*', '/' ]

    # Language tokens
    tokens = [ 
        'DEF', 
        'LAMBDA', 
        'AND', 
        'OR', 
        'XOR', 
        'NEWLINE',
        #'EQ', 
        #'COMMA', 
        #'LP', 
        #'RP', 
        #'LB', 
        #'RB', 
        #'ADD', 
        #'SUB', 
        #'MUL', 
        #'DIV', 
        'ID', 
        'INT', 
        'BOOL', 
        'STRING', 
        'COMMENT' 
    ]

    # Simple rules
    t_ignore = ' \t'
    t_ID     = '[A-Za-z][A-Za-z0-9]*'
    t_INT    = '-?[0-9]+'
   # t_EQ     = '='
   # t_COMMA  = ','          # comma (tuple)
    #t_LP     = '\('         # left paranthesis (tuple)
    #t_RP     = '\)'         # right parenthesis (tuple)
    #t_LB     = '\['         # left bracket (list)
    #t_RB     = '\]'         # right bracket (list)
    #t_ADD    = '\+'         # integer addition
    #t_SUB    = '-'          # integer subtract
    #t_MUL    = '\*'         # integer multiplication
    #t_DIV    = '/'          # integer division
    t_STRING = '"[^"]*"'    # string

    # Keyword for definitons
    def t_DEF(self, t):
        'def'
        return t

    # Keyword for lambda expressions
    def t_LAMBDA(self, t):
        'lambda'
        return t

    # Keyword for logical and
    def t_AND(self, t):
        'and'
        return t

    # Keyword for logical or
    def t_OR(self, t):
        'or'
        return t

    # Keyword for logical xor
    def t_XOR(self, t):
        'xor'
        return t


    # Ignore comments
    def t_COMMENT(self, t):
        '//.+'

    # Keywords for boolean
    def t_BOOL(self, t):
        '(true|false)'
        return t

    # Count newlines in code
    def t_NEWLINE(self, t):
        '[\n]'
        self.lex.lineno += 1

    # On error
    def t_error(self, t):
        self.onError(t)


class Lexer(Scanner):
    def __init__(self):
        self.lex = lex.lex(object=self)
        self.errors = []


    # Sets the input file to parse
    def input(self, input):
        self.input = input
        self.lex.input(input)

    # Gets next token from input stream
    def token(self):
        try:
            token = self.lex.token()
            if token != None:
                newline_pos = self.input.rfind('\n', 0, token.lexpos)
                if newline_pos > 0:
                    token.lexpos = (token.lexpos - newline_pos) + 1

                return TokenAdapter(token)
            return None
        except:
            return None

    # Gets all token as list
    def allTokens(self):
        tokens = []
        token = self.token()
        while token != None:
            tokens.append(token)
            token = self.token()
        return (tokens, self.errors)

    # On error
    def onError(self, token):
        self.errors.append("Unknown token " + repr(token.value[0]))


class TokenAdapter:
    def __init__(self, token):
        self.type = token.type
        self.value = token

    def __str__(self):
        return str(self.value)


