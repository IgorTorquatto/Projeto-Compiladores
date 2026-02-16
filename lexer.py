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
    "true": TokenType.BOOL_LITERAL,
    "false": TokenType.BOOL_LITERAL,
    "not": TokenType.NOT,
    "and": TokenType.AND,
    "or": TokenType.OR,
}

class Lexer:
    def __init__(self, source):
        self.source = source
        self.pos = 0
        self.line = 1
        self.tokens = self.tokenize()
        self.current = 0

    def peek(self):
        if self.pos >= len(self.source):
            return '\0'
        return self.source[self.pos]

    def advance(self):
        ch = self.peek()
        self.pos += 1
        return ch

    def skip_whitespace(self):
        while self.pos < len(self.source) and self.peek().isspace():
            if self.peek() == '\n':
                self.line += 1
            self.advance()

    def tokenize(self):
        tokens = []

        while self.pos < len(self.source):
            self.skip_whitespace()

            if self.pos >= len(self.source):
                break

            ch = self.peek()

            if ch.isdigit():
                tokens.append(self.number())

            elif ch == '"':
                tokens.append(self.string())

            elif ch.isalpha() or ch == '_':
                tokens.append(self.identifier())

            elif ch == '+':
                tokens.append(Token(TokenType.PLUS, '+', self.line))
                self.advance()

            elif ch == '-':
                tokens.append(Token(TokenType.MINUS, '-', self.line))
                self.advance()

            elif ch == '*':
                tokens.append(Token(TokenType.MULT, '*', self.line))
                self.advance()

            elif ch == '/':
                tokens.append(Token(TokenType.DIV, '/', self.line))
                self.advance()

            elif ch == '=':
                self.advance()
                if self.peek() == '=':
                    self.advance()
                    tokens.append(Token(TokenType.EQ, '==', self.line))
                else:
                    tokens.append(Token(TokenType.ASSIGN, '=', self.line))

            elif ch == '!':
                self.advance()
                if self.peek() == '=':
                    self.advance()
                    tokens.append(Token(TokenType.NE, '!=', self.line))
                else:
                    raise Exception(f"Caractere inválido '!' na linha {self.line}")

            elif ch == '<':
                self.advance()
                if self.peek() == '=':
                    self.advance()
                    tokens.append(Token(TokenType.LE, '<=', self.line))
                else:
                    tokens.append(Token(TokenType.LT, '<', self.line))

            elif ch == '>':
                self.advance()
                if self.peek() == '=':
                    self.advance()
                    tokens.append(Token(TokenType.GE, '>=', self.line))
                else:
                    tokens.append(Token(TokenType.GT, '>', self.line))

            elif ch == '(':
                tokens.append(Token(TokenType.LPAREN, '(', self.line))
                self.advance()

            elif ch == ')':
                tokens.append(Token(TokenType.RPAREN, ')', self.line))
                self.advance()

            elif ch == '{':
                tokens.append(Token(TokenType.LBRACE, '{', self.line))
                self.advance()

            elif ch == '}':
                tokens.append(Token(TokenType.RBRACE, '}', self.line))
                self.advance()

            elif ch == ';':
                tokens.append(Token(TokenType.SEMICOLON, ';', self.line))
                self.advance()

            elif ch == ',':
                tokens.append(Token(TokenType.COMMA, ',', self.line))
                self.advance()

            elif ch == ':':
                tokens.append(Token(TokenType.COLON, ':', self.line))
                self.advance()

            else:
                raise Exception(f"Caractere inválido '{ch}' na linha {self.line}")

        tokens.append(Token(TokenType.EOF, '', self.line))
        return tokens

    def number(self):
        start = self.pos
        while self.pos < len(self.source) and self.peek().isdigit():
            self.advance()

        if self.pos < len(self.source) and self.peek() == '.':
            self.advance()
            while self.pos < len(self.source) and self.peek().isdigit():
                self.advance()
            return Token(TokenType.REAL_LITERAL,
                         self.source[start:self.pos], self.line)

        return Token(TokenType.INT_LITERAL,
                     self.source[start:self.pos], self.line)

    def string(self):
        self.advance()  
        start = self.pos
        while self.pos < len(self.source) and self.peek() != '"':
            self.advance()
        
        if self.pos >= len(self.source):
            raise Exception(f"String não fechada na linha {self.line}")
            
        value = self.source[start:self.pos]
        self.advance()  
        return Token(TokenType.STRING_LITERAL, value, self.line)

    def identifier(self):
        start = self.pos
        while self.pos < len(self.source) and (self.peek().isalnum() or self.peek() == '_'):
            self.advance()
        text = self.source[start:self.pos]
        
        token_type = KEYWORDS.get(text, TokenType.ID)
        return Token(token_type, text, self.line)

    def get_next_token(self):
        if self.current < len(self.tokens):
            tok = self.tokens[self.current]
            self.current += 1
            return tok
        return Token(TokenType.EOF, '', self.line)