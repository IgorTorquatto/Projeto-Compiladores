from symbol_table import SymbolTable, Symbol, SemanticError
from ast_nodes import *


class SemanticAnalyzer:
    def __init__(self):
        self.global_scope = SymbolTable()
        self.current_scope = self.global_scope
        self.current_function_return_type = None

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
                    if item is not None:
                        self.visit(item)
            elif hasattr(value, "__dict__"):
                self.visit(value)

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
            self.error(
                f"Tipo incompatível na declaração de '{node.name}': esperado {node.var_type}, obtido {expr_type}"
            )

        self.current_scope.declare(
            node.name, Symbol(node.name, node.var_type)
        )

    def visit_Assignment(self, node):
        symbol = self.current_scope.lookup(node.name)
        expr_type = self.visit(node.expr)

        if symbol.type != expr_type:
            self.error(
                f"Atribuição incompatível para '{node.name}': esperado {symbol.type}, obtido {expr_type}"
            )

    def visit_PrintStmt(self, node):
        self.visit(node.expr)

    def visit_IfStmt(self, node):
        cond_type = self.visit(node.condition)

        if cond_type != "bool":
            self.error(f"Condição do if deve ser booleana, obtido {cond_type}")

        self.visit(node.then_block)

        if node.else_block:
            self.visit(node.else_block)

    def visit_WhileStmt(self, node):
        cond_type = self.visit(node.condition)

        if cond_type != "bool":
            self.error(f"Condição do while deve ser booleana, obtido {cond_type}")

        self.visit(node.block)

    def visit_ReturnStmt(self, node):
        expr_type = self.visit(node.expr)

        if self.current_function_return_type is None:
            self.error("Comando 'return' fora de função")

        if expr_type != self.current_function_return_type:
            self.error(
                f"Tipo de retorno incompatível: esperado {self.current_function_return_type}, obtido {expr_type}"
            )

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

        self.current_function_return_type = node.return_type

        self.visit(node.block)

        self.current_scope = self.global_scope
        self.current_function_return_type = None

    def visit_FunctionCall(self, node):

        symbol = self.current_scope.lookup(node.name)

        if symbol.type != "function":
            self.error(f"'{node.name}' não é uma função")

        params, return_type = symbol.extra

        if len(node.args) != len(params):
            self.error(
                f"Número incorreto de argumentos em '{node.name}': esperado {len(params)}, obtido {len(node.args)}"
            )

        for i, (arg, param) in enumerate(zip(node.args, params)):
            arg_type = self.visit(arg)

            if arg_type != param.param_type:
                self.error(
                    f"Tipo incompatível no argumento {i+1} de '{node.name}': esperado {param.param_type}, obtido {arg_type}"
                )

        return return_type

    def visit_BinaryOp(self, node):

        left = self.visit(node.left)
        right = self.visit(node.right)

        # Operações aritméticas
        if node.op in ("PLUS", "MINUS", "MULT", "DIV"):

            if left not in ("int", "real") or right not in ("int", "real"):
                self.error(
                    f"Operação aritmética '{node.op}' requer números, obtido {left} e {right}"
                )

            # promoção de tipo
            if left == "real" or right == "real":
                return "real"

            return "int"

        # Comparações
        if node.op in ("LT", "GT", "LE", "GE", "EQ", "NE"):

            if left != right:
                self.error(
                    f"Comparação '{node.op}' entre tipos incompatíveis: {left} e {right}"
                )

            return "bool"

        # Operações lógicas
        if node.op in ("AND", "OR"):

            if left != "bool" or right != "bool":
                self.error(
                    f"Operação lógica '{node.op}' requer booleanos, obtido {left} e {right}"
                )

            return "bool"

        self.error(f"Operador binário desconhecido: {node.op}")

    def visit_UnaryOp(self, node):

        expr_type = self.visit(node.expr)

        if node.op == "NOT":

            if expr_type != "bool":
                self.error(
                    f"Operador 'not' requer booleano, obtido {expr_type}"
                )

        elif node.op in ("PLUS", "MINUS"):

            if expr_type not in ("int", "real"):
                self.error(
                    f"Operador unário '{node.op}' requer número, obtido {expr_type}"
                )

        return expr_type

    def visit_IntLiteral(self, node):
        return "int"

    def visit_RealLiteral(self, node):
        return "real"

    def visit_BoolLiteral(self, node):
        return "bool"

    def visit_StringLiteral(self, node):
        return "string"

    def visit_Identifier(self, node):
        symbol = self.current_scope.lookup(node.name)
        return symbol.type