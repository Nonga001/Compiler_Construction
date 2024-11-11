class SymbolTable:
    def __init__(self):
        self.symbols = {}

    def declare(self, name, type_):
        if name in self.symbols:
            raise ValueError(f"Variable '{name}' already declared.")
        self.symbols[name] = type_

    def lookup(self, name):
        if name not in self.symbols:
            raise ValueError(f"Variable '{name}' not found.")
        return self.symbols[name]


class IntermediateCodeGenerator:
    def __init__(self):
        self.code = []
        self.temp_counter = 0
        self.label_counter = 0
        self.symbol_table = SymbolTable()

    def new_temp(self):
        temp_name = f"t{self.temp_counter}"
        self.temp_counter += 1
        return temp_name

    def new_label(self):
        label_name = f"L{self.label_counter}"
        self.label_counter += 1
        return label_name

    def generate_expression(self, expr):
        operator, left, right = expr
        temp = self.new_temp()
        self.code.append(f"{temp} = {left} {operator} {right}")
        return temp

    def generate_assignment(self, var, expr):
        result = self.generate_expression(expr)
        self.code.append(f"{var} = {result}")

    def generate_if(self, condition, true_block, false_block=None):
        condition_result = self.generate_expression(condition)
        true_label = self.new_label()
        end_label = self.new_label()

        self.code.append(f"if {condition_result} goto {true_label}")

        if false_block:
            for statement in false_block:
                self.process_statement(statement)
            self.code.append(f"goto {end_label}")

        self.code.append(f"{true_label}:")
        for statement in true_block:
            self.process_statement(statement)

        self.code.append(f"{end_label}:")

    def generate_while(self, condition, body):
        start_label = self.new_label()
        end_label = self.new_label()

        self.code.append(f"{start_label}:")
        condition_result = self.generate_expression(condition)
        self.code.append(f"if not {condition_result} goto {end_label}")

        for statement in body:
            self.process_statement(statement)
        self.code.append(f"goto {start_label}")
        self.code.append(f"{end_label}:")

    def generate_function_call(self, func_name, args):
        for arg in args:
            self.code.append(f"param {arg}")
        self.code.append(f"call {func_name}, {len(args)}")

    def process_statement(self, statement):
        if statement[0] == "assign":
            _, var, expr = statement
            self.generate_assignment(var, expr)
        elif statement[0] == "if":
            _, condition, true_block, false_block = statement
            self.generate_if(condition, true_block, false_block)
        elif statement[0] == "while":
            _, condition, body = statement
            self.generate_while(condition, body)
        elif statement[0] == "call":
            _, func_name, args = statement
            self.generate_function_call(func_name, args)

    def print_code(self):
        for line in self.code:
            print(line)


def get_statement():
    stmt_type = input("Enter statement type (assign, if, while, call, or 'done' to finish): ").strip()
    if stmt_type == "assign":
        var = input("Enter variable name: ")
        left = input("Enter left operand: ")
        operator = input("Enter operator (+, -, *, /, etc.): ")
        right = input("Enter right operand: ")
        return ("assign", var, (operator, left, right))
    elif stmt_type == "if":
        left = input("Enter left operand of condition: ")
        operator = input("Enter comparison operator (==, !=, >, <, etc.): ")
        right = input("Enter right operand of condition: ")
        true_block = []
        false_block = []
        print("Enter statements for the 'true' block:")
        while True:
            true_stmt = get_statement()
            if true_stmt == "done":
                break
            true_block.append(true_stmt)
        if input("Do you want an 'else' block? (yes/no): ") == "yes":
            print("Enter statements for the 'false' block:")
            while True:
                false_stmt = get_statement()
                if false_stmt == "done":
                    break
                false_block.append(false_stmt)
        return ("if", (operator, left, right), true_block, false_block)
    elif stmt_type == "while":
        left = input("Enter left operand of condition: ")
        operator = input("Enter comparison operator (==, !=, >, <, etc.): ")
        right = input("Enter right operand of condition: ")
        body = []
        print("Enter statements for the 'while' loop body:")
        while True:
            body_stmt = get_statement()
            if body_stmt == "done":
                break
            body.append(body_stmt)
        return ("while", (operator, left, right), body)
    elif stmt_type == "call":
        func_name = input("Enter function name: ")
        args = input("Enter arguments separated by commas: ").split(",")
        args = [arg.strip() for arg in args]
        return ("call", func_name, args)
    elif stmt_type == "done":
        return "done"
    else:
        print("Invalid statement type!")
        return None


# Main code execution
print("Enter your Zara code statements:")
generator = IntermediateCodeGenerator()
statements = []

while True:
    stmt = get_statement()
    if stmt == "done":
        break
    elif stmt:
        statements.append(stmt)

for stmt in statements:
    generator.process_statement(stmt)

print("\nGenerated Three-Address Code (TAC):")
generator.print_code()
