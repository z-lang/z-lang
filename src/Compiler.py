from Parser import Parser
from TypeChecker import TypeChecker
from Environment import Environment
from CodeGenerator import CodeGenerator
from haskellTemplate import template

class Compiler:
    def compile(self, source, env=None, library=False):
        if env == None:
            env = Environment()

        # parse input
        (definitions, errors) = Parser().parse(source)

        # check for errors
        if len(errors) > 0:
            return ("", errors)

        # type checking
        for definition in definitions:
            TypeChecker().check(errors, env, definition) 

        # check for errors
        if len(errors) > 0:
            return ("", errors)

        # code generation
        generator = CodeGenerator()
        for node  in definitions:
            symbol = node[0].value()
            code = generator.generateDefinition(env, symbol, template)

        # generate library
        if library:
            code += generator.generateLibrary(template)

        return (code, errors)
       
