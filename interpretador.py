import sys

class AnalisadorSintatico:
    def __init__(self, lista) -> None:
        self.tokensnome = {'+' : 1,
                '-': 2,
                '/': 3,
                '*': 4,
                'mod': 5,
                'div': 6,
                'or': 7,
                'and': 8,
                'not': 9,
                '==': 10,
                '<>': 11,
                '>': 12,
                '<': 13,
                '>=': 14,
                '<=': 15,
                ':=': 16,
                'program': 17,
                'var': 18,
                'interger': 19,
                'real': 20,
                'string': 21,
                'begin': 22,
                'end': 23,
                'for': 24,
                'to': 25,
                'while': 26,
                'do': 27,
                'break': 28,
                'continue': 29,
                'if': 30,
                'else': 31,
                'then': 32,
                'write': 33,
                'read': 34,
                ';': 35,
                ':': 36,
                ',': 37,
                '.': 38,
                '(': 39,
                ')': 40,
                '[': 41,
                ']': 42,
                '{': 43,
                '}': 44,
                'STR': 45,
                'IDENT': 46}
        self.index = -1
        self.lista = lista

    def consome(self, token_esperado):
        self.index += 1
        lista_tupla = self.lista[self.index]
        if lista_tupla[0] == token_esperado:
            return
        else:
            print('ERRO NA LINHA: ', lista_tupla)
            print('TOKEN ESPERADO: ', token_esperado)
            sys.exit()
            return

    #------------------------------------
    # funcao principal
    #------------------------------------

    def function(self):
        self.consome(self.tokensnome['program'])
        self.consome(self.tokensnome['IDENT'])
        self.consome(self.tokensnome[';'])
        self.declarations()
        self.consome(self.tokensnome['begin'])
        self.stmtList()
        self.consome(self.tokensnome['end'])
        self.consome(self.tokensnome['.'])
        print('passou sem erros')

    #------------------------------------
    # declaracoes de variaveis
    #------------------------------------

    def declarations(self):
        self.consome(self.tokensnome['var'])
        self.declaration()
        self.restoDeclaration()
        return

    def declaration(self):
        self.listaIdent()
        self.consome(self.tokensnome[':'])
        self.typefunc()
        self.consome(self.tokensnome[';'])
        return

    def listaIdent(self):
        self.consome(self.tokensnome['IDENT'])
        self.restoIdentList()    
        return

    def restoIdentList(self):
        prox_index = self.index + 1
        lista_tupla_prox = self.lista[prox_index]
        if(lista_tupla_prox[0] == self.tokensnome[',']):
            self.consome(self.tokensnome[','])
            self.consome(self.tokensnome['IDENT'])
            self.restoIdentList()
        else:
            return

    def restoDeclaration(self):
        prox_index = self.index + 1
        lista_tupla_prox = self.lista[prox_index]
        if(lista_tupla_prox[0] == self.tokensnome['IDENT']):
            self.declaration()
            self.restoDeclaration()
        else:
            return

    def typefunc(self):
        prox_index = self.index + 1
        lista_tupla_prox = self.lista[prox_index]
        if(lista_tupla_prox[0] == self.tokensnome['interger']):
            self.consome(self.tokensnome['interger'])
        elif(lista_tupla_prox[0] == self.tokensnome['real']):
            self.consome(self.tokensnome['real'])
        elif(lista_tupla_prox[0] == self.tokensnome['string']):
            self.consome(self.tokensnome['string'])
        else:
            print('ERRO NA LINHA: ', lista_tupla_prox)
            print('TOKENS ESPERADOS: interger real string')
            sys.exit()
            return
        return

    #------------------------------------
    # lista de instrucoes
    #------------------------------------

    def stmtList(self):
        self.statement()
        self.restoStmtList()
        return

    def restoStmtList(self):
        prox_index = self.index + 1
        lista_tupla_prox = self.lista[prox_index]
        if(lista_tupla_prox[0] == self.tokensnome[';']):
            self.consome(self.tokensnome[';'])
            self.statement()
            self.restoStmtList()
        else:
            return

    def statement(self):
        prox_index = self.index + 1
        lista_tupla_prox = self.lista[prox_index]
        if(lista_tupla_prox[0] == self.tokensnome['IDENT']):
            self.atribuicao()
        elif(lista_tupla_prox[0] == self.tokensnome['begin']):
            self.composto()
        elif(lista_tupla_prox[0] == self.tokensnome['if']):
            self.condicional()
        elif(lista_tupla_prox[0] == self.tokensnome['while']):
            self.repeticao()
        elif(lista_tupla_prox[0] == self.tokensnome['write']):
            self.escrita()
        elif(lista_tupla_prox[0] == self.tokensnome['read']):
            self.leitura()
        else:
            return

    def atribuicao(self):
        self.consome(self.tokensnome['IDENT'])
        self.consome(self.tokensnome[':='])
        self.expr()
        return

    def composto(self):
        self.consome(self.tokensnome['begin'])
        self.stmtList()
        self.consome(self.tokensnome['end'])
        return

    def condicional(self):
        self.consome(self.tokensnome['if'])
        self.expr()
        self.consome(self.tokensnome['then'])
        self.statement()
        self.restoIf()
        return

    def restoIf(self):
        prox_index = self.index + 1
        lista_tupla_prox = self.lista[prox_index]
        if(lista_tupla_prox[0] == self.tokensnome['else']):
            self.consome(self.tokensnome['else'])
            self.statement()
        else:
            return

    def repeticao(self):
        self.consome(self.tokensnome['while'])
        self.expr()
        self.consome(self.tokensnome['do'])
        self.statement()
        return

    def escrita(self):
        self.consome(self.tokensnome['write'])
        self.consome(self.tokensnome['('])
        self.expr()
        self.consome(self.tokensnome[')'])
        return

    def leitura(self):
        self.consome(self.tokensnome['read'])
        self.consome(self.tokensnome['('])
        self.consome(self.tokensnome['IDENT'])
        self.consome(self.tokensnome[')'])
        return

    def expr(self):
        self.simplesExpr()
        self.restoExpr()
        return

    def simplesExpr(self):
        self.termo()
        self.restoTermo()
        return

    def restoExpr(self):
        prox_index = self.index + 1
        lista_tupla_prox = self.lista[prox_index]
        if lista_tupla_prox[0] in [self.tokensnome['+'], self.tokensnome['-']]:
            self.consome(lista_tupla_prox[0])
            self.termo()
            self.restoExpr()
        else:
            return

    def restoTermo(self):
        prox_index = self.index + 1
        lista_tupla_prox = self.lista[prox_index]
        if lista_tupla_prox[0] in [self.tokensnome['*'], self.tokensnome['/'], self.tokensnome['mod'], self.tokensnome['div']]:
            self.consome(lista_tupla_prox[0])
            self.fator()
            self.restoTermo()
        else:
            return

    def termo(self):
        self.fator()
        self.restoFator()
        return

    def restoFator(self):
        prox_index = self.index + 1
        lista_tupla_prox = self.lista[prox_index]
        if lista_tupla_prox[0] in [self.tokensnome['*'], self.tokensnome['/']]:
            self.consome(lista_tupla_prox[0])
            self.fator()
            self.restoFator()
        else:
            return

    def fator(self):
        prox_index = self.index + 1
        lista_tupla_prox = self.lista[prox_index]
        if lista_tupla_prox[0] == self.tokensnome['(']:
            self.consome(self.tokensnome['('])
            self.expr()
            self.consome(self.tokensnome[')'])
        elif lista_tupla_prox[0] == self.tokensnome['IDENT']:
            self.consome(self.tokensnome['IDENT'])
        elif lista_tupla_prox[0] == self.tokensnome['NUM']:
            self.consome(self.tokensnome['NUM'])
        else:
            print('ERRO NA LINHA: ', lista_tupla_prox)
            print('TOKEN ESPERADO: ( IDENT NUM')
            sys.exit()
            return

# Classe Interpretador adicionada ao final do arquivo
class Interpretador:
    def __init__(self):
        self.variaveis = {}
        self.labels = {}
        self.programa = []
        self.ponteiro = 0

    def carregar_programa(self, programa):
        self.programa = programa
        self.identificar_labels()

    def identificar_labels(self):
        for i, instrucao in enumerate(self.programa):
            if instrucao[0] == "LABEL":
                self.labels[instrucao[1]] = i

    def executar(self):
        while self.ponteiro < len(self.programa):
            instrucao = self.programa[self.ponteiro]
            self.executar_instrucao(instrucao)
            self.ponteiro += 1

    def executar_instrucao(self, instrucao):
        operador = instrucao[0]
        if operador in ("+", "-", "*", "/", "%", "//"):
            self.operacao_aritmetica(instrucao)
        elif operador in ("||", "&&", "!", "==", "<>", ">", ">=", "<", "<="):
            self.operacao_logica(instrucao)
        elif operador == "=":
            self.atribuicao(instrucao)
        elif operador == "IF":
            self.condicional(instrucao)
        elif operador == "JUMP":
            self.jump(instrucao)
        elif operador == "CALL":
            self.chamada_sistema(instrucao)
        elif operador == "LABEL":
            pass  # Labels são processadas na identificação
        else:
            raise ValueError(f"Operador desconhecido: {operador}")

    def operacao_aritmetica(self, instrucao):
        operador, guardar, operando1, operando2 = instrucao
        if operando2 is None:
            valor = self.obter_valor(operando1)
            if operador == "+":
                resultado = valor
            elif operador == "-":
                resultado = -valor
        else:
            valor1 = self.obter_valor(operando1)
            valor2 = self.obter_valor(operando2)
            if operador == "+":
                resultado = valor1 + valor2
            elif operador == "-":
                resultado = valor1 - valor2
            elif operador == "*":
                resultado = valor1 * valor2
            elif operador == "/":
                resultado = valor1 / valor2
            elif operador == "%":
                resultado = valor1 % valor2
            elif operador == "//":
                resultado = valor1 // valor2
        self.variaveis[guardar] = resultado

    def operacao_logica(self, instrucao):
        operador, guardar, operando1, operando2 = instrucao
        valor1 = self.obter_valor(operando1)
        valor2 = self.obter_valor(operando2) if operando2 is not None else None
        if operador == "||":
            resultado = valor1 or valor2
        elif operador == "&&":
            resultado = valor1 and valor2
        elif operador == "!":
            resultado = not valor1
        elif operador == "==":
            resultado = valor1 == valor2
        elif operador == "<>":
            resultado = valor1 != valor2
        elif operador == ">":
            resultado = valor1 > valor2
        elif operador == ">=":
            resultado = valor1 >= valor2
        elif operador == "<":
            resultado = valor1 < valor2
        elif operador == "<=":
            resultado = valor1 <= valor2
        self.variaveis[guardar] = resultado

    def atribuicao(self, instrucao):
        _, guardar, operando1, _ = instrucao
        self.variaveis[guardar] = self.obter_valor(operando1)

    def condicional(self, instrucao):
        _, condicao, label1, label2 = instrucao
        if self.obter_valor(condicao):
            self.ponteiro = self.labels[label1] - 1
        else:
            self.ponteiro = self.labels[label2] - 1

    def jump(self, instrucao):
        _, label, _, _ = instrucao
        self.ponteiro = self.labels[label] - 1

    def chamada_sistema(self, instrucao):
        _, comando, valor, _ = instrucao
        if comando == "PRINT":
            print(self.obter_valor(valor))
        elif comando == "SCAN":
            self.variaveis[valor] = input("Input: ")

    def obter_valor(self, operando):
        if isinstance(operando, (int, float)):
            return operando
        return self.variaveis.get(operando, 0)
