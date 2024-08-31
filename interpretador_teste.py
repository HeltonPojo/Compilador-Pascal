import logging
from sintatico import AnalisadorSintatico

# Configuração de logging
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')

class Interpretador:
    def __init__(self):
        self.variaveis = {}
        self.labels = {}
        self.ponteiro = 0

    def carregar_labels(self, instrucoes):
        for i, instrucao in enumerate(instrucoes):
            if instrucao[0] == 'LABEL':
                self.labels[instrucao[1]] = i
                logging.debug(f"Label '{instrucao[1]}' carregada na posição {i}.")
        logging.info("Todas as labels foram carregadas.")

    def jump(self, instrucao):
        _, label = instrucao
        if label in self.labels:
            self.ponteiro = self.labels[label]
            logging.debug(f"Jump para label '{label}' na posição {self.ponteiro}.")
        else:
            raise ValueError(f"Label '{label}' não encontrada.")

    def jump_if_false(self, instrucao):
        _, label, condicao, _ = instrucao
        if not self.avaliar_condicao(condicao):
            self.jump(('JUMP', label))
        else:
            self.ponteiro += 1            

    def executar(self, instrucoes):
        while self.ponteiro < len(instrucoes):
            instrucao = instrucoes[self.ponteiro]
            operador = instrucao[0].upper()
            logging.info(f"Executando instrução: {instrucao} na posição {self.ponteiro}.")
            
            if operador in ('+', '-', '*', '/', 'MOD', 'DIV'):
                self.operacao_aritmetica(instrucao)
            elif operador in ('||', '&&', '!'):
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
                pass  # Ignorar, já processado
            elif operador in ('PROGRAM', 'VAR', 'BEGIN', 'END', ';'):
                pass  # Ignorar tokens de estrutura de programa
            else:
                raise ValueError(f"Operador desconhecido: {operador}")
            self.ponteiro += 1

    def operacao_aritmetica(self, instrucao):
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
        
        self.variaveis[guardar] = resultado
        logging.debug(f"Variável '{guardar}' atribuída com o resultado: {resultado}.")

    def operacao_logica(self, instrucao):
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

        self.variaveis[guardar] = resultado
        logging.debug(f"Variável '{guardar}' atribuída com o resultado: {resultado}.")

    def operacao_relacional(self, instrucao):
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

        self.variaveis[guardar] = resultado
        logging.debug(f"Variável '{guardar}' atribuída com o resultado: {resultado}.")

    def atribuicao(self, instrucao):
        _, variavel, valor = instrucao
        self.variaveis[variavel] = self.obter_valor(valor)
        logging.debug(f"Variável '{variavel}' atribuída com o valor: {self.variaveis[variavel]}.")

    def condicional(self, instrucao):
        _, condicao, label1, label2 = instrucao
        if label1 not in self.labels or label2 not in self.labels:
            raise ValueError("Uma ou ambas as labels não foram encontradas.")
        if self.avaliar_condicao(condicao):
            self.jump(('JUMP', label1))
        else:
            self.jump(('JUMP', label2))

    def chamada_sistema(self, instrucao):
        _, comando, valor, _ = instrucao
        if comando == 'PRINT':
            print(self.obter_valor(valor))
        elif comando == 'SCAN':
            entrada = input()
            self.variaveis[valor] = self.converter_tipo(entrada)
            logging.debug(f"Entrada do usuário armazenada em '{valor}': {self.variaveis[valor]}")

    def declaracao(self, instrucao):
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
        if isinstance(operando, (int, float)):
            return operando
        return self.variaveis.get(operando, 0)

    def avaliar_condicao(self, condicao):
        return bool(self.obter_valor(condicao))

    def converter_tipo(self, entrada):
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
