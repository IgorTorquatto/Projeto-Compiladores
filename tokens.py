from enum import Enum, auto

class TokenType(Enum):
    #palavras-chave
    VAR = auto()
    SET = auto()
    DEF = auto()
    IF = auto()
    ELSE = auto()
    WHILE = auto()
    RETURN = auto()
    PRINT = auto()
    INT = auto()
    REAL = auto()
    BOOL = auto()
    VOID = auto()
    TRUE = auto()
    FALSE = auto()
    NOT = auto()
    AND = auto()
    OR = auto()
    #identificadores,literais
    ID = auto()
    INT_LITERAL = auto()
    #operadores
    PLUS = auto()
    MINUS = auto()
    MULT = auto()
    DIV = auto()
    LT = auto()
    GT = auto()
    LE = auto()
    GE = auto()
    EQ = auto()
    NE = auto()
    ASSIGN = auto()
    #simbolos
    LPAREN = auto()
    RPAREN = auto()
    LBRACE = auto()
    RBRACE = auto()
    COLON = auto()
    COMMA = auto()
    SEMICOLON = auto()
    EOF = auto()

class Token:
    def __init__(self, type_, value, line, column):
        self.type = type_
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return f"<{self.type.name}, {self.value}> (linha {self.line})"
