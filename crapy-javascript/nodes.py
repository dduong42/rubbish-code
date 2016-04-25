class Statement:
    def execute(self, local_variables):
        pass


class Assignation(Statement):
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def execute(self, local_variables):
        local_variables[self.name] = self.value.evaluate(local_variables)

    def __repr__(self):
        return '{}(name={}, value={})'.format(
            self.__class__.__name__,
            self.name,
            self.value,
        )


class Expression:
    def evaluate(self, local_variables):
        pass


class ValueExpression(Expression):
    def __init__(self, value):
        self.value = value

    def evaluate(self, local_variables):
        return self.value

    def __repr__(self):
        return '{}(value={})'.format(
            self.__class__.__name__, repr(self.value))


class Boolean(ValueExpression):
    pass


class Number(ValueExpression):
    pass


class String(ValueExpression):
    pass


class Function(Expression):
    def __init__(self, args, statements, return_expression=None):
        self.args = args
        self.statements = statements
        self.return_expression = return_expression
        self.local_variables = {}

    def __repr__(self):
        return '{}(args={}, statements={}, return_expression={})'.format(
            self.__class__.__name__,
            self.args,
            self.statements,
            self.return_expression,
        )

    def evaluate(self, local_variables):
        def f(*args):
            local_variables = {
                name: value
                for name, value in zip(self.args, args)
            }
            for statement in self.statements:
                statement.execute(local_variables)
            return self.return_expression.evaluate(local_variables)
        return f



class Name(Expression):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '{}(name={})'.format(self.__class__.__name__, self.name)

    def evaluate(self, local_variables):
        return local_variables[self.name]
