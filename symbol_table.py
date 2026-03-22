"""
symbol_table.py

Tabela de símbolos, controla escopo e declarações.
"""

class SemanticError(Exception):
    pass


class Symbol:
    
    def __init__(self, name, sym_type, extra=None):
        self.name = name      # Nome do identificador
        self.type = sym_type  # Tipo
        self.extra = extra    # Informação extra 


    def __str__(self):
        if self.extra:
            return f"Symbol({self.name}, {self.type}, {self.extra})"
        return f"Symbol({self.name}, {self.type})"


    def __repr__(self):
        return self.__str__()


class SymbolTable:
    
    def __init__(self, parent=None):
        self.parent = parent  # Escopo "pai"
        self.symbols = {}     # Dicionário dos símbolos


    # Declarar símbolo, criar viriável, função e parâmetro
    def declare(self, name, symbol):
        if name in self.symbols:
            raise SemanticError(f"Declaração duplicada do identificador '{name}'")
        self.symbols[name] = symbol


    # Buscar símbolo com escopo, se não achar busca o "pai"
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