class SemanticError(Exception):
    pass


class Symbol:
    def __init__(self, name, sym_type, extra=None):
        self.name = name
        self.type = sym_type
        self.extra = extra  # usado para funções (parâmetros, retorno)


class SymbolTable:
    def __init__(self, parent=None):
        self.parent = parent
        self.symbols = {}

    def declare(self, name, symbol):
        if name in self.symbols:
            raise SemanticError(f"Declaração duplicada da variável '{name}'")
        self.symbols[name] = symbol

    def lookup(self, name):
        if name in self.symbols:
            return self.symbols[name]
        if self.parent:
            return self.parent.lookup(name)
        raise SemanticError(f"Uso de variável não declarada '{name}'")
