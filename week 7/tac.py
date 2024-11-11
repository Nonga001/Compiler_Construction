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
        """Generates a new temporary variable for expressions."""
        temp_name = f"t{self.temp_counter}"
        self.temp_counter += 1
        return temp_name

    def new_label(self):
        """Generates a new label for control structures."""
        label_name = f"L{self.label_counter}"
        self.label_counter += 1
        return label_name

    def generate_expression(self, expr):
        """Generates TAC for a binary expression."""
        operator, left, right = expr
        temp = self.new_temp()
        self.code.append(f"{temp} = {left} {operator} {right}")
        return temp

    def generate_assignment(self, var, expr):
        """Generates TAC for an assignment statement."""
        result = self.generate_expression(expr)
        self.code.append(f"{var} = {result}")

    def generate_if(self, condition, true_block, false_block=None):
        """Generates TAC for an if-else control structure."""
        condition_result = self.generate_expression(condition)
        true_label = self.new_label()
        end_label = self.new_label()

        # Condition check and jump
        self.code.append(f"if {condition_result} goto {true_label}")

        # False block
        if false_block:
            for statement in false_block:
                self.process_statement(statement)
            self.code.append(f"goto {end_label}")

        # True block
        self.code.append(f"{true_label}:")
        for statement in true_block:
            self.process_statement(statement)

        self.code.append(f"{end_label}:")

    def generate_while(self, condition, body):
        """Generates TAC for a while loop."""
        start_label = self.new_label()
        end_label = self.new_label()

        # Loop start
        self.code.append(f"{start_label}:")
        condition_result = self.generate_expression(condition)
        self.code.append(f"if not {condition_result} goto {end_label}")

        # Loop body
        for statement in body:
            self.process_statement(statement)
        self.code.append(f"goto {start_label}")
        self.code.append(f"{end_label}:")

    def generate_function_call(self, func_name, args):
        """Generates TAC for a function call."""
        for arg in args:
            self.code.append(f"param {arg}")
        self.code.append(f"call {func_name}, {len(args)}")

    def process_statement(self, statement):
        """Processes a single statement and generates corresponding TAC."""
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
        """Prints the generated three-address code."""
        for line in self.code:
            print(line)


# Sample Zara code in structured format for the generator
sample_code = [
    ("assign", "a", ("+", "b", "c")),                # a = b + c
    ("assign", "x", ("-", "d", "e")),                # x = d - e
    ("if", ("==", "a", "x"),                         # if a == x
        [("assign", "y", ("*", "a", "x"))],          #     y = a * x
        [("assign", "y", ("/", "a", "x"))]           # else y = a / x
    ),
    ("while", (">", "n", "0"),                       # while n > 0
        [
            ("assign", "n", ("-", "n", "1"))         #     n = n - 1
        ]
    ),
    ("call", "print", ["a", "x", "y"])               # print(a, x, y)
]

# Run the code generator
generator = IntermediateCodeGenerator()

# Process each statement in the sample Zara code
for stmt in sample_code:
    generator.process_statement(stmt)

# Print the generated three-address code
print("Generated Three-Address Code (TAC):")
generator.print_code()
