# Intermediate code generator for Zara language

class IntermediateCodeGenerator:
    label_count = 0  # Counter to generate unique labels

    @staticmethod
    def new_label():
        # Generate a new unique label
        label = f"L{IntermediateCodeGenerator.label_count}"
        IntermediateCodeGenerator.label_count += 1
        return label

    def generate_expression(self, left, op, right):
        # Generate code for arithmetic expressions
        code = f"LOAD {left}\n"
        code += f"LOAD {right}\n"
        if op == '+':
            code += "ADD\n"
        elif op == '-':
            code += "SUB\n"
        elif op == '*':
            code += "MUL\n"
        elif op == '/':
            code += "DIV\n"
        return code

    def generate_if_else(self, condition, if_block, else_block):
        # Generate code for an if-else statement
        else_label = self.new_label()
        end_label = self.new_label()

        code = condition
        code += f"IF_FALSE GOTO {else_label}\n"
        code += if_block
        code += f"GOTO {end_label}\n"
        code += f"{else_label}:\n"
        code += else_block
        code += f"{end_label}:\n"
        return code

    def generate_while_loop(self, condition, loop_body):
        # Generate code for a while loop
        start_label = self.new_label()
        end_label = self.new_label()

        code = f"{start_label}:\n"
        code += condition
        code += f"IF_FALSE GOTO {end_label}\n"
        code += loop_body
        code += f"GOTO {start_label}\n"
        code += f"{end_label}:\n"
        return code

    def generate_function(self, func_name, params, body, return_var):
        # Generate code for a function
        code = f"FUNC {func_name}\n"
        for param in params:
            code += f"LOAD {param}\n"
        code += body
        code += f"RETURN {return_var}\n"
        code += f"END_FUNC {func_name}\n"
        return code


# Example usage of the generator

# Create an instance of the code generator
gen = IntermediateCodeGenerator()

# Generate code for an arithmetic expression (e.g., x - y)
expr_code = gen.generate_expression('x', '-', 'y')

# Generate code for an if-else statement
if_block_code = f"STORE result\n"
else_block_code = f"STORE result\n"
if_else_code = gen.generate_if_else(expr_code, if_block_code, else_block_code)

# Generate code for a while loop (e.g., while (x > y))
condition_code = f"LOAD x\nLOAD y\nGT\n"  # Example condition
while_loop_code = gen.generate_while_loop(condition_code, f"{expr_code}STORE result\n")

# Generate code for a function
function_code = gen.generate_function("calculate", ["x", "y"], if_else_code, "result")

# Print the generated code
print("Generated Intermediate Code for Function 'calculate':")
print(function_code)
