import jinja2
from UniqueLetter import UniqueLetter

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
                "value" : node[1],
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
            "name" : name,
            "type" : type,
            "value" : node[1],
            "unique" : lambda key: unique[key],
            "library" : False,
            "ord" : lambda s: ', '.join(map(lambda c: str(ord(c)), s[1:-1]))
        })
        return code


    def generateLibrary(self, templateString):
        # create a template environement and define settings
        env = jinja2.Environment(line_statement_prefix='#', line_comment_prefix='##')

        # create template from templateString
        template = env.from_string(templateString)

        # give ast as input an render template
        return template.render({ 
            "definitions" : [],
            "library" : True
        })

