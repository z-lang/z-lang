from Parser import Parser
from TypeChecker import TypeChecker
from Environment import Environment
from CodeGenerator import CodeGenerator
from haskellTemplate import template

class Compiler:
    def compile(self, source, library=False):
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
        code = generator.generate(env, template)

        # generate library
        if library:
            code += generator.generateLibrary(template)

        return (code, errors)
       
