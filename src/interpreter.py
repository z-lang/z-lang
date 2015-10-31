import checker
from checker import Function
from checker import Call

class Interpreter:

    def interpret(self, context, call):
        localContext = context.copy()

        # interpret call
        if call.getName() in context:
            func = context[call.getName()]
            if len(func.params) != len(call.args):
                print("param and arg count does not match: " + call.getName() + " " + str(len(func.params)) + "=" + str(len(args)))
                return None

            # add argrument to local context
            for i in range(0, len(call.args)):
                print(func.params[i])
                arg = self.interpret(context, call.args[i])
                localContext[func.params[i]] = Function(arg.getName(), [], arg)

            # interpret arguemnts
            call_args = []
            for arg in func.value.args:
                call_args.append(self.interpret(localContext, arg))

            return self.interpret(context, Call(func.value.getName(), call_args))
        else:
            return call

