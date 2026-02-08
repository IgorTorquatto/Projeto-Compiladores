from symbol_table import SymbolTable, Symbol, SemanticError
from ast_nodes import *


class SemanticAnalyzer:
    def __init__(self):
        self.global_scope = SymbolTable()
        self.current_scope = self.global_scope

    def error(self, msg):
        raise SemanticError(f"Erro semântico: {msg}")

    def visit(self, node):
        method_name = f"visit_{type(node).__name__}"
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        for value in vars(node).values():
            if isinstance(value, list):
                for item in value:
                    self.visit(item)
            elif hasattr(value, "__dict__"):
                self.visit(value)

    # ---------------------
    # Nós principais
    # ---------------------
    def visit_Program(self, node):
        for stmt in node.statements:
            self.visit(stmt)

    def visit_Block(self, node):
        self.current_scope = SymbolTable(self.current_scope)
        for stmt in node.statements:
            self.visit(stmt)
        self.current_scope = self.current_scope.parent

    def visit_VarDecl(self, node):
        expr_type = self.visit(node.expr)
        if expr_type != node.var_type:
            self.error(f"Tipo incompatível na declaração de '{node.name}'")
        self.current_scope.declare(
            node.name, Symbol(node.name, node.var_type)
        )

    def visit_Assignment(self, node):
        symbol = self.current_scope.lookup(node.name)
        expr_type = self.visit(node.expr)
        if symbol.type != expr_type:
            self.error(f"Atribuição incompatível para '{node.name}'")

    def visit_PrintStmt(self, node):
        self.visit(node.expr)

    def visit_IfStmt(self, node):
        cond_type = self.visit(node.condition)
        if cond_type != "bool":
            self.error("Condição do if deve ser booleana")
        self.visit(node.then_block)
        if node.else_block:
            self.visit(node.else_block)

    def visit_WhileStmt(self, node):
        cond_type = self.visit(node.condition)
        if cond_type != "bool":
            self.error("Condição do while deve ser booleana")
        self.visit(node.block)

    def visit_ReturnStmt(self, node):
        return self.visit(node.expr)

    # ---------------------
    # Funções
    # ---------------------
    def visit_FunctionDecl(self, node):
        if node.name in self.global_scope.symbols:
            self.error(f"Função '{node.name}' já declarada")

        self.global_scope.declare(
            node.name,
            Symbol(node.name, "function", (node.params, node.return_type))
        )

        self.current_scope = SymbolTable(self.global_scope)
        for param in node.params:
            self.current_scope.declare(
                param.name, Symbol(param.name, param.param_type)
            )

        self.visit(node.block)
        self.current_scope = self.global_scope

    def visit_FunctionCall(self, node):
        symbol = self.current_scope.lookup(node.name)
        if symbol.type != "function":
            self.error(f"'{node.name}' não é uma função")

        params, return_type = symbol.extra
        if len(node.args) != len(params):
            self.error(f"Número incorreto de argumentos em '{node.name}'")

        for arg, param in zip(node.args, params):
            arg_type = self.visit(arg)
            if arg_type != param.param_type:
                self.error(f"Tipo incompatível em chamada de '{node.name}'")

        return return_type

    # ---------------------
    # Expressões
    # ---------------------
    def visit_BinaryOp(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)

        if node.op in ("PLUS", "MINUS", "MULT", "DIV"):
            if left != "int" or right != "int":
                self.error("Operações aritméticas exigem inteiros")
            return "int"

        if node.op in ("LT", "GT", "LE", "GE", "EQ", "NE"):
            if left != right:
                self.error("Comparação entre tipos incompatíveis")
            return "bool"

        if node.op in ("AND", "OR"):
            if left != "bool" or right != "bool":
                self.error("Operações lógicas exigem booleanos")
            return "bool"

    def visit_UnaryOp(self, node):
        expr_type = self.visit(node.expr)
        if node.op == "NOT" and expr_type != "bool":
            self.error("Operador 'not' exige booleano")
        return expr_type

    def visit_Literal(self, node):
        if node.value in ("true", "false"):
            return "bool"
        return "int"

    def visit_Identifier(self, node):
        symbol = self.current_scope.lookup(node.name)
        return symbol.type
