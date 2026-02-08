from tokens import Token, TokenType

KEYWORDS = {
    "var": TokenType.VAR,
    "set": TokenType.SET,
    "def": TokenType.DEF,
    "if": TokenType.IF,
    "else": TokenType.ELSE,
    "while": TokenType.WHILE,
    "return": TokenType.RETURN,
    "print": TokenType.PRINT,
    "int": TokenType.INT,
    "real": TokenType.REAL,
    "bool": TokenType.BOOL,
    "void": TokenType.VOID,
    "true": TokenType.TRUE,
    "false": TokenType.FALSE,
    "not": TokenType.NOT,
    "and": TokenType.AND,
    "or": TokenType.OR,
}


class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.line = 1
        self.column = 1

    def current_char(self):
        if self.pos >= len(self.text):
            return None
        return self.text[self.pos]

    def advance(self):
        if self.current_char() == '\n':
            self.line += 1
            self.column = 0
        self.pos += 1
        self.column += 1

    def skip_whitespace(self):
        while self.current_char() is not None and self.current_char().isspace():
            self.advance()

    def number(self):
        start_col = self.column
        value = ""
        while self.current_char() and self.current_char().isdigit():
            value += self.current_char()
            self.advance()
        return Token(TokenType.INT_LITERAL, value, self.line, start_col)

    def identifier_or_keyword(self):
        start_col = self.column
        value = ""
        while self.current_char() and (self.current_char().isalnum() or self.current_char() == "_"):
            value += self.current_char()
            self.advance()

        token_type = KEYWORDS.get(value, TokenType.ID)
        return Token(token_type, value, self.line, start_col)

    def get_next_token(self):
        while self.current_char() is not None:

            if self.current_char().isspace():
                self.skip_whitespace()
                continue

            if self.current_char().isdigit():
                return self.number()

            if self.current_char().isalpha() or self.current_char() == "_":
                return self.identifier_or_keyword()

            ch = self.current_char()

            # Operadores e símbolos
            if ch == '+':
                self.advance()
                return Token(TokenType.PLUS, '+', self.line, self.column - 1)
            if ch == '-':
                self.advance()
                return Token(TokenType.MINUS, '-', self.line, self.column - 1)
            if ch == '*':
                self.advance()
                return Token(TokenType.MULT, '*', self.line, self.column - 1)
            if ch == '/':
                self.advance()
                return Token(TokenType.DIV, '/', self.line, self.column - 1)

            if ch == '=':
                self.advance()
                if self.current_char() == '=':
                    self.advance()
                    return Token(TokenType.EQ, '==', self.line, self.column - 2)
                return Token(TokenType.ASSIGN, '=', self.line, self.column - 1)

            if ch == '!':
                self.advance()
                if self.current_char() == '=':
                    self.advance()
                    return Token(TokenType.NE, '!=', self.line, self.column - 2)

            if ch == '<':
                self.advance()
                if self.current_char() == '=':
                    self.advance()
                    return Token(TokenType.LE, '<=', self.line, self.column - 2)
                return Token(TokenType.LT, '<', self.line, self.column - 1)

            if ch == '>':
                self.advance()
                if self.current_char() == '=':
                    self.advance()
                    return Token(TokenType.GE, '>=', self.line, self.column - 2)
                return Token(TokenType.GT, '>', self.line, self.column - 1)

            if ch == '(':
                self.advance()
                return Token(TokenType.LPAREN, '(', self.line, self.column - 1)
            if ch == ')':
                self.advance()
                return Token(TokenType.RPAREN, ')', self.line, self.column - 1)
            if ch == '{':
                self.advance()
                return Token(TokenType.LBRACE, '{', self.line, self.column - 1)
            if ch == '}':
                self.advance()
                return Token(TokenType.RBRACE, '}', self.line, self.column - 1)
            if ch == ':':
                self.advance()
                return Token(TokenType.COLON, ':', self.line, self.column - 1)
            if ch == ',':
                self.advance()
                return Token(TokenType.COMMA, ',', self.line, self.column - 1)
            if ch == ';':
                self.advance()
                return Token(TokenType.SEMICOLON, ';', self.line, self.column - 1)

            raise Exception(f"Caractere inválido '{ch}' na linha {self.line}")

        return Token(TokenType.EOF, None, self.line, self.column)
