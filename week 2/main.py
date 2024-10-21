import re

# Token types
TOKEN_TYPES = {
    'KEYWORD': r'\b(if|else|do|while)\b',
    'IDENTIFIER': r'\b[a-zA-Z_]\w*\b',
    'NUMBER': r'\b\d+(\.\d+)?\b',  # Supports integers and floats
    'STRING': r'"[^"]*"',  # Double-quoted strings
    'OPERATOR': r'[+\-*/=]',
    'WHITESPACE': r'\s+',  # Skip whitespace
    'UNKNOWN': r'.'  # Catch-all for unrecognized characters
}

# Combine token patterns into one regex
token_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in TOKEN_TYPES.items())

def lexical_analyzer(source_code):
    tokens = []
    for match in re.finditer(token_regex, source_code):
        token_type = match.lastgroup
        token_value = match.group(token_type)
        
        if token_type != 'WHITESPACE':  # Skip whitespace tokens
            tokens.append((token_type, token_value))
    return tokens

def main():
    # Prompt user for input
    print("Enter Zara code (type 'exit' to finish):")
    source_code = ""
    
    while True:
        line = input()  # Read input line by line
        if line.strip().lower() == 'exit':  # Exit condition
            break
        source_code += line + "\n"  # Append line to source_code
    
    # Test the lexical analyzer
    tokens = lexical_analyzer(source_code)
    for token in tokens:
        print(f"Token Type: {token[0]}, Token Value: {token[1]}")

if __name__ == "__main__":
    main()


# sample code used is 
# if x = 10 + 20 do {
#     y = "Hello, World!";
#     while y > 5 {
#         y = y - 1;
#     }
# }
# else {
#     z = 2.5;
# }