"""
main.py

Driver do compilador que conecta todas as outras fases da compilação.
"""

import sys
import os

from lexer import Lexer
from parser import Parser
from ast_printer import print_ast
from codegen import CodeGenerator
from semantic import SemanticAnalyzer, SemanticError
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
    try:
        ast = parser.parse()
        print_ast(ast)
    except Exception as e:
        print(f"Erro durante o parsing: {e}")
        sys.exit(1)


def print_ast_json_only(source_code):
    lexer = Lexer(source_code)
    parser = Parser(lexer)
    try:
        ast = parser.parse()
        print_ast_json(ast)
    except Exception as e:
        print(f"Erro durante o parsing: {e}")
        sys.exit(1)


def compile_and_generate(source_code, output_file="output.py"):

    try:
        lexer = Lexer(source_code)
        parser = Parser(lexer)
        ast = parser.parse()

        semantic = SemanticAnalyzer()
        semantic.visit(ast)

        codegen = CodeGenerator()
        python_code = codegen.generate(ast)

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(python_code)

        print(f"Sucesso! Arquivo '{output_file}' gerado com sucesso.")
        
    except SemanticError as e:
        print(e)
        sys.exit(1)
    except Exception as e:
        print(f"Erro durante a compilação: {e}")
        sys.exit(1)


def print_usage():
    print("""Uso: python main.py <arquivo.min> [opções]
    Opções:
        --tokens      Imprime a lista de tokens
        --ast         Imprime a AST em formato legível
        --ast-json    Imprime a AST em formato JSON
        --output <arquivo>  Nome do arquivo de saída (padrão: output.py)
        --help        Exibe esta mensagem""")


def main():
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)

    # Verifica se pediu ajuda
    if "--help" in sys.argv:
        print_usage()
        sys.exit(0)

    filename = sys.argv[1]

    if not os.path.exists(filename):
        print(f"Erro: arquivo '{filename}' não encontrado")
        sys.exit(1)

    try:
        with open(filename, "r", encoding="utf-8") as f:
            source_code = f.read()
    except Exception as e:
        print(f"Erro ao ler arquivo '{filename}': {e}")
        sys.exit(1)

    if "--tokens" in sys.argv:
        print_tokens(source_code)
        return

    if "--ast" in sys.argv:
        print_ast_only(source_code)
        return

    if "--ast-json" in sys.argv:
        print_ast_json_only(source_code)
        return

    output_file = "output.py"
    if "--output" in sys.argv:
        try:
            idx = sys.argv.index("--output")
            if idx + 1 < len(sys.argv):
                output_file = sys.argv[idx + 1]
            else:
                print("Erro: --output requer um nome de arquivo")
                sys.exit(1)
        except ValueError:
            pass

    compile_and_generate(source_code, output_file)


if __name__ == "__main__":
    main()