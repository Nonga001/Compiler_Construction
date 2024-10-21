# Symbol Table Class
class SymbolTable:
    def __init__(self):
        self.table = {}

    def add_symbol(self, name, var_type, value=None):
        if name in self.table:
            raise Exception(f"Error: Variable '{name}' is already declared.")
        self.table[name] = {"type": var_type, "value": value}

    def update_symbol(self, name, value):
        if name not in self.table:
            raise Exception(f"Error: Variable '{name}' is not declared.")
        self.table[name]["value"] = value

    def get_symbol(self, name):
        if name not in self.table:
            raise Exception(f"Error: Variable '{name}' is not declared.")
        return self.table[name]

    def print_table(self):
        for name, details in self.table.items():
            print(f"Variable: {name}, Type: {details['type']}, Value: {details['value']}")

# Lexical Scanner
def lexical_scanner(source_code, symbol_table):
    length = len(source_code)
    i = 0

    while i < length:
        current_char = source_code[i]

        if current_char.isspace():
            i += 1
            continue

        if current_char == '+':
            print("Token: PLUS Operator")
            i += 1
        elif current_char == '-':
            print("Token: MINUS Operator")
            i += 1
        elif current_char == '=':
            print("Token: ASSIGNMENT Operator")
            i += 1
            if i < length and source_code[i].isdigit():
                number = ""
                while i < length and source_code[i].isdigit():
                    number += source_code[i]
                    i += 1
                print(f"Assigning NUMBER {number} to variable")
            elif i < length and source_code[i].isalpha():
                identifier = ""
                while i < length and source_code[i].isalnum():
                    identifier += source_code[i]
                    i += 1
                print(f"Assigning IDENTIFIER {identifier} to variable")

        elif current_char.isalpha():
            identifier = ""
            while i < length and source_code[i].isalnum():
                identifier += source_code[i]
                i += 1

            if identifier == "if":
                print("Token: IF Keyword")
            elif identifier == "else":
                print("Token: ELSE Keyword")
            else:
                print(f"Token: IDENTIFIER ({identifier})")
                symbol_table.add_symbol(identifier, "unknown")

        elif current_char.isdigit():
            number = ""
            while i < length and source_code[i].isdigit():
                number += source_code[i]
                i += 1
            print(f"Token: NUMBER ({number})")

        else:
            print(f"Error: Unrecognized character '{current_char}'")
            i += 1

# Sample input for testing
source_code = "if x = 10 + y - 5 else"
symbol_table = SymbolTable()
print("Lexical analysis of the source code:")
lexical_scanner(source_code, symbol_table)

# Print the symbol table after scanning
symbol_table.print_table()
