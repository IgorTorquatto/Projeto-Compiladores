import sys

from lexer import Lexer
from parser import Parser
from ast_printer import print_ast
from codegen import CodeGenerator
from semantic import SemanticAnalyzer
from tokens import TokenType
from ast_json import print_ast_json



def print_tokens(source_code):
    lexer = Lexer(source_code)
    while True:
        token = lexer.get_next_token()
        print(token)
        if token.type == TokenType.EOF:
            break


def print_ast_only(source_code):
    lexer = Lexer(source_code)
    parser = Parser(lexer)
    ast = parser.parse()
    print_ast(ast)


def compile_and_generate(source_code):
    # Lexer + Parser
    lexer = Lexer(source_code)
    parser = Parser(lexer)
    ast = parser.parse()

    # Análise semântica
    semantic = SemanticAnalyzer()
    semantic.visit(ast)

    # Geração de código
    codegen = CodeGenerator()
    python_code = codegen.generate(ast)

    with open("output.py", "w") as f:
        f.write(python_code)

    print("sucesso! arquivo output.py já disponivel")


def main():
    if len(sys.argv) < 2:
        print("Uso: python main.py <arquivo> [--tokens | --ast]")
        sys.exit(1)

    filename = sys.argv[1]

    try:
        with open(filename, "r") as f:
            source_code = f.read()
    except FileNotFoundError:
        print(f"Erro: arquivo '{filename}' não encontrado")
        sys.exit(1)

    # Flags opcionais
    if "--tokens" in sys.argv:
        print_tokens(source_code)
        return

    if "--ast" in sys.argv:
        lexer = Lexer(source_code)
        parser = Parser(lexer)
        ast = parser.parse()
        print_ast_json(ast)
        return


    # Execução normal (pipeline completo)
    compile_and_generate(source_code)


if __name__ == "__main__":
    main()
