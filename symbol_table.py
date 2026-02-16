class SemanticError(Exception):
    pass


class Symbol:
    def __init__(self, name, sym_type, extra=None):
        self.name = name
        self.type = sym_type
        self.extra = extra 

    def __str__(self):
        if self.extra:
            return f"Symbol({self.name}, {self.type}, {self.extra})"
        return f"Symbol({self.name}, {self.type})"

    def __repr__(self):
        return self.__str__()


class SymbolTable:
    def __init__(self, parent=None):
        self.parent = parent
        self.symbols = {}

    def declare(self, name, symbol):
        if name in self.symbols:
            raise SemanticError(f"Declaração duplicada do identificador '{name}'")
        self.symbols[name] = symbol

    def lookup(self, name):
        if name in self.symbols:
            return self.symbols[name]
        if self.parent:
            return self.parent.lookup(name)
        raise SemanticError(f"Uso de identificador não declarado '{name}'")

    def lookup_current_scope(self, name):
        return self.symbols.get(name)

    def __str__(self):
        return f"SymbolTable({self.symbols})"

    def __repr__(self):
        return self.__str__()