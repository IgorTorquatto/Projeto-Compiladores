# MiniLang Compiler

Este projeto implementa um **compilador completo** para uma linguagem simples chamada **MiniLang**, desenvolvido como trabalho final da disciplina de **Compiladores**.

O compilador foi implementado inteiramente em **Python**, sem o uso de geradores automáticos, contemplando todas as fases clássicas do processo de compilação:

* Análise Léxica (Scanner)
* Análise Sintática (Parser descendente recursivo)
* Construção da AST (Árvore Sintática Abstrata)
* Análise Semântica
* Geração de Código (Python)
* Execução do código gerado

---

## 📁 Estrutura do Projeto

```
ast_nodes.py (Definição dos nós da AST)
ast_printer.py (Impressão da AST)
ast_json.py (Conversão da AST para JSON)
codegen.py (Gerador de Código Python)
main.py   (Ponto de entrada do compilador)
grammar.ebnf (Gramática)
lexer.py (Analisador léxico)  
parser.py (Analisador Sintático)
semantic.py (Analisador Semântico)
symbol_table.py (Tabela de símbolos)        
tokens.py (Definição dos tokens)

```

---


---

## 📂 Arquivo de Entrada (MiniLang)

O código fonte da linguagem MiniLang deve ser colocado na pasta:

```bash
exemplos/teste.min
```

Basta editar esse arquivo para escrever seu programa em MiniLang.


## ▶️ Execução do Compilador (Fluxo Normal)

No terminal, dentro da pasta do projeto, execute:

```bash
python main.py exemplos/teste.min
```

Após a execução, o compilador gera automaticamente o arquivo:

```
output.py
```

Para executar o código gerado, utilize:

```bash
python output.py
```

Esse fluxo corresponde ao funcionamento completo do compilador, desde a leitura do código-fonte em MiniLang até a execução do programa traduzido.

---

## 🔎 Modo Scanner – Impressão dos Tokens

O compilador possui um modo específico para demonstrar o funcionamento da **análise léxica**.

Para imprimir a lista de tokens reconhecidos pelo scanner, execute:

```bash
python main.py exemplos/teste.min --tokens
```

Esse modo exibe, no terminal, todos os tokens identificados no código-fonte, incluindo palavras-chave, identificadores, operadores, símbolos e o token de fim de arquivo (EOF).

---

## 🌳 Modo AST – Impressão da Árvore Sintática Abstrata

Também é possível visualizar a **árvore sintática abstrata (AST)** gerada pelo parser.A árvore sintática pode ser exibida de duas formas: formato textual indentado, formato JSON.

Execute o seguinte comando e verá a árvore em formato textual indentado:

```bash
python main.py exemplos/teste.min --ast
```
Execute o seguinte comando e verá a árvore em formato JSON:

```bash
python main.py exemplos/teste.min --ast-json
```

Nesse modo, o compilador imprime uma representação textual e hierárquica da AST, evidenciando a estrutura sintática do programa, sem detalhes léxicos supérfluos como parênteses ou ponto-e-vírgula.

---

## 📘 Observações Finais

* Os modos `--tokens` e `--ast` permitem a demonstração clara das fases de análise léxica e sintática.
* O código gerado é executável em Python.
* A linguagem MiniLang suporta comentários de linha, os comentários são ignorados pelo compilador.
* O arquivo `output.py` é sobrescrito a cada execução.

---

**Autores:** Cicero Igor Alves Torquato, André Castro, Clice Romão, Alex Reis, José Denis, Najla Cavalcante
**Disciplina:** Compiladores
**Instituição:** UFCA