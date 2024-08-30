class AnalisadorSintatico:
    def __init__(self, lista):
        self.lista = lista
        self.index = -1
        self.tokensnome = {
            'if': 1, 'then': 2, 'else': 3, 'for': 4, 'do': 5, 'while': 6,
            'IDENT': 7, 'NUM': 8, 'STR': 9, '(': 10, ')': 11, ':=': 12, ';': 13,
            '=': 14, '<>': 15, '>': 16, '<': 17, '>=': 18, '<=': 19,
            'not': 20, 'or': 21, 'and': 22, 'begin': 23, 'end': 24,
        }
        self.gerador = GeradorDeLabelsETemporarias()

    def consome(self, token_esperado):
        self.index += 1
        lista_tupla = self.lista[self.index]
        if lista_tupla[0] == token_esperado:
            return
        else:
            raise Exception(f"ERRO NA LINHA: {lista_tupla}, TOKEN ESPERADO: {token_esperado}")

    def function(self):
        self.stmtList()

    def stmtList(self):
        prox_index = self.index + 1
        lista_tupla_prox = self.lista[prox_index]
        if lista_tupla_prox[0] in (
            self.tokensnome['interger'], self.tokensnome['for'], self.tokensnome['write'],
            self.tokensnome['read'], self.tokensnome['begin'], self.tokensnome['if'],
            self.tokensnome['IDENT'], self.tokensnome['while'], self.tokensnome[';']):
            self.stmt()
            self.restoStmtList()

    def restoStmtList(self):
        prox_index = self.index + 1
        lista_tupla_prox = self.lista[prox_index]
        if lista_tupla_prox[0] in (
            self.tokensnome['interger'], self.tokensnome['for'], self.tokensnome['write'],
            self.tokensnome['read'], self.tokensnome['begin'], self.tokensnome['if'],
            self.tokensnome['IDENT'], self.tokensnome['while'], self.tokensnome[';']):
            self.stmt()
            self.restoStmtList()

    def stmt(self):
        prox_index = self.index + 1
        lista_tupla_prox = self.lista[prox_index]
        if lista_tupla_prox[0] == self.tokensnome['for']:
            self.forStmt()
        elif lista_tupla_prox[0] == self.tokensnome['while']:
            self.whileStmt()
        elif lista_tupla_prox[0] == self.tokensnome['IDENT']:
            self.atribuicao()
        elif lista_tupla_prox[0] == self.tokensnome['write']:
            self.writeStmt()
        elif lista_tupla_prox[0] == self.tokensnome['read']:
            self.readStmt()
        elif lista_tupla_prox[0] == self.tokensnome['begin']:
            self.block()
        elif lista_tupla_prox[0] == self.tokensnome['if']:
            self.ifStmt()

    def ifStmt(self):
        self.consome(self.tokensnome['if'])
        self.expr()
        if self.lista[self.index + 1][0] != self.tokensnome['then']:
            raise Exception(f"ERRO: Esperado 'then' na linha {self.index + 1}")
        self.consome(self.tokensnome['then'])
        self.stmt()
        self.elsePart()

    def forStmt(self):
        self.consome(self.tokensnome['for'])
        inicializacao = self.lista[self.index + 1][1]
        self.consome(self.tokensnome['IDENT'])
        self.consome(self.tokensnome[':='])
        valor_inicial = self.lista[self.index + 1][1]
        self.consome(self.tokensnome['IDENT'])
        self.consome(self.tokensnome['to'])
        valor_final = self.lista[self.index + 1][1]
        self.consome(self.tokensnome['IDENT'])
        label_inicio = self.gerador.gerar_label()
        label_fim = self.gerador.gerar_label()
        self.lista_interpretador.append(('LABEL', label_inicio, None, None))
        self.lista_interpretador.append(('IF', ('<=', inicializacao, valor_final), label_fim, None))
        self.consome(self.tokensnome['do'])
        self.consome(self.tokensnome['begin'])
        while self.lista[self.index + 1][0] != self.tokensnome['end']:
            self.stmt()
            self.consome(self.tokensnome[';'])
        self.consome(self.tokensnome['end'])
        self.lista_interpretador.append(('JUMP', label_inicio, None, None))
        self.lista_interpretador.append(('LABEL', label_fim, None, None))

    def expr(self):
        self.exprFinalCorrecao()

    def orfunc(self):
        self.andfunc()
        while self.restoOr():
            pass

    def andfunc(self):
        self.notfunc()
        while self.restoAnd():
            pass

    def notfunc(self):
        prox_index = self.index + 1
        lista_tupla_prox = self.lista[prox_index]
        if lista_tupla_prox[0] == self.tokensnome['not']:
            self.consome(self.tokensnome['not'])
            self.restoNot()
        else:
            self.restoNot()

    def restoOr(self):
        prox_index = self.index + 1
        lista_tupla_prox = self.lista[prox_index]
        if lista_tupla_prox[0] == self.tokensnome['or']:
            self.consome(self.tokensnome['or'])
            self.andfunc()
            return True
        return False

    def restoAnd(self):
        prox_index = self.index + 1
        lista_tupla_prox = self.lista[prox_index]
        if lista_tupla_prox[0] == self.tokensnome['and']:
            self.consome(self.tokensnome['and'])
            self.notfunc()
            return True
        return False

    def restoNot(self):
        prox_index = self.index + 1
        lista_tupla_prox = self.lista[prox_index]
        if lista_tupla_prox[0] in (self.tokensnome['IDENT'], self.tokensnome['STR'], self.tokensnome['(']):
            self.consome(lista_tupla_prox[0])
        return False

# Gerador de Labels e Variáveis Temporárias

class GeradorDeLabelsETemporarias:
    def __init__(self):
        self.contador_labels = 0
        self.contador_temporarias = 0

    def gerar_label(self):
        label = f"L{self.contador_labels}"
        self.contador_labels += 1
        return label

    def gerar_temporaria(self):
        temp = f"TEMP{self.contador_temporarias}"
        self.contador_temporarias += 1
        return temp

# Definição do método corrigido para consumo completo da expressão

def exprFinalCorrecao(self):
    print(f"Iniciando expr na posição {self.index}")
    self.orfunc()  # Processa a expressão como um todo
    prox_index = self.index + 1
    lista_tupla_prox = self.lista[prox_index]
    print(f"Token após expr: {lista_tupla_prox}")
    
    # Processar operadores e garantir que a expressão seja completamente consumida
    while lista_tupla_prox[0] in (self.tokensnome['='], self.tokensnome['<>'], self.tokensnome['>'], 
                                  self.tokensnome['<'], self.tokensnome['>='], self.tokensnome['<=']):
        self.consome(lista_tupla_prox[0])
        print(f"Consumindo operador {lista_tupla_prox[0]} na posição {self.index}")
        # Após consumir o operador, garantir que o próximo token seja consumido
        prox_index = self.index + 1
        lista_tupla_prox = self.lista[prox_index]
        if lista_tupla_prox[0] in (self.tokensnome['IDENT'], self.tokensnome['STR'], self.tokensnome['(']):
            self.consome(lista_tupla_prox[0])
            print(f"Consumindo operando {lista_tupla_prox[0]} na posição {self.index}")
            prox_index = self.index + 1
            lista_tupla_prox = self.lista[prox_index]
            print(f"Token atualizado após consumir operador e operando: {lista_tupla_prox}")
        else:
            raise Exception(f"ERRO: Esperado operando na linha {prox_index + 1}, encontrado {lista_tupla_prox}")
        
    # Certificar que o próximo token após a expressão seja 'then'
    if lista_tupla_prox[0] == self.tokensnome['then']:
        self.consome(self.tokensnome['then'])
        print(f"Consumido 'then' na posição {self.index}")
    else:
        raise Exception(f"ERRO: Esperado 'then' na linha {prox_index + 1}, encontrado {lista_tupla_prox}")

# Substituição do método expr original pelo corrigido

setattr(AnalisadorSintatico, 'expr', exprFinalCorrecao)

# Código de teste, configuração e execução do analisador sintático
import sys

def testar_analisador_sintatico_com_detalhes(nome_arquivo):
    import lexico
    lista = lexico.main(nome_arquivo)
    sintatico_atualizado = AnalisadorSintatico(lista)
    try:
        sintatico_atualizado.function()
    except Exception as e:
        return str(e)
    return sintatico_atualizado.lista_interpretador
