# gridpy, a python to gridlang compiler

import ast


class Compiler(object):
    def __init__(self):
        # local variables (the top of the stack)
        self.locals = []

        # gridlang code will be appended here as it is generated
        self.code = []

    def compile(self, source):
        # ast.parse returns a module
        module = ast.parse(source)
        self.gen_module(module)
        return '\n'.join(self.code)

    def gen_module(self, module):
        # module.body is a list of statements
        for statement in module.body:
            self.gen_statement(statement)

    def gen_statement(self, statement):
        # statements can be ast.Assign, ast.FunctionDef, ast.Print, etc
        if isinstance(statement, ast.Assign):
            self.gen_assign(statement)
        elif isinstance(statement, ast.Print):
            self.gen_print(statement)
        else:
            print 'unknown statement: %s' % repr(statement)

    def gen_assign(self, assign):
        # assign.targets is a list of names
        # assign.value is an expression

        # generate code for the value expression
        self.gen_expression(assign.value)

        # when the program execution reaches this point, the top of the stack
        # will contain one value that corresponds to the evaluated expression

        # let's just assume targets is a list of 1 element
        target = assign.targets[0]

        # the temporary expression on the top of the stack is now this variable
        self.locals[-1] = target.id

    def gen_print(self, print_):
        # evaluate the expression being printed
        # assuming only one argument is being passed to print
        self.gen_expression(print_.values[0])

        self.code.append("PRINT")
        # print will pop one value from the stack
        self.locals.pop()

    def gen_expression(self, expression):
        # expressions can be ast.Num, ast.Name, ast.BinOp, etc
        if isinstance(expression, ast.Num):
            self.gen_num(expression)
        elif isinstance(expression, ast.Name):
            self.gen_name(expression)
        else:
            print 'unknown expression: %s' % repr(expression)

    def gen_num(self, num):
        # just push the number onto the stack
        self.code.append("PUSH %d" % num.n)
        self.locals.append("num %d" % num.n)

    def gen_name(self, name):
        # find the variable and put it on top of the stack
        index = self.locals.index(name.id)
        pos = index - len(self.locals)
        self.code.append("PEEK << %d" % pos)
        self.locals.append("copy of %s" % name.id)


if __name__ == '__main__':
    compiler = Compiler()
    source = "a=1; print(a);"
    code = compiler.compile(source)
    print(code)
