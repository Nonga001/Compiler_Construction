# implementation using LR0  and we will define our grammar as below
"""
1. S -> statement
2. statement -> if_stmt | for_stmt | do_while_stmt | assignment | method_decl
3. if_stmt -> IF LPAREN expr RPAREN LBRACE statement RBRACE (ELSE LBRACE statement RBRACE)?
4. for_stmt -> FOR LPAREN assignment SEMICOLON expr SEMICOLON assignment RPAREN LBRACE statement RBRACE
5. do_while_stmt -> DO LBRACE statement RBRACE WHILE LPAREN expr RPAREN SEMICOLON
6. assignment -> IDENTIFIER ASSIGN expr SEMICOLON
7. expr -> term ((PLUS | MINUS) term)*
8. term -> factor ((MUL | DIV) factor)*
9. factor -> IDENTIFIER | NUMBER | LPAREN expr RPAREN
10. method_decl -> DEF IDENTIFIER LPAREN param_list RPAREN LBRACE statement RBRACE
11. param_list -> IDENTIFIER (COMMA IDENTIFIER)*

"""

import re

class Parser:
    def __init__(self):
        self.tokens = []
        self.position = 0
    
    def tokenize(self, code):
        token_specification = [
            ('NUMBER', r'\d+(\.\d*)?'),      # Integer or decimal number
            ('ASSIGN', r'='),                 # Assignment operator
            ('PLUS', r'\+'),                  # Addition operator
            ('MINUS', r'-'),                  # Subtraction operator
            ('MULT', r'\*'),                  # Multiplication operator
            ('DIV', r'/'),                    # Division operator
            ('IDENTIFIER', r'[A-Za-z_][A-Za-z0-9_]*'),  # Identifiers
            ('LPAREN', r'\('),                # Parenthesis
            ('RPAREN', r'\)'),                # Parenthesis
            ('LBRACE', r'\{'),                # Left brace
            ('RBRACE', r'\}'),                # Right brace
            ('IF', r'if'),                    # If keyword
            ('ELSE', r'else'),                # Else keyword
            ('WHILE', r'while'),              # While keyword
            ('DO', r'do'),                    # Do keyword
            ('FOR', r'for'),                  # For keyword
            ('RETURN', r'return'),            # Return keyword
            ('SEMICOLON', r';'),              # Semicolon
            ('SKIP', r'[ \t]+'),              # Skip spaces and tabs
            ('NEWLINE', r'\n'),               # Line endings
            ('MISMATCH', r'.'),               # Any other character
        ]
        tok_regex = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in token_specification)
        line_number = 1
        line_start = 0
        for mo in re.finditer(tok_regex, code):
            kind = mo.lastgroup
            value = mo.group()
            if kind == 'NEWLINE':
                line_start = mo.end()
                line_number += 1
            elif kind == 'SKIP':
                continue
            elif kind == 'MISMATCH':
                raise RuntimeError(f'{value} unexpected on line {line_number}')
            else:
                self.tokens.append((kind, value))
    
    def parse(self):
        while self.position < len(self.tokens):
            token = self.tokens[self.position]
            print(f'Matched token: {token}')
            self.position += 1
            
            # Implement parsing logic for shift/reduce parsing.
            # This should include handling expressions, control structures, etc.
            
            # Example parsing logic for handling statements and control structures
            if token[0] == 'IF':
                # Handle if statement
                print("Parsing if statement...")
                self.expect('LPAREN')
                self.expect('IDENTIFIER')  # Assuming the condition is an identifier
                self.expect('ASSIGN')       # Assuming an assignment operation
                self.expect('NUMBER')       # Assuming the number to compare against
                self.expect('RPAREN')
                self.expect('LBRACE')
                # Parse the block statements
                self.expect('RBRACE')
            elif token[0] == 'DO':
                print("Parsing do statement...")
                self.expect('LBRACE')
                # Assume some statements here
                self.expect('RBRACE')
                self.expect('WHILE')
                self.expect('LPAREN')
                self.expect('IDENTIFIER')
                self.expect('LESS')         # Assuming a comparison operator
                self.expect('NUMBER')
                self.expect('RPAREN')
            elif token[0] == 'FOR':
                print("Parsing for loop...")
                self.expect('LPAREN')
                self.expect('IDENTIFIER')
                self.expect('ASSIGN')
                self.expect('NUMBER')
                self.expect('SEMICOLON')
                # Assuming loop condition
                self.expect('IDENTIFIER')
                self.expect('LESS')         # Assuming a comparison operator
                self.expect('NUMBER')
                self.expect('SEMICOLON')
                # Assuming loop update
                self.expect('IDENTIFIER')
                self.expect('ASSIGN')
                self.expect('IDENTIFIER')
                self.expect('PLUS')
                self.expect('NUMBER')
                self.expect('RPAREN')
                self.expect('LBRACE')
                # Parse the loop body
                self.expect('RBRACE')
            elif token[0] == 'SEMICOLON':
                print("Semicolon found, ending statement.")

    def expect(self, expected_token_type):
        if self.position < len(self.tokens):
            token = self.tokens[self.position]
            if token[0] == expected_token_type:
                print(f'Expected {expected_token_type}, got {token}')
                self.position += 1
            else:
                raise RuntimeError(f'Expected {expected_token_type}, got {token}')
        else:
            raise RuntimeError(f'Expected {expected_token_type}, but reached end of input.')

def main():
    parser = Parser()
    print("Enter Zara code (type 'exit' to finish input):")
    code_lines = []
    while True:
        line = input()
        if line.strip().lower() == 'exit':
            break
        code_lines.append(line.strip())
    
    code = "\n".join(code_lines)
    
    try:
        parser.tokenize(code)
        parser.parse()
    except RuntimeError as e:
        print(e)

if __name__ == '__main__':
    main()
