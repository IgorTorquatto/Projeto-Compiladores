def print_ast(node, indent=0):
    space = "  " * indent
    print(space + node.__class__.__name__)

    for attr, value in vars(node).items():
        if isinstance(value, list):
            for item in value:
                print_ast(item, indent + 1)
        elif hasattr(value, "__dict__"):
            print_ast(value, indent + 1)
        else:
            print(space + "  " + f"{attr}: {value}")
