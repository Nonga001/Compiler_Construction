# Define basic types and a symbol representation
class Symbol:
    def __init__(self, name, sym_type, scope_level):
        self.name = name
        self.type = sym_type
        self.scope_level = scope_level

class SymbolTable:
    def __init__(self):
        self.table = []
        
    def add_symbol(self, symbol):
        self.table.append(symbol)
        
    def get_symbol(self, name, scope_level):
        for symbol in reversed(self.table):
            if symbol.name == name and symbol.scope_level <= scope_level:
                return symbol
        return None

class Type:
    INTEGER = 'int'
    FLOAT = 'float'
    STRING = 'string'
    ARRAY = 'array'
    STACK = 'stack'

# Define the Semantic Analyzer with type checking and scope management
class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = SymbolTable()
        self.current_scope_level = 0

    def enter_scope(self):
        self.current_scope_level += 1

    def exit_scope(self):
        # Clean up symbols at the current scope level when exiting
        self.symbol_table.table = [
            sym for sym in self.symbol_table.table if sym.scope_level < self.current_scope_level
        ]
        self.current_scope_level -= 1

    def declare_variable(self, name, sym_type):
        symbol = self.symbol_table.get_symbol(name, self.current_scope_level)
        if symbol:
            raise Exception(f"Error: Variable '{name}' already declared in current scope.")
        self.symbol_table.add_symbol(Symbol(name, sym_type, self.current_scope_level))

    def check_variable(self, name):
        symbol = self.symbol_table.get_symbol(name, self.current_scope_level)
        if not symbol:
            raise Exception(f"Error: Variable '{name}' is not declared.")
        return symbol

    def check_type_consistency(self, left_type, right_type):
        if left_type != right_type:
            raise Exception(f"Error: Type mismatch between '{left_type}' and '{right_type}'.")

    def declare_array(self, name, element_type):
        self.declare_variable(name, Type.ARRAY)
        self.symbol_table.add_symbol(Symbol(name, element_type, self.current_scope_level))

    def check_array_access(self, name, index_type):
        symbol = self.check_variable(name)
        if symbol.type != Type.ARRAY:
            raise Exception(f"Error: '{name}' is not an array.")
        self.check_type_consistency(index_type, Type.INTEGER)

    def declare_stack(self, name, element_type):
        self.declare_variable(name, Type.STACK)
        self.symbol_table.add_symbol(Symbol(name, element_type, self.current_scope_level))

    def check_stack_push(self, name, value_type):
        symbol = self.check_variable(name)
        if symbol.type != Type.STACK:
            raise Exception(f"Error: '{name}' is not a stack.")
        if symbol.type != value_type:
            raise Exception(f"Error: Stack '{name}' expected type '{symbol.type}' but got '{value_type}'.")

# Test functions (mocked code below, assuming a Zara program parser provides data)
def test_correct_usage(analyzer):
    analyzer.enter_scope()
    analyzer.declare_variable("x", Type.INTEGER)
    analyzer.declare_variable("y", Type.INTEGER)
    analyzer.check_type_consistency(Type.INTEGER, Type.INTEGER)  # Example correct type usage

    # Array declaration and access
    analyzer.declare_array("arr", Type.INTEGER)
    analyzer.check_array_access("arr", Type.INTEGER)

    # Stack usage
    analyzer.declare_stack("stackInt", Type.INTEGER)
    analyzer.check_stack_push("stackInt", Type.INTEGER)  # Correct usage
    
    analyzer.exit_scope()
    print("Test passed: Correct usage.")

def test_incorrect_usage(analyzer):
    analyzer.enter_scope()
    analyzer.declare_variable("x", Type.INTEGER)
    try:
        analyzer.check_type_consistency(Type.INTEGER, Type.FLOAT)  # Incorrect type usage
    except Exception as e:
        print(e)

    # Array access with wrong index type
    try:
        analyzer.declare_array("arr", Type.INTEGER)
        analyzer.check_array_access("arr", Type.FLOAT)  # Should fail
    except Exception as e:
        print(e)

    # Stack push with wrong type
    try:
        analyzer.declare_stack("stackInt", Type.INTEGER)
        analyzer.check_stack_push("stackInt", Type.FLOAT)  # Should fail
    except Exception as e:
        print(e)

    analyzer.exit_scope()

# Running tests
analyzer = SemanticAnalyzer()
print("Testing correct usage:")
test_correct_usage(analyzer)
print("\nTesting incorrect usage:")
test_incorrect_usage(analyzer)
