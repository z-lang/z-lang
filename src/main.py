import sys
import argparse

from Compiler import Compiler
import subprocess

def main():
    # parse arguments
    arg_parser = argparse.ArgumentParser(
            description="Compiler for the functional programming language zlang"
        )
    arg_parser.add_argument('files', nargs="+", help="input files")
    arg_parser.add_argument('-t', '--print-ast', action='store_true', help="Prints abstract syntax tree")
    arg_parser.add_argument('-s', '--print-source', action='store_true', help="Prints source code")
    arg_parser.add_argument('-c', '--print-code', action='store_true', help="Prints generated code")
    args = arg_parser.parse_args()

    # read files into string
    source = ""
    for f in args.files:
        with open(f, "r") as file:
            source += file.read() + "\n"
            file.close()

    # print source
    if args.print_source:
        print("### INPUT ###")
        print(source)

    # compile
    (code, errors) = Compiler().compile(source)

    # check for errors
    if len(errors) > 0:
        for error in errors:
            print(error)
        print("Abort.")
        return

    # print generated code 
    if args.print_code:
        print("### OUTPUT ###")
        print(code)

    # writing output file
    outputFilename = "output.hs"
    if len(args.files) == 1:
        outputFilename = args.files[0].split(".")[0] + ".hs"
    outputFile = open(outputFilename, "w")
    outputFile.write(code)
    outputFile.close()

    # executing interpreter
    subprocess.call(["ghci", outputFilename])

if __name__ == "__main__":
    main()
