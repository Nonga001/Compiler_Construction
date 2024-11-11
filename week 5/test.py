class SymbolTable:
    def __init__(self):
        self.symbols = {}
        self.scopes = [[]]  # list of symbols for each scope

    def enter_scope(self):
        self.scopes.append([])

    def exit_scope(self):
        self.scopes.pop()

    def declare(self, name, type_):
        if name in self.symbols:
            raise ValueError(f"Variable '{name}' already declared")
        self.symbols[name] = type_
        self.scopes[-1].append((name, type_))

    def lookup(self, name):
        for scope in reversed(self.scopes):
            for symbol in scope:
                if symbol[0] == name:
                    return symbol[1]
        raise ValueError(f"Variable '{name}' not found")

    def check_type(self, name, expected_type):
        actual_type = self.lookup(name)
        if actual_type != expected_type:
            raise TypeError(f"Variable '{name}' is of type '{actual_type}', expected '{expected_type}'")


class TypeChecker:
    def __init__(self, symbol_table):
        self.symbol_table = symbol_table

    def check_expression(self, expr):
        if isinstance(expr, tuple):
            operator, left, right = expr
            left_type = self.check_expression(left)
            right_type = self.check_expression(right)

            if operator == "+":
                if left_type == right_type:
                    return left_type
                else:
                    raise TypeError(f"Cannot add '{left_type}' and '{right_type}' types")
            elif operator == "-":
                if left_type == right_type:
                    return left_type
                else:
                    raise TypeError(f"Cannot subtract '{left_type}' and '{right_type}' types")
        elif isinstance(expr, str):
            return self.symbol_table.lookup(expr)
        return expr


class ScopeChecker:
    def __init__(self, symbol_table):
        self.symbol_table = symbol_table

    def check_use(self, name, line):
        try:
            self.symbol_table.lookup(name)
        except ValueError:
            raise ValueError(f"Line {line}: Variable '{name}' used without declaration")


class FunctionChecker:
    def __init__(self, symbol_table):
        self.symbol_table = symbol_table

    def check_function_call(self, func_name, args, line):
        if func_name not in self.symbol_table.symbols:
            raise ValueError(f"Line {line}: Function '{func_name}' is not declared")

        func_type = self.symbol_table.lookup(func_name)
        if len(args) != len(func_type):
            raise ValueError(f"Line {line}: Incorrect number of arguments for function '{func_name}'")


class ArrayStackChecker:
    def __init__(self, symbol_table):
        self.symbol_table = symbol_table

    def check_array_usage(self, name, index, line):
        array_type = self.symbol_table.lookup(name)
        if array_type != "array":
            raise TypeError(f"Line {line}: '{name}' is not an array")
        if not isinstance(index, int):
            raise TypeError(f"Line {line}: Array index must be an integer, found {type(index)}")

    def check_stack_usage(self, name, line):
        stack_type = self.symbol_table.lookup(name)
        if stack_type != "stack":
            raise TypeError(f"Line {line}: '{name}' is not a stack")


class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = SymbolTable()
        self.type_checker = TypeChecker(self.symbol_table)
        self.scope_checker = ScopeChecker(self.symbol_table)
        self.function_checker = FunctionChecker(self.symbol_table)
        self.array_stack_checker = ArrayStackChecker(self.symbol_table)

    def analyze(self, code):
        lines = code.split('\n')
        for line_number, line in enumerate(lines, 1):
            self.check_node(line, line_number)

    def check_node(self, line, line_number):
        tokens = line.split()
        if not tokens:
            return  # Ignore empty lines

        if tokens[0] == "declare":
            self.symbol_table.declare(tokens[1], tokens[2])
        elif tokens[0] == "use":
            self.scope_checker.check_use(tokens[1], line_number)
            self.type_checker.check_expression(tokens[1])
        elif tokens[0] == "function_call":
            self.function_checker.check_function_call(tokens[1], tokens[2:], line_number)
        elif tokens[0] == "array_access":
            self.array_stack_checker.check_array_usage(tokens[1], int(tokens[2]), line_number)
        elif tokens[0] == "stack_operation":
            self.array_stack_checker.check_stack_usage(tokens[1], line_number)


def get_input_code():
    print("Enter Zara code (type 'exit' to finish):")
    code = []
    while True:
        line = input()
        if line.lower() == 'exit':
            break
        code.append(line)
    return '\n'.join(code)


def test_analyzer():
    code = get_input_code()
    analyzer = SemanticAnalyzer()

    try:
        analyzer.analyze(code)
        print("Code is semantically correct!")
    except Exception as e:
        print(f"Error: {e}")


# Run the program
test_analyzer()
