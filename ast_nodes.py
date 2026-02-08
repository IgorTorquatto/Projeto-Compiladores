class ASTNode:
    pass


class Program(ASTNode):
    def __init__(self, statements):
        self.statements = statements


class Block(ASTNode):
    def __init__(self, statements):
        self.statements = statements


class VarDecl(ASTNode):
    def __init__(self, name, var_type, expr):
        self.name = name
        self.var_type = var_type
        self.expr = expr


class Assignment(ASTNode):
    def __init__(self, name, expr):
        self.name = name
        self.expr = expr


class PrintStmt(ASTNode):
    def __init__(self, expr):
        self.expr = expr


class IfStmt(ASTNode):
    def __init__(self, condition, then_block, else_block=None):
        self.condition = condition
        self.then_block = then_block
        self.else_block = else_block


class WhileStmt(ASTNode):
    def __init__(self, condition, block):
        self.condition = condition
        self.block = block


class ReturnStmt(ASTNode):
    def __init__(self, expr):
        self.expr = expr


class FunctionDecl(ASTNode):
    def __init__(self, name, params, return_type, block):
        self.name = name
        self.params = params
        self.return_type = return_type
        self.block = block


class Param(ASTNode):
    def __init__(self, name, param_type):
        self.name = name
        self.param_type = param_type


class BinaryOp(ASTNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right


class UnaryOp(ASTNode):
    def __init__(self, op, expr):
        self.op = op
        self.expr = expr


class Literal(ASTNode):
    def __init__(self, value):
        self.value = value


class Identifier(ASTNode):
    def __init__(self, name):
        self.name = name


class FunctionCall(ASTNode):
    def __init__(self, name, args):
        self.name = name
        self.args = args
