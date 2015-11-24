import jinja2
from Node import Node
from UniqueLetter import UniqueLetter
from re import match

class CodeGenerator:
    def generate(self, environment, templateString):
        # create a template environement and define settings
        env = jinja2.Environment(line_statement_prefix='#', line_comment_prefix='##')

        # create template from templateString
        template = env.from_string(templateString)

        # give ast as input an render template
        code = ""
        for (name, (type, node, local)) in environment.elements.items():
            unique = UniqueLetter()

            if node == None:
                continue
            code += template.render({ 
                "name" : name,
                "type" : type,
                "value" : self.escape(node[1], type),
                "unique" : lambda key: unique[key],
                "library" : False,
                "ord" : lambda s: ', '.join(map(lambda c: str(ord(c)), s[1:-1]))
            })
        return code

    def generateDefinition(self, environment, name, templateString):
        if not name in environment.elements:
            return
        (type, node, local) = environment.get(name) 

        # create a template environement and define settings
        env = jinja2.Environment(line_statement_prefix='#', line_comment_prefix='##')

        # create template from templateString
        template = env.from_string(templateString)

        # give ast as input an render template
        code = ""
        unique = UniqueLetter()

        if node == None:
            return

        code += template.render({ 
            "name" : "z_" + name,
            "type" : type,
            "value" : self.escape(node[1], type),
            "unique" : lambda key: unique[key],
            "library" : False,
            "ord" : lambda s: ', '.join(map(lambda c: str(ord(c)), s[1:-1]))
        })
        return code

    def escape(self, node, type):
        if node.isVariable():
            name = node.value()
            if node.tokenId() == 'STRING':
                name = '[%s]' % ', '.join(map(lambda c: str(ord(c)), s[1:-1]))
            if node.tokenId() != 'INT':
                name = "z_" + name
            return Node(node.syntax, Token(name, node.tokenId()), list(map(lambda n: self.escape(n, None), node)))
        else:
            return Node(node.syntax, Token(node.value(), node.tokenId()), list(map(lambda n: self.escape(n, None), node)))

'''
    def escape(self, node, type):
        if node.isVariable():
            name = node.value()
            #if type.isString():
            #    name = '[%s]' % ', '.join(map(lambda c: str(ord(c)), s[1:-1]))
            if not type.isInteger():
                name = "z_" + name

            return Node(node.syntax, Token(name, node.tokenId()), node.children)
        elif node.isTuple():
            return Node(node.syntax, Token(node.value(), node.tokenId()), list(map(lambda n, t: self.escape(n, t), zip(node.children, type.types))))
        elif node.isList():
            return Node(node.syntax, Token(node.value(), node.tokenId()), list(map(lambda n: self.escape(n, type.types[0]), node)))
        elif node.isLambda():
            print(str(node[0][0]) + " == " + str(type.types[0]))
            if len(type.types[0].types) > 1:
                arg = Node(node[0].syntax, Token(node[0].value(), node[0].tokenId()), list(map(lambda n, t: self.escape(n, t), zip(node[0], type[0].types))))
            else:
                arg = Node(node[0].syntax, Token(node[0].value(), node[0].tokenId()), list(map(lambda n: self.escape(n, type.types[0]), node[0])))
            res = Node(node[1].syntax, Token(node[1].value(), node[1].tokenId()), list(map(lambda n: self.escape(n, type.types[1]), node[1])))
            return Node(node.syntax, Token(node.value(), node.tokenId()), [arg, res])
        elif node.isApplication():
            return Node(node.syntax, Token(node.value(), node.tokenId()), list(map(lambda n, t: self.escape(n, t), zip(node, type.types))))
        elif node.isLet():
            return Node(node.syntax, Token(node.value(), node.tokenId()), list(map(lambda n, t: self.escape(n, t), zip(node, type.types))))
        else:
            return None
'''

class Token:
    def __init__(self, value, type):
        self.value = value
        self.type = type
