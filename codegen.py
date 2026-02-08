from ast_nodes import *


class CodeGenerator:
    def __init__(self):
        self.indent = 0
        self.lines = []

    def emit(self, line=""):
        self.lines.append("    " * self.indent + line)

    def generate(self, node):
        self.visit(node)
        return "\n".join(self.lines)

    def visit(self, node):
        method_name = f"visit_{type(node).__name__}"
        visitor = getattr(self, method_name)
        return visitor(node)

    # -------------------
    # Estrutura geral
    # -------------------
    def visit_Program(self, node):
        for stmt in node.statements:
            self.visit(stmt)

    def visit_Block(self, node):
        self.indent += 1
        for stmt in node.statements:
            self.visit(stmt)
        self.indent -= 1

    # -------------------
    # Comandos
    # -------------------
    def visit_VarDecl(self, node):
        self.emit(f"{node.name} = {self.visit(node.expr)}")

    def visit_Assignment(self, node):
        self.emit(f"{node.name} = {self.visit(node.expr)}")

    def visit_PrintStmt(self, node):
        self.emit(f"print({self.visit(node.expr)})")

    def visit_IfStmt(self, node):
        self.emit(f"if {self.visit(node.condition)}:")
        self.visit(node.then_block)
        if node.else_block:
            self.emit("else:")
            self.visit(node.else_block)

    def visit_WhileStmt(self, node):
        self.emit(f"while {self.visit(node.condition)}:")
        self.visit(node.block)

    def visit_ReturnStmt(self, node):
        self.emit(f"return {self.visit(node.expr)}")

    # -------------------
    # Funções
    # -------------------
    def visit_FunctionDecl(self, node):
        params = ", ".join(p.name for p in node.params)
        self.emit(f"def {node.name}({params}):")
        self.visit(node.block)
        self.emit()

    def visit_FunctionCall(self, node):
        args = ", ".join(self.visit(arg) for arg in node.args)
        return f"{node.name}({args})"

    # -------------------
    # Expressões
    # -------------------
    def visit_BinaryOp(self, node):
        op_map = {
            "PLUS": "+",
            "MINUS": "-",
            "MULT": "*",
            "DIV": "/",
            "LT": "<",
            "GT": ">",
            "LE": "<=",
            "GE": ">=",
            "EQ": "==",
            "NE": "!=",
            "AND": "and",
            "OR": "or",
        }
        return f"({self.visit(node.left)} {op_map[node.op]} {self.visit(node.right)})"

    def visit_UnaryOp(self, node):
        op_map = {
            "PLUS": "+",
            "MINUS": "-",
            "NOT": "not",
        }
        return f"({op_map[node.op]} {self.visit(node.expr)})"

    def visit_Literal(self, node):
        if node.value == "true":
            return "True"
        if node.value == "false":
            return "False"
        return node.value

    def visit_Identifier(self, node):
        return node.name
