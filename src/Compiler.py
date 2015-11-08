from Parser import Parser
from TypeChecker import TypeChecker
from Environment import Environment
from CodeGenerator import CodeGenerator
from haskellTemplate import template

class Compiler:
    def compile(self, source, library=False):
        # parse input
        (definitions, errors) = Parser().parse(source)

        # check for errors
        if len(errors) > 0:
            return ("", errors)

        # type checking
        for definition in definitions:
            TypeChecker().check(errors, Environment(), definition) 

        # check for errors
        if len(errors) > 0:
            return ("", errors)

        # code generation
        code = CodeGenerator().generate(definitions, template, library)

        return (code, errors)
       
