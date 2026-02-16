import json


def ast_to_dict(node):
    if node is None:
        return None
    
    result = {
        "type": node.__class__.__name__
    }

    for attr, value in node.__dict__.items():
        if attr.startswith('_'):
            continue
            
        if isinstance(value, list):
            result[attr] = []
            for item in value:
                if hasattr(item, "__dict__"):
                    result[attr].append(ast_to_dict(item))
                else:
                    result[attr].append(item)
        
        elif hasattr(value, "__dict__"):
            result[attr] = ast_to_dict(value)
        
        else:
            if isinstance(value, bool):
                result[attr] = value
            elif isinstance(value, (int, float)):
                result[attr] = value
            elif value is None:
                result[attr] = None
            else:
                result[attr] = str(value)

    return result


def print_ast_json(ast):
    ast_dict = ast_to_dict(ast)
    print(json.dumps(ast_dict, indent=2, ensure_ascii=False))


def ast_to_json_string(ast, indent=None):
    ast_dict = ast_to_dict(ast)
    if indent is not None:
        return json.dumps(ast_dict, indent=indent, ensure_ascii=False)
    return json.dumps(ast_dict, ensure_ascii=False)


def save_ast_json(ast, filename, indent=2):
    ast_dict = ast_to_dict(ast)
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(ast_dict, f, indent=indent, ensure_ascii=False)

if __name__ == "__main__":
    from ast_nodes import *
    
    ast = Program([
        VarDecl("x", "int", IntLiteral(10)),
        VarDecl("y", "int", IntLiteral(20)),
        FunctionDecl(
            "soma",
            [Param("a", "int"), Param("b", "int")],
            "int",
            Block([
                ReturnStmt(
                    BinaryOp(Identifier("a"), "PLUS", Identifier("b"))
                )
            ])
        ),
        PrintStmt(StringLiteral("Olá, mundo!"))
    ])
    
    print("=== AST em JSON ===")
    print_ast_json(ast)
    
    print("\n=== AST em JSON minificado ===")
    print(ast_to_json_string(ast))
    
    save_ast_json(ast, "ast_test.json")
    print("\nAST salva em 'ast_test.json'")