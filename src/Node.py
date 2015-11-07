class Syntax:
    Variable    = 0
    Tuple       = 1
    List        = 2
    Application = 3
    Lambda      = 4
    Let         = 5

class Node:
    def __init__(self, syntax, token, children):
        self.syntax = syntax
        self.token = token
        self.children = children

    def __getitem__(self, key):
        return self.children.__getitem__(key)

    def __len__(self):
        return len(self.children)

    def __iter__(self):
        return self.children.__iter__()

    def __str__(self):
        if self.token:
            return self.value()
        return ""

    def value(self):
        if self.token:
            return self.token.value
        return None

    def tokenId(self):
        if self.token:
            return self.token.type
        return None

    def isVariable(self):
        return self.syntax == Syntax.Variable

    def isTuple(self):
        return self.syntax == Syntax.Tuple

    def isList(self):
        return self.syntax == Syntax.List

    def isApplication(self):
        return self.syntax == Syntax.Application

    def isLambda(self):
        return self.syntax == Syntax.Lambda
   
    def isLet(self):
        return self.syntax == Syntax.Let



def VariableNode(token, children):
    return Node(Syntax.Variable, token, children)

def TupleNode(children):
    return Node(Syntax.Tuple, None, children)

def ListNode(children):
    return Node(Syntax.List, None, children)


def ApplicationNode(token, children):
    return Node(Syntax.Application, token, children)


def LambdaNode(token, children):
    return Node(Syntax.Lambda, token, children)

def LetNode(token, children):
    return Node(Syntax.Let, token, children)

