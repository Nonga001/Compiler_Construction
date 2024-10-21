"""our simplified version of zara grammar for our parser

program       ::= statement*
statement     ::= if_statement | do_while_statement | for_statement | method_declaration | expression_statement
if_statement  ::= 'if' '(' expression ')' '{' statement* '}'
do_while_statement ::= 'do' '{' statement* '}' 'while' '(' expression ')'
for_statement ::= 'for' '(' expression ';' expression ';' expression ')' '{' statement* '}'
method_declaration ::= 'def' IDENTIFIER '(' parameter_list? ')' '{' statement* '}'
expression_statement ::= expression ';'
expression    ::= IDENTIFIER '=' expression | literal | IDENTIFIER | binary_expression
binary_expression ::= expression ( '+' | '-' | '*' | '/' ) expression
literal       ::= NUMBER | STRING
parameter_list ::= IDENTIFIER (',' IDENTIFIER)*


"""


import re

class Tokenizer:
    def tokenize(self, source_code):
        token_specification = [
            ('NUMBER', r'\d+(\.\d+)?'),   # Integer or decimal number
            ('IDENTIFIER', r'[a-zA-Z_]\w*'), # Identifiers
            ('IF', r'if'),                  # Keyword if
            ('ELSE', r'else'),              # Keyword else
            ('DO', r'do'),                  # Keyword do
            ('WHILE', r'while'),            # Keyword while
            ('FOR', r'for'),                # Keyword for
            ('DEF', r'def'),                # Keyword def
            ('LPAREN', r'\('),              # Left parenthesis
            ('RPAREN', r'\)'),              # Right parenthesis
            ('LBRACE', r'\{'),              # Left brace
            ('RBRACE', r'\}'),              # Right brace
            ('SEMICOLON', r';'),            # Semicolon
            ('ASSIGN', r'='),               # Assignment operator
            ('EQUAL', r'=='),               # Equal to operator
            ('LT', r'<'),                   # Less than operator
            ('GT', r'>'),                   # Greater than operator
            ('LEQ', r'<='),                 # Less than or equal to
            ('GEQ', r'>='),                 # Greater than or equal to
            ('PLUS', r'\+'),                # Plus operator
            ('MINUS', r'-'),                # Minus operator
            ('TIMES', r'\*'),               # Multiplication operator
            ('DIVIDE', r'/'),               # Division operator
            ('STRING', r'"[^"]*"'),         # String literals
            ('WHITESPACE', r'\s+'),         # Skip whitespace
            ('UNKNOWN', r'.'),              # Catch-all for unrecognized characters
        ]
        tok_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_specification)
        token_regex = re.compile(tok_regex)
        tokens = []

        for match in token_regex.finditer(source_code):
            token_type = match.lastgroup
            if token_type == 'WHITESPACE':
                continue  # Skip whitespace
            elif token_type == 'UNKNOWN':
                raise SyntaxError(f"Unexpected character: {match.group(token_type)}")
            token_value = match.group(token_type)
            tokens.append((token_type, token_value))
        return tokens


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token_index = 0
        self.current_token = self.tokens[self.current_token_index] if self.tokens else None

    def parse(self):
        while self.current_token:
            self.program()

    def program(self):
        while self.current_token:
            self.statement()

    def statement(self):
        if self.current_token[0] == 'IF':
            self.match('IF')
            self.match('LPAREN')
            self.expression()
            self.match('RPAREN')
            self.match('LBRACE')
            self.statement()
            self.match('RBRACE')
            if self.current_token and self.current_token[0] == 'ELSE':
                self.match('ELSE')
                self.match('LBRACE')
                self.statement()
                self.match('RBRACE')
        elif self.current_token[0] == 'DO':
            self.match('DO')
            self.match('LBRACE')
            self.statement()
            self.match('RBRACE')
            self.match('WHILE')
            self.match('LPAREN')
            self.expression()
            self.match('RPAREN')
        elif self.current_token[0] == 'FOR':
            self.match('FOR')
            self.match('LPAREN')
            self.assignment()
            self.expression()
            self.match(';')
            self.assignment()
            self.match('RPAREN')
            self.match('LBRACE')
            self.statement()
            self.match('RBRACE')
        elif self.current_token[0] == 'IDENTIFIER':
            self.assignment()
        else:
            raise SyntaxError(f"Unexpected token: {self.current_token}")

    def assignment(self):
        self.match('IDENTIFIER')
        self.match('ASSIGN')
        self.expression()
        self.match('SEMICOLON')

    def expression(self):
        if self.current_token[0] == 'NUMBER':
            self.match('NUMBER')
        elif self.current_token[0] == 'IDENTIFIER':
            self.match('IDENTIFIER')
        else:
            raise SyntaxError(f"Expected NUMBER or IDENTIFIER, got: {self.current_token}")

    def match(self, expected_type):
        if self.current_token and self.current_token[0] == expected_type:
            print(f"Matched token: {self.current_token}")
            self.current_token_index += 1
            self.current_token = self.tokens[self.current_token_index] if self.current_token_index < len(self.tokens) else None
        else:
            raise SyntaxError(f"Expected token: {expected_type}, but got: {self.current_token}")

# Main execution
if __name__ == "__main__":
    source_code = input("Enter Zara code:\n")
    tokenizer = Tokenizer()
    try:
        tokens = tokenizer.tokenize(source_code)
        parser = Parser(tokens)
        parser.parse()
        print("Parsing completed successfully.")
    except SyntaxError as e:
        print(f"Syntax error: {e}")
