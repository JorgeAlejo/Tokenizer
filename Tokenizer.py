from dataclasses import dataclass


# Definicion de Token
@dataclass
class Token:
    type        : str
    value       : str
    line_number : int = 0
    index       : int = 0


# Definiciones de tokens
literal_tokens = {
    '+' : 'PLUS',
    '-' : 'MINUS',
    '*' : 'TIMES',
    '/' : 'DIVIDE',
    ';' : 'SEMI',
    ',' : 'COMMA',
    '(' : 'LPAREN',
    ')' : 'RPAREN',
    '{' : 'LBRACE',
    '}' : 'RBRACE',
    '<' : 'LT',
    '>' : 'GT',
    '=' : 'ASSIGN',
    '==': 'EQ',
    '>=': 'GE',
    '<=': 'LE',
    '!=': 'NE',
    '&&': 'AND',
    '||': 'OR',
    '!' : 'NOT',
}

keywords = {
    'var', 'print', 'if', 'else', 'while', 'fun',
    'return', 'true', 'false', 'class', 'for', 'nil',
    'this', 'super'
}


def tokenize(text: str) -> Token:
    line_number, n = 1, 0

    while n < len(text):

        # newline
        if text[n] == '\n':
            n += 1
            line_number += 1
            continue

        # whitespace (' \t\n')
        if text[n].isspace():
            if text[n] == '\n':
                line_number += 1
            n += 1
            continue

        # Comentarios de bloque
        if text[n:n+2] == '/*':
            while n < len(text) and text[n:n+2] != '*/':
                if text[n] == '\n':
                    line_number += 1
                n += 1
            n += 2
            continue

        # Comentario de linea
        if text[n:n+2] == '//':
            while n < len(text) and text[n] != '\n':
                n += 1
            continue

        # Tokens de longitud 2
        if text[n:n+2] in literal_tokens:
            yield Token(literal_tokens[text[n:n+2]], text[n:n+2], line_number, n)
            n += 2
            continue

        # Tokens de longitud 1
        if text[n] in literal_tokens:
            yield Token(literal_tokens[text[n]], text[n], line_number, n)
            n += 1
            continue

        # Numeros enteros y de punto flotante
        if text[n].isdigit() or text[n] == '.':
            start = n
            if text[n] == '0' and text[n+1] != '.':
                while n < len(text) and text[n] != '\n':
                    n += 1
                yield Token('ERROR', text[start:n], line_number, start)#ERROR
                continue
            while n < len(text) and text[n].isdigit():
                n += 1
            if n < len(text) and text[n] == '.':
                n += 1
                while n < len(text) and text[n].isdigit():
                    n += 1
                yield Token('FLOAT', text[start:n], line_number, start)
            else:
                yield Token('INTEGER', text[start:n], line_number, start)
            continue

        # Identificadores
        if text[n].isalpha() or text[n] == '_':
            start = n
            while n < len(text) and (text[n].isalnum() or text[n] == '_'):
                n += 1
            if text[start:n] in keywords:
                n += 1
                yield Token('KEYWORD', text[start:n], line_number, start)
                continue
            yield Token('ID', text[start:n], line_number, start)
            continue
        
        #String
        if text[n] == '"':
            start = n
            n += 1
            while n < len(text) and text[n] != '\n' and text[n] != '"':
                n += 1
            if text[n] == '\n':
                n += 1
                yield Token('ERROR', text[start:n], line_number, start)
            else:
                n += 1
                yield Token('STRING', text[start:n], line_number, start)

        n += 1

if __name__ == '__main__':
    import sys

    if len(sys.argv) != 2:
        print('Usage: python tokenizer.py filename')
        exit(0)
    
    text = open(sys.argv[1]).read()
    
    for tok in tokenize(text):
        print(tok)