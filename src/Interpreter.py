from sys import stdin
from Environment import Environment
from TypeChecker import TypeChecker
from Parser import Parser
from CodeGenerator import CodeGenerator
from haskellTemplate import template
from Compiler import Compiler
from time import sleep
from subprocess import Popen, PIPE, STDOUT
from select import select
from os import devnull, O_NONBLOCK
from fcntl import fcntl, F_SETFL

class GHCI:
    def __init__(self):
        self.process = Popen(['ghci', '-v0'], stdout=PIPE, stdin=PIPE, stderr=PIPE)
        self.stdin = self.process.stdin
        self.stdout = self.process.stdout
        self.stderr = self.process.stderr
        self.devnull = open(devnull, "w")

        fcntl(self.stdout.fileno(), F_SETFL, O_NONBLOCK)
        fcntl(self.stderr.fileno(), F_SETFL, O_NONBLOCK)

    def execute(self, code):
        self.stdin.flush()
        self.stdout.flush()
        self.stderr.flush()

        self.stdout.read()
        self.stderr.read()

        self.stdin.write(bytes(code + "\n", "utf-8"))
        self.stdin.flush()
        self.stdout.flush()
        self.stderr.flush()

        # read input
        out = ""
        fds = select([self.stdout, self.stderr], [], [], 1)[0]
        while len(fds) > 0:
            for fd in fds:
                fd.flush()
                line = fd.read().decode("utf-8")
                out += line
            fds = select([self.stdout, self.stderr], [], [], 1)[0]
        print(out.strip(), end="", flush=True)


class Interpreter:
    def __init__(self):
        self.commands = {
            ":type" : self.printType,
            ":list" : self.printList,
            ":show" : self.printDefinition,
            ":code" : self.printGeneratedCode,
            ":string" : self.setString,
            ":help" : lambda x: None,
            "def"   : self.addDefinition,
        }

        self.printString = False
        self.env = Environment()
        self.checker = TypeChecker()
        self.ghci = GHCI()

        
        generator = CodeGenerator()
        code = generator.generateLibrary(template)
        interpret = ""

        for definition in code.strip().splitlines():
            if not definition.startswith('z_'):
                continue
            interpret += ":{\nlet\n" + definition.strip() + "\n:}\n"
        self.ghci.execute(interpret)

        # imports
        self.ghci.execute("import Data.Char")

    def interpret(self):
        self.printInfo()
        self.printLineInput()

        line = self.readLine()
        while line:
            self.execute(line)
            self.printLineInput()
            line = self.readLine()
        print()

    def printInfo(self):
        print("Commandline interpreter for zlang")
        print("Copyright 2015 by Roger Knecht")

    def printLineInput(self):
        print("zlang> ", end="", flush=True)

    def readLine(self):
        input = ""
        for line in stdin:
            if line[:-1].endswith("\\"):
                input += line[:-2]
            else:
                input += line
                return input

    def execute(self, line):
        tokens = line.strip().split(' ')
        tokens = list(filter(lambda x: len(x) > 0, tokens))

        if len(tokens) == 0:
            return

        cmd = tokens[0]

        if cmd in self.commands:
            self.commands[cmd](line)
        else:
            self.printCall(line)

    def printType(self, line):
        tokens = line.strip().split(' ')
       
        if len(tokens) < 2:
            print("No symbol specified")

        for symbol in tokens[1:]:
            if symbol in self.env.elements:
                (type, node, local) = self.env.get(symbol)
                print(symbol + " :: " + str(type))
            else:
                print(symbol + " :: Symbol does not exists")

    def printList(self, line):
        for name, (type, node, local) in self.env.elements.items():
            print(name + " :: " + str(type))
            sleep(0.05)

    def printDefinition(self, line):
        tokens = line.strip().split(' ')
       
        if len(tokens) < 2:
            print("No symbol specified")

        for symbol in tokens[1:]:
            if symbol in self.env.elements:
                (type, node, local) = self.env.get(symbol)
                print(str(node))
            else:
                print(symbol + " :: Symbol does not exists")

    def printGeneratedCode(self, line):
        tokens = line.strip().split(' ')
       
        if len(tokens) < 2:
            print("No symbol specified")

        for symbol in tokens[1:]:
            if not symbol in self.env.elements:
                print("No symbol " + symbol)
                continue

            # code generation
            generator = CodeGenerator()
            code = generator.generateDefinition(self.env, symbol, template)
            if code == None:
                print("Native function")
            else:
                print(code.strip())

    def addDefinition(self, line):
        (code, errors) = Compiler().compile(line, self.env)

        # check for errors
        if len(errors) > 0:
            for error in errors:
                print(error)
            return

        code = ":{\nlet\n" + code.strip() + "\n:}\n" 
        self.ghci.execute(code)

    def printCall(self, line):
        (code, errors) = Compiler().compile("def v = " + line, self.env)

        # check for errors
        if len(errors) > 0:
            for error in errors:
                print(error)
            return

        if self.printString and "v" in self.env.elements and str(self.env.get("v")[0]) == "[Int]": 
            code = ":{\nlet\n" + code.strip() + "\n:}\nmap (\\x -> chr x) z_v\n" 
        else:
            code = ":{\nlet\n" + code.strip() + "\n:}\nz_v\n" 
        self.ghci.execute(code)
        print()

    def loadNative(self, path):
        native = open(path, "r")
        code = native.read()
        native.close()

        out = ""
        for definition in code.strip().split("\n\n"):
            out += ":{\nlet\n" + definition.strip() + "\n:}\n" 
        self.ghci.execute(out)

    def loadModule(self, path):
        module = open(path, "r")
        (code, errors) = Compiler().compile(module.read(), self.env)
        module.close()

        # check for errors
        if len(errors) > 0:
            for error in errors:
                print(error)
            return

        out = ""
        for definition in code.strip().split("\n\n"):
            out += ":{\nlet\n" + definition.strip() + "\n:}\n" 
        self.ghci.execute(out)

    def setString(self, line):
        tokens = line.strip().split(' ')
       
        if len(tokens) > 1:
            if tokens[1] == "on":
                self.printString = True
            elif tokens[1] == "off":
                self.printString = False


       


