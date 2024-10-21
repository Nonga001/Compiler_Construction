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
    def __init__(self, code):
        self.code = code
        self.position = 0
        self.tokens = []
        self.token_regex = [
            (r'if|else|do|while|for|def|return', 'IDENTIFIER'),
            (r'==|!=|<=|>=|>|<', 'COMPARATOR'),
            (r'\+|-|\*|/', 'OPERATOR'),
            (r'=', 'ASSIGN'),
            (r'\d+(\.\d+)?', 'NUMBER'),
            (r'[a-zA-Z_]\w*', 'IDENTIFIER'),
            (r'\s+', None),  # Ignore whitespace
            (r'\{', 'LBRACE'),
            (r'\}', 'RBRACE'),
            (r'\(', 'LPAREN'),
            (r'\)', 'RPAREN'),
            (r';', 'SEMICOLON'),
            (r',', 'COMMA')  # Added comma as a token
        ]

    def tokenize(self):
        while self.position < len(self.code):
            match = None
            for regex, token_type in self.token_regex:
                regex = re.compile(regex)
                match = regex.match(self.code, self.position)
                if match:
                    if token_type:  # Ignore None types (whitespace)
                        self.tokens.append((token_type, match.group(0)))
                    self.position = match.end(0)
                    break
            if not match:
                raise RuntimeError(f'Unexpected character: {self.code[self.position]}')
        return self.tokens

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token_index = 0

    def current_token(self):
        return self.tokens[self.current_token_index] if self.current_token_index < len(self.tokens) else None

    def eat(self, token_type):
        token = self.current_token()
        if token and token[0] == token_type:
            print(f'Matched token: {token}')
            self.current_token_index += 1
        else:
            expected = token_type
            got = token[0] if token else 'EOF'
            raise RuntimeError(f'Syntax error: Expected token: {expected}, but got: {got}')

    def parse(self):
        while self.current_token_index < len(self.tokens):
            token = self.current_token()
            if token[0] == 'IDENTIFIER' and token[1] == 'if':
                self.eat('IDENTIFIER')
                self.eat('LPAREN')
                self.expression()
                self.eat('RPAREN')
                self.eat('LBRACE')
                self.statement()
                self.eat('RBRACE')
            else:
                break

    def expression(self):
        # Basic expression parsing (can be expanded)
        self.eat('IDENTIFIER')
        self.eat('COMPARATOR')
        self.eat('NUMBER')

    def statement(self):
        while self.current_token() and self.current_token()[0] != 'RBRACE':
            self.eat('IDENTIFIER')
            self.eat('ASSIGN')
            self.eat('NUMBER')
            self.eat('SEMICOLON')

def main():
    print("Enter Zara code (type 'exit' to finish input):")
    code = []
    while True:
        line = input()
        if line.strip() == 'exit':
            break
        code.append(line)
    full_code = '\n'.join(code)

    try:
        tokenizer = Tokenizer(full_code)
        tokens = tokenizer.tokenize()
        print("Tokens:", tokens)

        parser = Parser(tokens)
        parser.parse()
        print("Parsing completed successfully.")
    except RuntimeError as e:
        print(e)

if __name__ == '__main__':
    main()
