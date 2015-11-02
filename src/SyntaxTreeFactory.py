from Node import Node, variableNode, applicationNode, lambdaNode, letNode
from ply.lex import LexToken

def nodes(tokens):
    return list( map( lambda x: variableNode(x, []), tokens ) )

class SyntaxTreeFactory:
    def createFunctionDefinition(self, def_token, var_token, params, val_node):
       lamToken = LexToken()
       lamToken.value = 'lambda'
       return letNode(def_token, [ 
            variableNode(var_token, []),
            lambdaNode(lamToken, [ variableNode(None, nodes(params)), val_node ]), 
            ])

    def createVariableDefinition(self, def_token, var_token, val_node):
       return letNode(def_token, [ 
            variableNode(var_token, []), 
            val_node 
            ])

    def createLambda(self, lambda_token, params, val):
        if len(params) > 0:
            return lambdaNode(lambda_token, [ variableNode(None, nodes(params)), val ])
        else:
            return variableNode(lambda_token, [ val ])

    def createTuple(self, args):
        return variableNode(None, args)

    def createCall(self, var_token, args):
        return applicationNode(var_token, args)

    def createVariable(self, var_token):
        return variableNode(var_token, [])

    def createInteger(self, var_token):
        return variableNode(var_token, [])

    def createBoolean(self, var_token):
        return variableNode(var_token, [])

