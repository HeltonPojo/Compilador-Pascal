from sintatico import AnalisadorSintatico
from os import sys

# interpretador.py
# Este arquivo implementa o interpretador que executa o código intermediário gerado pelo analisador sintático.
# A classe Interpretador carrega e executa as instruções (tuplas) geradas pelo analisador sintático.
# As operações aritméticas, lógicas, e de controle de fluxo são processadas e executadas por este interpretador.

class Interpretador:
    # Construtor da classe. Inicializa o dicionário de variáveis, labels e o ponteiro de execução.
    def __init__(self):
        self.variaveis = {}  # Dicionário que armazena os valores das variáveis
        self.labels = {}  # Dicionário que mapeia labels para posições no código intermediário
        self.ponteiro = 0  # Ponteiro que indica a instrução atual sendo executada

    # Carrega labels a partir da lista de instruções para facilitar o controle de fluxo.
    def carregar_labels(self, instrucoes):
        for i, instrucao in enumerate(instrucoes):
            if instrucao[0] == 'LABEL':
                self.labels[instrucao[1]] = i  # Armazena a posição da label no dicionário

    # Executa a lista de instruções
    def executar(self, instrucoes):
         # Executa a lista de instruções uma a uma.
        while self.ponteiro < len(instrucoes):  # Continua executando enquanto houver instruções
            instrucao = instrucoes[self.ponteiro]  # Obtém a instrução atual
            operador = instrucao[0]  # Obtém o operador da instrução

            # Verifica qual operação deve ser executada
            if operador in ('+', '-', '*', '/', 'mod', 'div'):
                self.operacao_aritmetica(instrucao)
            elif operador in ('or', 'and', 'not'):
                self.operacao_logica(instrucao)
            elif operador in ('==', '<>', '>', '<', '>=', '<='):
                self.operacao_relacional(instrucao)
            elif operador == 'JUMP':
                self.jump(instrucao[1])
            elif operador == 'IF_FALSE':
                self.if_false(instrucao[1], instrucao[2])
            elif operador == '=':
                self.atribuicao(instrucao)
            elif operador == 'CALL':
                self.chamada(instrucao)
            elif operador == 'LABEL':
                pass  # Labels não fazem nada durante a execução
            self.ponteiro += 1  # Avança para a próxima instrução

    # Função que executa operações aritméticas
    def operacao_aritmetica(self, instrucao):
        op1 = self.obter_valor(instrucao[2])
        op2 = self.obter_valor(instrucao[3])
        resultado = eval(f"{op1} {instrucao[0]} {op2}")
        self.variaveis[instrucao[1]] = resultado

    # Função que executa operações lógicas
    def operacao_logica(self, instrucao):
        op1 = self.obter_valor(instrucao[2])
        op2 = self.obter_valor(instrucao[3]) if len(instrucao) > 3 else None
        if instrucao[0] == 'or':
            resultado = op1 or op2
        elif instrucao[0] == 'and':
            resultado = op1 and op2
        elif instrucao[0] == 'not':
            resultado = not op1
        self.variaveis[instrucao[1]] = resultado

    # Função que executa operações relacionais
    def operacao_relacional(self, instrucao):
        op1 = self.obter_valor(instrucao[2])
        op2 = self.obter_valor(instrucao[3])
        resultado = eval(f"{op1} {instrucao[0]} {op2}")
        self.variaveis[instrucao[1]] = resultado

    # Função que realiza a atribuição de valores a variáveis
    def atribuicao(self, instrucao):
        self.variaveis[instrucao[1]] = self.obter_valor(instrucao[2])

    # Função que executa chamadas de funções ou procedimentos
    def chamada(self, instrucao):
        if instrucao[1] == 'SCAN':
            self.variaveis[instrucao[2]] = input(f"Entrada ({instrucao[2]}): ")
        elif instrucao[1] == 'PRINT':
            print(self.obter_valor(instrucao[2]))

    # Função que realiza saltos incondicionais
    def jump(self, label):
        self.ponteiro = self.labels[label] - 1

    # Função que realiza saltos condicionais
    def if_false(self, condicao, label):
        if not self.obter_valor(condicao):
            self.jump(label)

    # Função auxiliar para obter o valor de uma variável ou retornar o valor diretamente
    def obter_valor(self, valor):
        return self.variaveis.get(valor, valor)

class Interpretador:
    def __init__(self):
        self.variaveis = {}
        self.labels = {}
        self.ponteiro = 0

    def carregar_labels(self, instrucoes):
        for i, instrucao in enumerate(instrucoes):
            if instrucao[0] == 'LABEL':
                self.labels[instrucao[1]] = i

    def executar(self, instrucoes):
        while self.ponteiro < len(instrucoes):
            instrucao = instrucoes[self.ponteiro]
            operador = instrucao[0]
            if operador in ('+', '-', '*', '/', 'mod', 'div'):
                self.operacao_aritmetica(instrucao)
            elif operador in ('or', 'and', 'not'):
                self.operacao_logica(instrucao)
            elif operador in ('==', '<>', '>', '<', '>=', '<='):
                self.operacao_relacional(instrucao)
            elif operador == ':=':
                self.atribuicao(instrucao)
            elif operador == 'IF':
                self.condicional(instrucao)
            elif operador == 'JUMP':
                self.jump(instrucao)
            elif operador == 'CALL':
                self.chamada_sistema(instrucao)
            elif operador == 'LABEL':
                pass
            else:
                raise ValueError(f"Operador desconhecido: {operador}")
            self.ponteiro += 1

    def operacao_aritmetica(self, instrucao):
        # Realiza operações aritméticas como +, -, *, /.
        operador, guardar, operando1, operando2 = instrucao
        numero1 = 0
        numero2 = 0
        if type(operando1) == type(2):
            numero1 = operando1
        else:
            numero1 = float(self.variaveis.get(operando1, 0))
        if type(operando2) == type(2):
            numero2 = operando2
        else:
            numero2 = float(self.variaveis.get(operando2, 0))

        if operador == '+':
            self.variaveis[guardar] = numero1 + numero2
        elif operador == '-':
            self.variaveis[guardar] = numero1 - numero2
        elif operador == '*':
            self.variaveis[guardar] = numero1 * numero2
        elif operador == '/':
            self.variaveis[guardar] = numero1 / numero2
        elif operador == 'mod':
            self.variaveis[guardar] = numero1 % numero2
        elif operador == 'div':
            self.variaveis[guardar] = numero1 // numero2

    def operacao_logica(self, instrucao):
        # Realiza operações lógicas como AND, OR, NOT.
        operador, guardar, operando1, operando2 = instrucao
        if operador == 'or':
            self.variaveis[guardar] = self.variaveis.get(operando1, False) or self.variaveis.get(operando2, False)
        elif operador == 'and':
            self.variaveis[guardar] = self.variaveis.get(operando1, False) and self.variaveis.get(operando2, False)
        elif operador == 'not':
            self.variaveis[guardar] = not self.variaveis.get(operando1, False)

    def operacao_relacional(self, instrucao):
        # Realiza comparações como ==, >, <, etc.
        operador, guardar, operando1, operando2 = instrucao
        numero1 = 0
        numero2 = 0
        if type(operando1) == type(2):
            numero1 = operando1
        else:
            numero1 = float(self.variaveis.get(operando1, 0))
        if type(operando2) == type(2):
            numero2 = operando2
        else:
            numero2 = float(self.variaveis.get(operando2, 0))

        if operador == '==':
            self.variaveis[guardar] = numero1 == numero2
        elif operador == '<>':
            self.variaveis[guardar] = numero1 != numero2
        elif operador == '>':
            self.variaveis[guardar] = numero1 > numero2
        elif operador == '<':
            self.variaveis[guardar] = numero1 < numero2
        elif operador == '>=':
            self.variaveis[guardar] = numero1 >= numero2
        elif operador == '<=':
            self.variaveis[guardar] = numero1 <= numero2

    def atribuicao(self, instrucao):
        # Atribui valores a variáveis.
        _, guardar, operando1, _ = instrucao
        self.variaveis[guardar] = self.variaveis.get(operando1, 0)

    def condicional(self, instrucao):
        # Processa a instrução IF-THEN.
        _, condicao, label1, label2 = instrucao
        if self.variaveis.get(condicao, False):
            self.ponteiro = self.labels[label1] - 1
        else:
            self.ponteiro = self.labels[label2] - 1

    def jump(self, instrucao):
        # Realiza um salto incondicional para um label.
        _, label, _, _ = instrucao
        self.ponteiro = self.labels[label] - 1

    def chamada_sistema(self, instrucao):
                # Realiza chamadas de sistema como leitura e escrita.
        _, comando, valor, variavel = instrucao
        if comando == 'PRINT':
            palavra = ''
            if type(variavel) == type('a'):
                print(self.variaveis.get(variavel, 'Variavel não atribuida'))
            else:
                print(valor)
        elif comando == 'SCAN':
            self.variaveis[valor] = input()

if __name__ == "__main__":
    import lexico
    if len(sys.argv) > 1:
        lista = lexico.main(sys.argv[1])
        AnSint = AnalisadorSintatico(lista)
        AnSint.function()

        # Carregar e executar o interpretador
        interpretador = Interpretador()
        interpretador.carregar_labels(lista)
        interpretador.executar(lista)
