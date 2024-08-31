import logging
from sintatico import AnalisadorSintatico

# Configuração de logging para ajudar na depuração
#logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')

class Interpretador:
    def __init__(self):
        # Inicializa as variáveis e labels
        self.variaveis = {}  # Dicionário para armazenar variáveis e seus valores
        self.labels = {}     # Dicionário para armazenar labels e suas posições na lista de instruções
        self.ponteiro = 0    # Ponteiro para controlar a posição atual na lista de instruções

    def carregar_labels(self, instrucoes):
        for i, instrucao in enumerate(instrucoes):
            if instrucao[0].startswith('LABEL'):
                self.labels[instrucao[1]] = i



    def jump(self, instrucao):
        if len(instrucao) == 2:
            _, label = instrucao
        elif len(instrucao) >= 3:
            _, label, *_ = instrucao
        
        if label in self.labels:
            self.ponteiro = self.labels[label]
        else:
            raise ValueError(f"Label '{label}' não encontrada nas labels: {self.labels}")

    def jump_if_false(self, instrucao):
        # Realiza o salto condicional para a posição da label se a condição for falsa
        _, label, condicao, _ = instrucao
        if not self.avaliar_condicao(condicao):
            self.jump(('JUMP', label))
        else:
            self.ponteiro += 1

    def executar(self, instrucoes):
        self.carregar_labels(instrucoes)  # Adiciona a carga de labels antes de executar as instruções
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
            elif operador == 'JUMP_IF_FALSE':
                self.jump_if_false(instrucao)
            elif operador == 'CALL':
                self.chamada_sistema(instrucao)
            elif operador == 'DECLARATION':
                self.declaracao(instrucao)
            elif operador == 'LABEL':
                pass
            elif operador in ('program', 'var', 'begin', 'end', ';'):
                pass
            else:
                raise ValueError(f"Operador desconhecido: {operador}")
            self.ponteiro += 1


    def operacao_aritmetica(self, instrucao):
        # Realiza operações aritméticas como +, -, *, /, MOD e DIV
        operador, guardar, operando1, operando2 = instrucao
        numero1 = self.obter_valor(operando1)
        numero2 = self.obter_valor(operando2)
        
        if operador == '+':
            resultado = numero1 + numero2
        elif operador == '-':
            resultado = numero1 - numero2
        elif operador == '*':
            resultado = numero1 * numero2
        elif operador == '/':
            if numero2 == 0:
                raise ZeroDivisionError("Divisão por zero.")
            resultado = numero1 / numero2
        elif operador == '%':
            if numero2 == 0:
                raise ZeroDivisionError("Divisão por zero.")
            resultado = numero1 % numero2
        elif operador == '//':
            if numero2 == 0:
                raise ZeroDivisionError("Divisão por zero.")
            resultado = numero1 // numero2
        elif operador == '+' and operando2 is None:
            resultado = +numero1
        elif operador == '-' and operando2 is None:
            resultado = -numero1
        else:
            raise ValueError(f"Operador aritmético desconhecido: {operador}")
        
        # Armazena o resultado na variável especificada
        self.variaveis[guardar] = resultado
        logging.debug(f"Variável '{guardar}' atribuída com o resultado: {resultado}.")

    def operacao_logica(self, instrucao):
        # Realiza operações lógicas como ||, &&, !
        operador, guardar, operando1, operando2 = instrucao
        valor1 = self.obter_valor(operando1)
        valor2 = self.obter_valor(operando2)
        
        if operador == '||':
            resultado = valor1 or valor2
        elif operador == '&&':
            resultado = valor1 and valor2
        elif operador == '!':
            resultado = not valor1
        else:
            raise ValueError(f"Operador lógico desconhecido: {operador}")

        # Armazena o resultado na variável especificada
        self.variaveis[guardar] = resultado
        logging.debug(f"Variável '{guardar}' atribuída com o resultado: {resultado}.")

    def operacao_relacional(self, instrucao):
        # Realiza operações relacionais como ==, <>, >, <, >=, <=
        operador, guardar, operando1, operando2 = instrucao
        valor1 = self.obter_valor(operando1)
        valor2 = self.obter_valor(operando2)

        if operador == '==':
            resultado = valor1 == valor2
        elif operador == '<>':
            resultado = valor1 != valor2
        elif operador == '>':
            resultado = valor1 > valor2
        elif operador == '<':
            resultado = valor1 < valor2
        elif operador == '>=':
            resultado = valor1 >= valor2
        elif operador == '<=':
            resultado = valor1 <= valor2
        else:
            raise ValueError(f"Operador relacional desconhecido: {operador}")

        # Armazena o resultado na variável especificada
        self.variaveis[guardar] = resultado
        logging.debug(f"Variável '{guardar}' atribuída com o resultado: {resultado}.")

    def atribuicao(self, instrucao):
        # Atribui um valor a uma variável
        _, variavel, valor = instrucao
        self.variaveis[variavel] = self.obter_valor(valor)
        logging.debug(f"Variável '{variavel}' atribuída com o valor: {self.variaveis[variavel]}.")

    def condicional(self, instrucao):
        # Realiza a operação condicional IF
        _, condicao, label1, label2 = instrucao
        if label1 not in self.labels or label2 not in self.labels:
            raise ValueError("Uma ou ambas as labels não foram encontradas.")
        if self.avaliar_condicao(condicao):
            self.jump(('JUMP', label1))
        else:
            self.jump(('JUMP', label2))

    def chamada_sistema(self, instrucao):
        # Realiza chamadas de sistema como PRINT e SCAN
        _, comando, valor, _ = instrucao
        if comando == 'PRINT':
            # Verifica se o valor a ser impresso é uma variável ou uma string literal
            if valor in self.variaveis:
                print(self.variaveis[valor])  # Imprime o valor da variável
                
            else:
                print(valor)  # Imprime a string literal diretamente
        elif comando == 'SCAN':
            entrada = input()  # Lê entrada do usuário
            self.variaveis[valor] = self.converter_tipo(entrada)
            logging.debug(f"Entrada do usuário armazenada em '{valor}': {self.variaveis[valor]}")

    def declaracao(self, instrucao):
        # Declara uma variável com um tipo específico
        _, variavel, tipo = instrucao
        if tipo == 'integer':
            self.variaveis[variavel] = 0
        elif tipo == 'real':
            self.variaveis[variavel] = 0.0
        elif tipo == 'string':
            self.variaveis[variavel] = ""
        else:
            raise ValueError(f"Tipo de variável desconhecido: {tipo}")
        logging.debug(f"Variável '{variavel}' declarada como '{tipo}'.")

    def obter_valor(self, operando):
        # Obtém o valor de um operando, seja ele um literal ou uma variável
        if isinstance(operando, (int, float)):
            return operando
        return self.variaveis.get(operando, 0)

    def avaliar_condicao(self, condicao):
        # Avalia uma condição para determinar se é verdadeira ou falsa
        return bool(self.obter_valor(condicao))

    def converter_tipo(self, entrada):
        # Converte a entrada para o tipo apropriado (inteiro, float ou string)
        try:
            if '.' in entrada:
                return float(entrada)
            return int(entrada)
        except ValueError:
            return entrada

if __name__ == "__main__":
    import lexico, sys
    if len(sys.argv) > 1:
        lista = lexico.main(sys.argv[1])
        AnSint = AnalisadorSintatico(lista)
        listaDoInterpretador = AnSint.function()
        interpretador = Interpretador()
        interpretador.carregar_labels(listaDoInterpretador)
        interpretador.executar(listaDoInterpretador)