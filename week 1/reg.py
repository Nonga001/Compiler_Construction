import re

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
        print("\nSymbol Table:")
        for name, details in self.table.items():
            print(f"Variable: {name}, Type: {details['type']}, Value: {details['value']}")

# Lexical Scanner using Regex
def lexical_scanner(source_code, symbol_table):
    # Define regex patterns for tokens
    token_patterns = [
        (r'\s+', None),                      # whitespace (ignored)
        (r'\+', 'PLUS'),                     # PLUS operator
        (r'-', 'MINUS'),                    # MINUS operator
        (r'\*', 'MULTIPLY'),                # MULTIPLY operator
        (r'/', 'DIVIDE'),                    # DIVIDE operator
        (r'=', 'ASSIGNMENT'),                # ASSIGNMENT operator
        (r'\bif\b', 'IF'),                   # IF keyword
        (r'\belse\b', 'ELSE'),               # ELSE keyword
        (r'\bfor\b', 'FOR'),                 # FOR keyword
        (r'\bwhile\b', 'WHILE'),             # WHILE keyword
        (r'\bfunction\b', 'FUNCTION'),       # FUNCTION keyword
        (r'\breturn\b', 'RETURN'),           # RETURN keyword
        (r'\d+(\.\d+)?', 'NUMBER'),          # INTEGER or FLOAT
        (r'[a-zA-Z_][a-zA-Z0-9_]*', 'IDENTIFIER'),  # IDENTIFIER
        (r'.', 'UNKNOWN')                    # Catch-all for unrecognized characters
    ]

    # Create a single regex pattern by combining all token patterns
    combined_pattern = '|'.join(f'(?P<{name}>{pattern})' for pattern, name in token_patterns if name)

    for match in re.finditer(combined_pattern, source_code):
        token_type = match.lastgroup
        token_value = match.group(token_type)

        # Handle recognized tokens
        if token_type == 'NUMBER':
            print(f"Token: NUMBER ({token_value})")
        elif token_type == 'IDENTIFIER':
            if token_value not in symbol_table.table:  # Only add if not already in symbol table
                print(f"Token: IDENTIFIER ({token_value})")
                symbol_table.add_symbol(token_value, "unknown")  # Add to symbol table
            else:
                print(f"Token: IDENTIFIER ({token_value}) already declared.")
        elif token_type == 'PLUS':
            print("Token: PLUS Operator")
        elif token_type == 'MINUS':
            print("Token: MINUS Operator")
        elif token_type == 'MULTIPLY':
            print("Token: MULTIPLY Operator")
        elif token_type == 'DIVIDE':
            print("Token: DIVIDE Operator")
        elif token_type == 'ASSIGNMENT':
            print("Token: ASSIGNMENT Operator")
        elif token_type == 'IF':
            print("Token: IF Keyword")
        elif token_type == 'ELSE':
            print("Token: ELSE Keyword")
        elif token_type == 'FOR':
            print("Token: FOR Keyword")
        elif token_type == 'WHILE':
            print("Token: WHILE Keyword")
        elif token_type == 'FUNCTION':
            print("Token: FUNCTION Keyword")
        elif token_type == 'RETURN':
            print("Token: RETURN Keyword")
        elif token_type == 'UNKNOWN':
            print(f"Error: Unrecognized character '{token_value}'")  # Catch unrecognized characters

# Main function to run the lexical scanner
def main():
    symbol_table = SymbolTable()
    
    # Get input from the user
    print("Enter your source code (type 'END' on a new line to finish):")
    source_code = ""
    while True:
        line = input()
        if line.strip().upper() == "END":
            break
        source_code += line + "\n"

    print("\nLexical analysis of the source code:")
    lexical_scanner(source_code, symbol_table)

    # Print the symbol table after scanning
    symbol_table.print_table()

# Run the main function
if __name__ == "__main__":
    main()
<<<<<<< HEAD
"""to finish type END at the start of a new line below"""
=======
"""to finish, type END at the start of a new line"""
>>>>>>> origin/main
