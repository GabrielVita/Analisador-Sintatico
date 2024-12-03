import re
import tkinter as tk
from tkinter import scrolledtext, messagebox

# Definição das categorias de tokens
KEYWORDS = ['safira', 'diamante', 'esmeralda', 'ametista', 'topazio', 'água-marinha', 'granada']
OPERATORS = ['+', '-', '*', '/', '=', '==', '!=', '<', '>', '<=', '>=']
DELIMITERS = ['(', ')', '{', '}', ';', ',']
STRING_LITERAL = r'\".*?\"'

# Funções de detecção de tokens
def is_keyword(word):
    return word in KEYWORDS

def is_delimiter(char):
    return char in DELIMITERS

def is_operator(char):
    return char in OPERATORS

def is_number(token):
    return re.match(r'^\d+(\.\d+)?$', token) is not None

def is_identifier(token):
    return re.match(r'^[A-Za-z_]\w*$', token) is not None

# Analisador Léxico
def lex_analyzer(code):
    tokens = []
    current_line = 1
    code = re.sub(r'//.*?\n|/\*.*?\*/', '', code, flags=re.DOTALL)
    lines = code.split('\n')
    
    for line in lines:
        line_tokens = re.split(r'(\W)', line)
        for token in line_tokens:
            token = token.strip()
            if not token:
                continue

            if is_keyword(token):
                tokens.append((current_line, token, 'KEYWORD', None))
            elif is_number(token):
                tokens.append((current_line, token, 'NUMBER', token))
            elif token in OPERATORS:
                tokens.append((current_line, token, 'OPERATOR', token))
            elif is_delimiter(token):
                tokens.append((current_line, token, 'DELIMITER', token))
            elif is_identifier(token):
                tokens.append((current_line, token, 'IDENTIFIER', None))
            elif re.match(STRING_LITERAL, token):
                tokens.append((current_line, token, 'STRING', token))
            else:
                tokens.append((current_line, token, 'UNKNOWN', token))
        
        current_line += 1

    return tokens

# Analisador Sintático
def parse(tokens):
    index = 0

    def expect(token_type, value=None):
        nonlocal index
        if index < len(tokens):
            current_token = tokens[index]
            if current_token[2] == token_type and (value is None or current_token[1] == value):
                index += 1
                return True
        return False

    def parse_program():
        if not expect('KEYWORD', 'safira'):
            raise SyntaxError("Erro: O programa deve começar com 'safira'.")
        if not expect('IDENTIFIER', 'main'):
            raise SyntaxError("Erro: O nome da função principal deve ser 'main'.")
        if not expect('DELIMITER', '('):
            raise SyntaxError("Erro: Esperado '(' após 'main'.")
        if not expect('DELIMITER', ')'):
            raise SyntaxError("Erro: Esperado ')' após '('.")
        if not expect('DELIMITER', '{'):
            raise SyntaxError("Erro: Esperado '{' no início do programa.")
        parse_body()
        if not expect('DELIMITER', '}'):
            raise SyntaxError("Erro: Esperado '}' no final do programa.")

    def parse_body():
        while index < len(tokens) and tokens[index][1] != '}':
            if tokens[index][2] == 'KEYWORD' and tokens[index][1] in ['safira', 'diamante', 'esmeralda']:
                parse_declaration()
            elif tokens[index][2] == 'KEYWORD' and tokens[index][1] == 'ametista':
                parse_print()
            elif tokens[index][2] == 'KEYWORD' and tokens[index][1] == 'topazio':
                parse_conditional()
            else:
                raise SyntaxError(f"Erro: Comando inesperado na linha {tokens[index][0]}.")

    def parse_declaration():
        expect('KEYWORD')
        if not expect('IDENTIFIER'):
            raise SyntaxError("Erro: Esperado identificador após o tipo na declaração de variável.")
        if not expect('DELIMITER', ';'):
            raise SyntaxError("Erro: Esperado ';' no final da declaração.")

    def parse_print():
        expect('KEYWORD', 'ametista')
        if not expect('DELIMITER', '('):
            raise SyntaxError("Erro: Esperado '(' após 'ametista'.")
        while not expect('DELIMITER', ')'):
            if not (expect('STRING') or expect('IDENTIFIER') or expect('NUMBER') or expect('OPERATOR')):
                raise SyntaxError("Erro: Esperado string, identificador, número ou operador dentro de 'ametista'.")
        if not expect('DELIMITER', ';'):
            raise SyntaxError("Erro: Esperado ';' ao final do comando 'ametista'.")

    def parse_conditional():
        expect('KEYWORD', 'topazio')
        if not expect('DELIMITER', '('):
            raise SyntaxError("Erro: Esperado '(' após 'topazio'.")
        parse_expression()
        if not expect('DELIMITER', ')'):
            raise SyntaxError("Erro: Esperado ')' após a condição de 'topazio'.")
        if not expect('DELIMITER', '{'):
            raise SyntaxError("Erro: Esperado '{' no bloco de 'topazio'.")
        parse_body()
        if not expect('DELIMITER', '}'):
            raise SyntaxError("Erro: Esperado '}' ao final do bloco de 'topazio'.")
        if index < len(tokens) and tokens[index][1] == 'água-marinha':
            expect('KEYWORD', 'água-marinha')
            if not expect('DELIMITER', '{'):
                raise SyntaxError("Erro: Esperado '{' no bloco de 'água-marinha'.")
            parse_body()
            if not expect('DELIMITER', '}'):
                raise SyntaxError("Erro: Esperado '}' ao final do bloco de 'água-marinha'.")

    def parse_expression():
        if not (expect('IDENTIFIER') or expect('NUMBER')):
            raise SyntaxError("Erro: Esperado identificador ou número na expressão.")
        if expect('OPERATOR'):
            parse_expression()

    parse_program()
    return "Análise sintática concluída: sem erros!"

# Função para Analisar Léxico e Sintático
def analyze():
    code = text_input.get("1.0", tk.END).strip()
    if not code:
        messagebox.showerror("Erro", "Nenhum código fornecido.")
        return
    
    try:
        tokens = lex_analyzer(code)
        display_tokens(tokens)
        result = parse(tokens)
        result_output.insert(tk.END, result + "\n")
    except SyntaxError as e:
        result_output.insert(tk.END, f"Erro de Sintaxe: {e}\n")
    except Exception as e:
        result_output.insert(tk.END, f"Erro geral: {e}\n")

# Função para Exibir Tokens
def display_tokens(tokens):
    token_output.delete("1.0", tk.END)
    token_output.insert(tk.END, f"{'Linha':<5} {'Lexema':<20} {'Token':<15} {'Valor':<15}\n")
    token_output.insert(tk.END, f"{'-'*5} {'-'*20} {'-'*15} {'-'*15}\n")
    for line, lexeme, token, value in tokens:
        token_output.insert(tk.END, f"{line:<5} {lexeme:<20} {token:<15} {str(value):<15}\n")

# Função para Limpar Dados
def clear_all():
    text_input.delete("1.0", tk.END)
    token_output.delete("1.0", tk.END)
    result_output.delete("1.0", tk.END)

# Interface Gráfica
root = tk.Tk()
root.title("Analisador Léxico e Sintático")
root.geometry("800x600")

# Caixa de entrada
tk.Label(root, text="Insira o código:").pack(pady=5)
text_input = scrolledtext.ScrolledText(root, width=90, height=10)
text_input.pack(pady=5)

# Botões
button_frame = tk.Frame(root)
button_frame.pack(pady=5)
analyze_button = tk.Button(button_frame, text="Analisar", command=analyze)
analyze_button.pack(side="left", padx=5)
clear_button = tk.Button(button_frame, text="Limpar", command=clear_all)
clear_button.pack(side="left", padx=5)

# Exibição de Tokens
tk.Label(root, text="Tokens:").pack(pady=5)
token_output = scrolledtext.ScrolledText(root, width=90, height=10)
token_output.pack(pady=5)

# Exibição de Resultados
tk.Label(root, text="Resultado da Análise Sintática:").pack(pady=5)
result_output = scrolledtext.ScrolledText(root, width=90, height=10)
result_output.pack(pady=5)

root.mainloop()
