import sys
import argparse

from Compiler import Compiler
from Interpreter import Interpreter

def main():
    # parse arguments
    arg_parser = argparse.ArgumentParser(
            description="Compiler for the functional programming language zlang"
        )
    arg_parser.add_argument('files', nargs="+", help="input files")
    arg_parser.add_argument('-n', '--native', help="Prints abstract syntax tree")
    args = arg_parser.parse_args()

    # interpreter
    interpreter = Interpreter()

    # load native
    if args.native:
        interpreter.loadNative(args.native)

    # load modules
    for file in args.files:
        interpreter.loadModule(file)
    interpreter.interpret()


if __name__ == "__main__":
    main()
