from Node import Node

def nodes(tokens):
    return list( map( lambda x: Node(x, []), tokens ) )

class SyntaxTreeFactory:
    def createDefinition(self, def_token, dec_node):
        return Node(def_token, dec_node)

    def createDeclaration(self, id_token, params):
        return Node(id_token,  nodes(params))

    def createLambda(self, lambda_token, params, val):
        return Node(lambda_token, [ Node(None, nodes(params)), val ])

    def createTuple(self, args):
        return Node(None, args)

    def createCall(self, var_token, args):
        return Node(var_token, args)

    def createVariable(self, var_token):
        return Node(var_token, [])
