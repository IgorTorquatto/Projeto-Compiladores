def print_ast(node, indent=0):
    if node is None:
        print("  " * indent + "None")
        return

    space = "  " * indent
    print(space + node.__class__.__name__)

    for attr, value in vars(node).items():

        if attr.startswith('_'):
            continue
            
        if isinstance(value, list):
            if value:  
                print(space + "  " + f"{attr}:")
                for item in value:
                    print_ast(item, indent + 2)
            else:
                print(space + "  " + f"{attr}: []")
        
        elif hasattr(value, "__dict__"):
            print(space + "  " + f"{attr}:")
            print_ast(value, indent + 2)
        
        else:
            print(space + "  " + f"{attr}: {value}")


def print_ast_compact(node, indent=0):
    if node is None:
        print("None")
        return

    if not hasattr(node, "__dict__") or not vars(node):
        print(str(node), end="")
        return

    print(f"{node.__class__.__name__}(", end="")
    
    first = True
    for attr, value in vars(node).items():
        if attr.startswith('_'):
            continue
            
        if not first:
            print(", ", end="")
        first = False
        
        print(f"{attr}=", end="")
        
        if isinstance(value, list):
            print("[", end="")
            for i, item in enumerate(value):
                if i > 0:
                    print(", ", end="")
                print_ast_compact(item)
            print("]", end="")
        elif hasattr(value, "__dict__"):
            print_ast_compact(value)
        else:
            print(repr(value), end="")
    
    print(")", end="")

print_ast_pretty = print_ast
print_ast_minimal = print_ast_compact

if __name__ == "__main__":
    from ast_nodes import *

    ast = Program([
        VarDecl("x", "int", IntLiteral(10)),
        VarDecl("y", "int", IntLiteral(20)),
        PrintStmt(StringLiteral("Olá, mundo!"))
    ])
    
    print("=== AST Pretty Print ===")
    print_ast(ast)
    
    print("\n=== AST Compact Print ===")
    print_ast_compact(ast)
    print()  