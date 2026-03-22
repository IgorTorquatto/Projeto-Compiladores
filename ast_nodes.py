"""
ast_nodes.py

Define os nós da Abstract Syntax Tree (AST) da linguagem Mini-Lang.
A AST representa a estrutura hierárquica do programa após a análise sintática.
"""

# ========================================
# Classe base
# ========================================

class Node:
    pass


# ========================================
# Structures
# ========================================

class Program(Node):
    def __init__(self, statements):
        self.statements = statements


class Block(Node):
    def __init__(self, statements):
        self.statements = statements


# ========================================
# Statements
# ========================================

class VarDecl(Node):
    def __init__(self, name, var_type, expr):
        self.name = name
        self.var_type = var_type
        self.expr = expr


class FunctionDecl(Node):
    def __init__(self, name, params, return_type, block):
        self.name = name
        self.params = params
        self.return_type = return_type
        self.block = block


class Param(Node):
    def __init__(self, name, param_type):
        self.name = name
        self.param_type = param_type


class Assignment(Node):
    def __init__(self, name, expr):
        self.name = name
        self.expr = expr


class PrintStmt(Node):
    def __init__(self, expr):  
        self.expr = expr        


class IfStmt(Node):
    def __init__(self, condition, then_block, else_block=None):
        self.condition = condition
        self.then_block = then_block
        self.else_block = else_block


class WhileStmt(Node):
    def __init__(self, condition, block):
        self.condition = condition
        self.block = block


class ReturnStmt(Node):
    def __init__(self, expr):
        self.expr = expr


# ========================================
# Expressions
# ========================================

class BinaryOp(Node):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right


class UnaryOp(Node):
    def __init__(self, op, expr):
        self.op = op
        self.expr = expr


class FunctionCall(Node):
    def __init__(self, name, args):
        self.name = name
        self.args = args

class Identifier(Node):
    def __init__(self, name):
        self.name = name


# ========================================
# Tipos de variáveis
# ========================================

class IntLiteral(Node):
    def __init__(self, value):
        self.value = int(value)


class RealLiteral(Node):
    def __init__(self, value):
        self.value = float(value)


class BoolLiteral(Node):
    def __init__(self, value):
        if isinstance(value, str):
            self.value = value.lower() == "true"
        else:
            self.value = bool(value)


class StringLiteral(Node):
    def __init__(self, value):
        self.value = value