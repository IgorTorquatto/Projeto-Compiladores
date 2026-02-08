import json

def ast_to_dict(node):
    if node is None:
        return None

    result = {
        "type": node.__class__.__name__
    }

    for attr, value in node.__dict__.items():
        if isinstance(value, list):
            result[attr] = [ast_to_dict(v) for v in value]
        elif hasattr(value, "__dict__"):
            result[attr] = ast_to_dict(value)
        else:
            result[attr] = value

    return result


def print_ast_json(ast):
    ast_dict = ast_to_dict(ast)
    print(json.dumps(ast_dict, indent=2, ensure_ascii=False))
