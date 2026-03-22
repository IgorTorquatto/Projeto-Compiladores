"""
parser.py

Implementa o analisador sintático da linguagem Mini-Lang.
Ele recebe os tokens produzidos pelo lexer e constrói a AST.
"""

from tokens import TokenType
from ast_nodes import *

class ParserError(Exception):
    pass

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self, msg):
        raise ParserError(f"Erro sintático: {msg} (linha {self.current_token.line})")

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error(f"esperado {token_type.name}")

    def parse(self):
        statements = []
        while self.current_token.type != TokenType.EOF:
            statements.append(self.statement())
        return Program(statements)

    def statement(self):
        t = self.current_token.type

        if t == TokenType.VAR:
            node = self.var_decl()
            self.eat(TokenType.SEMICOLON)
            return node

        if t == TokenType.SET:
            node = self.assignment()
            self.eat(TokenType.SEMICOLON)
            return node

        if t == TokenType.PRINT:
            node = self.print_stmt()
            self.eat(TokenType.SEMICOLON)  
            return node

        if t == TokenType.IF:
            return self.if_stmt()

        if t == TokenType.WHILE:
            return self.while_stmt()

        if t == TokenType.RETURN:
            node = self.return_stmt()
            self.eat(TokenType.SEMICOLON)
            return node

        if t == TokenType.DEF:
            return self.function_decl()

        if t == TokenType.LBRACE:
            return self.block()

        self.error("comando inválido")

    def block(self):
        self.eat(TokenType.LBRACE)
        statements = []
        while self.current_token.type != TokenType.RBRACE:
            statements.append(self.statement())
        self.eat(TokenType.RBRACE)
        return Block(statements)

    def var_decl(self):
        self.eat(TokenType.VAR)
        name = self.current_token.value
        self.eat(TokenType.ID)
        self.eat(TokenType.COLON)
        var_type = self.current_token.value
        self.eat(self.current_token.type)
        self.eat(TokenType.ASSIGN)
        expr = self.expression()
        return VarDecl(name, var_type, expr)

    def assignment(self):
        self.eat(TokenType.SET)
        name = self.current_token.value
        self.eat(TokenType.ID)
        self.eat(TokenType.ASSIGN)
        expr = self.expression()
        return Assignment(name, expr)

    def print_stmt(self):
        self.eat(TokenType.PRINT)
        
        if self.current_token.type == TokenType.STRING_LITERAL:
            token = self.current_token
            self.eat(TokenType.STRING_LITERAL)
            return PrintStmt(StringLiteral(token.value))
        else:
            expr = self.expression()
            return PrintStmt(expr)

    def if_stmt(self):
        self.eat(TokenType.IF)
        self.eat(TokenType.LPAREN)
        cond = self.expression()
        self.eat(TokenType.RPAREN)
        then_block = self.block()
        else_block = None
        if self.current_token.type == TokenType.ELSE:
            self.eat(TokenType.ELSE)
            else_block = self.block()
        return IfStmt(cond, then_block, else_block)

    def while_stmt(self):
        self.eat(TokenType.WHILE)
        self.eat(TokenType.LPAREN)
        cond = self.expression()
        self.eat(TokenType.RPAREN)
        return WhileStmt(cond, self.block())

    def return_stmt(self):
        self.eat(TokenType.RETURN)
        return ReturnStmt(self.expression())

    def function_decl(self):
        self.eat(TokenType.DEF)
        name = self.current_token.value
        self.eat(TokenType.ID)
        self.eat(TokenType.LPAREN)

        params = []
        if self.current_token.type != TokenType.RPAREN:
            params.append(self.param())
            while self.current_token.type == TokenType.COMMA:
                self.eat(TokenType.COMMA)
                params.append(self.param())

        self.eat(TokenType.RPAREN)
        self.eat(TokenType.COLON)
        return_type = self.current_token.value
        self.eat(self.current_token.type)
        block = self.block()
        return FunctionDecl(name, params, return_type, block)

    def param(self):
        name = self.current_token.value
        self.eat(TokenType.ID)
        self.eat(TokenType.COLON)
        ptype = self.current_token.value
        self.eat(self.current_token.type)
        return Param(name, ptype)

    def expression(self):
        node = self.simple_expression()
        while self.current_token.type in (
            TokenType.LT, TokenType.GT, TokenType.LE,
            TokenType.GE, TokenType.EQ, TokenType.NE
        ):
            op = self.current_token.type
            self.eat(op)
            node = BinaryOp(node, op.name, self.simple_expression())
        return node

    def simple_expression(self):
        node = self.term()
        while self.current_token.type in (
            TokenType.PLUS, TokenType.MINUS, TokenType.OR
        ):
            op = self.current_token.type
            self.eat(op)
            node = BinaryOp(node, op.name, self.term())
        return node

    def term(self):
        node = self.factor()
        while self.current_token.type in (
            TokenType.MULT, TokenType.DIV, TokenType.AND
        ):
            op = self.current_token.type
            self.eat(op)
            node = BinaryOp(node, op.name, self.factor())
        return node

    def factor(self):
        t = self.current_token.type

        if t == TokenType.INT_LITERAL:
            value = self.current_token.value
            self.eat(TokenType.INT_LITERAL)
            return IntLiteral(value)

        if t == TokenType.REAL_LITERAL:
            value = self.current_token.value
            self.eat(TokenType.REAL_LITERAL)
            return RealLiteral(value)

        if t == TokenType.BOOL_LITERAL:
            value = self.current_token.value
            self.eat(t)
            return BoolLiteral(value)

        if t == TokenType.ID:
            name = self.current_token.value
            self.eat(TokenType.ID)

            if self.current_token.type == TokenType.LPAREN:
                self.eat(TokenType.LPAREN)
                args = []
                if self.current_token.type != TokenType.RPAREN:
                    args.append(self.expression())
                    while self.current_token.type == TokenType.COMMA:
                        self.eat(TokenType.COMMA)
                        args.append(self.expression())
                self.eat(TokenType.RPAREN)
                return FunctionCall(name, args)

            return Identifier(name)

        if t in (TokenType.PLUS, TokenType.MINUS, TokenType.NOT):
            op = self.current_token.type
            self.eat(op)
            return UnaryOp(op.name, self.factor())

        if t == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            node = self.expression()
            self.eat(TokenType.RPAREN)
            return node

        self.error("expressão inválida")