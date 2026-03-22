"""
tokens.py

Módulo responsável pela organização dos tipos de token do Mini-Lang.
Cada valor representa uma categoria léxica reconhecida pelo Lexer.
"""

from enum import Enum, auto


class TokenType(Enum):
    
    # Palavras-chave
    VAR = auto()
    SET = auto()
    DEF = auto()
    IF = auto()
    ELSE = auto()
    WHILE = auto()
    RETURN = auto()
    PRINT = auto()

    # Tipos
    INT = auto()
    REAL = auto()
    BOOL = auto()
    VOID = auto()

    # Identificadores e literais
    ID = auto()
    INT_LITERAL = auto()
    REAL_LITERAL = auto()
    STRING_LITERAL = auto()
    BOOL_LITERAL = auto()

    # Operadores aritméticos
    PLUS = auto()
    MINUS = auto()
    MULT = auto()
    DIV = auto()

    # Operadores relacionais
    LT = auto()   # <
    GT = auto()   # >
    LE = auto()   # <=
    GE = auto()   # >=
    EQ = auto()   # ==
    NE = auto()   # !=

    # Operadores lógicos
    AND = auto()
    OR = auto()
    NOT = auto()

    # Símbolos
    ASSIGN = auto()    # =
    LPAREN = auto()    # (
    RPAREN = auto()    # )
    LBRACE = auto()    # {
    RBRACE = auto()    # }
    SEMICOLON = auto() # ;
    COMMA = auto()     # ,
    COLON = auto()     # :

    EOF = auto()  # Fim do arquivo


# Classe que representa um token individual
class Token:
    
    
    def __init__(self, type_, value, line):
        self.type = type_    # Tipo de token
        self.value = value   # Valor do lexer
        self.line = line     # Linha onde apareceu

    # Represetação quando imprime o token
    def __str__(self):
        return f"<{self.type.name}, {self.value}>"

    # Representação para listas e debug
    def __repr__(self):
        return self.__str__()