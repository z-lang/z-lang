from jinja2 import Environment, Template

class CodeGenerator:
    def generate(self, definitions, templateString):
        # create a template environement and define settings
        env = Environment(line_statement_prefix='#', line_comment_prefix='##')

        # create template from templateString
        template = env.from_string(templateString)

        # give ast as input an render template
        return template.render({ "definitions" : definitions })

