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
                pass  # Labels são processados na inicialização
            else:
                raise ValueError(f"Operador desconhecido: {operador}")
            self.ponteiro += 1

    def operacao_aritmetica(self, instrucao):
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
        operador, guardar, operando1, operando2 = instrucao
        if operador == 'or':
            self.variaveis[guardar] = self.variaveis.get(operando1, False) or self.variaveis.get(operando2, False)
        elif operador == 'and':
            self.variaveis[guardar] = self.variaveis.get(operando1, False) and self.variaveis.get(operando2, False)
        elif operador == 'not':
            self.variaveis[guardar] = not self.variaveis.get(operando1, False)

    def operacao_relacional(self, instrucao):
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
        _, guardar, operando1, _ = instrucao
        self.variaveis[guardar] = self.variaveis.get(operando1, 0)

    def condicional(self, instrucao):
        _, condicao, label1, label2 = instrucao
        if self.variaveis.get(condicao, False):
            self.ponteiro = self.labels[label1] - 1
        else:
            self.ponteiro = self.labels[label2] - 1

    def jump(self, instrucao):
        _, label, _, _ = instrucao
        self.ponteiro = self.labels[label] - 1

    def chamada_sistema(self, instrucao):
        _, comando, valor, _ = instrucao
        if comando == 'PRINT':
            print(valor)
        elif comando == 'SCAN':
            self.variaveis[valor] = input()

if __name__ == "__main__":
    import lexico, sys
    if len(sys.argv) > 1:
        lista = lexico.main(sys.argv[1])
        AnSint = AnalisadorSintatico(lista)
        AnSint.function()

        # Carregar e executar o interpretador
        interpretador = Interpretador()
        interpretador.carregar_labels(lista)
        interpretador.executar(lista)
