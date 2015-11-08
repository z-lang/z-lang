from Node import VariableNode, TupleNode, ListNode, ApplicationNode, LambdaNode, LetNode
from ply.lex import LexToken

def nodes(tokens):
    return list( map( lambda x: VariableNode(x, []), tokens ) )

class SyntaxTreeFactory:
    functionMapping = {
        '+'  : 'add',
        '-'  : 'sub',
        '*'  : 'mul',
        '/'  : 'div',
        '==' : 'eq',
        '!=' : 'ne',
        '<=' : 'le',
        '>=' : 'ge',
        '<'  : 'lt',
        '>'  : 'gt',
    }

    def createFunctionDefinition(self, def_token, var_token, params, val_node):
       lamToken = LexToken()
       lamToken.value = 'lambda'
       return LetNode(def_token, [ 
            VariableNode(var_token, []),
            LambdaNode(lamToken, [ VariableNode(None, nodes(params)), val_node ]), 
            ])

    def createVariableDefinition(self, def_token, var_token, val_node):
       return LetNode(def_token, [ 
            VariableNode(var_token, []), 
            val_node 
            ])

    def createLambda(self, lambda_token, params, val):
        if len(params) > 0:
            return LambdaNode(lambda_token, [ VariableNode(None, nodes(params)), val ])
        else:
            return VariableNode(lambda_token, [ val ])

    def createTuple(self, args):
        return TupleNode(args)

    def createList(self, args):
        return ListNode(args)

    def createCall(self, var_token, args):
        e1 = self.createVariable(var_token)
        return self.createApplication(e1, TupleNode(args))

    def createApplication(self, e1, e2):
        return ApplicationNode(None, [e1, e2])

    def createVariable(self, var_token):
        if var_token.value in self.functionMapping:
            var_token.value = self.functionMapping[var_token.value]
    
        return VariableNode(var_token, [])

    def createInteger(self, var_token):
        return VariableNode(var_token, [])

    def createBoolean(self, var_token):
        return VariableNode(var_token, [])

    def createString(self, var_token):
        return VariableNode(var_token, [])

