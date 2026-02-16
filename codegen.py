from ast_nodes import *


class CodeGenerator:
    def __init__(self):
        self.indent = 0
        self.lines = []
        self.func_name = None  

    def emit(self, line=""):
        self.lines.append("    " * self.indent + line)

    def generate(self, node):
        self.visit(node)
        return "\n".join(self.lines)

    def visit(self, node):
        if node is None:
            return
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

    def visit_Program(self, node):
        for stmt in node.statements:
            self.visit(stmt)

    def visit_Block(self, node):
        self.indent += 1
        for stmt in node.statements:
            self.visit(stmt)
        self.indent -= 1

    def visit_VarDecl(self, node):
        self.emit(f"{node.name} = {self.visit(node.expr)}")

    def visit_Assignment(self, node):
        self.emit(f"{node.name} = {self.visit(node.expr)}")

    def visit_PrintStmt(self, node):
        # Agora aceita qualquer expressão (string, número, chamada de função, etc.)
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

    def visit_FunctionDecl(self, node):
        params = ", ".join(p.name for p in node.params)
        self.func_name = node.name
        self.emit(f"def {node.name}({params}):")
        self.visit(node.block)
        self.emit()  
        self.func_name = None

    def visit_FunctionCall(self, node):
        args = ", ".join(self.visit(arg) for arg in node.args)
        return f"{node.name}({args})"

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
        op = op_map.get(node.op, node.op)
        return f"({self.visit(node.left)} {op} {self.visit(node.right)})"

    def visit_UnaryOp(self, node):
        op_map = {
            "PLUS": "+",
            "MINUS": "-",
            "NOT": "not",
        }
        op = op_map.get(node.op, node.op)
        return f"({op} {self.visit(node.expr)})"

    def visit_IntLiteral(self, node):
        return str(node.value)

    def visit_RealLiteral(self, node):
        return str(node.value)

    def visit_BoolLiteral(self, node):
        return "True" if node.value else "False"

    def visit_StringLiteral(self, node):
        escaped = node.value.replace('"', '\\"')
        return f'"{escaped}"'

    def visit_Identifier(self, node):
        return node.name