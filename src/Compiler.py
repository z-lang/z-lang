from Parser import Parser
from CodeGenerator import CodeGenerator
from haskellTemplate import template

class Compiler:
    def compile(self, source, library=False):
        # parse input
        (definitions, errors) = Parser().parse(source)

        # check for errors
        if len(errors) > 0:
            return ("", errors)

        # code generation
        code = CodeGenerator().generate(definitions, template, library)

        return (code, errors)
       
