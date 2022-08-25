from ast import Lt
from tkinter import LEFT
from rich import print
import sly

class MiniCLexer(sly.Lexer):
    # Definicion de simbolos
    tokens = {
        # Palabras reservadas
        'VAR', 'PRINT', 'IF', 'ELSE', 'WHILE', 
        'RETURN', 'TRUE', 'FALSE',

        # Operadores (longitud 2)
        'LT', 'LE', 'GT', 'GE', 'EQ', 'AND', 'OR', 'NE', 'NOT',

        #Otros
        'IDENT', 'NUMBER', 'STRING',
    }
    literals = '+-*/=(){};,'

    #Ignorar espacios en blanco
    ignore = ' \t\r'

    #Ignorar newline
    @_(r'\n+')
    def ignore_newline(self, t):
        self.line_number += t.value.count('\n')
    
    #Igorar comentario bloque
    @_(r'/*(.|\n)*\*/')
    def ignore_comments(self, t):
        self.line_number += t.value.count('\n')
    
    @_(r'//.*\n')
    def ignore_cppcomment(self, t):
        self.line_number += 1
    
    #Defiicion de tokens

    LE  = r'<='
    LT  = r'<'
    GE  = r'>='
    GT  = r'>'
    EQ  = r'=='
    NE  = r'!='
    AND = r'&&'
    OR  = r'\|\|'
    NOT = r'!'

    IDENT = r'[a-zA-Z_][a-zA-Z0-9_]*'
    IDENT['fun']    = FUN
    IDENT['var']    = VAR 
    IDENT['print']  = PRINT
    IDENT['if']     = IF
    IDENT['else']   = ELSE
    IDENT['while']  = WHILE
    IDENT['return'] = RETURN
    IDENT['true']   = TRUE
    IDENT['false']  = FALSE

    @_(r'\d*\.\d+|\d+\.?')
    def NUMBER(self, t):
        t.value = float(t.value)
        return t
    
    def error(self, t):
        print(f"Caracter Ilegal: '{t.value[0]}'")
        self.index += 1