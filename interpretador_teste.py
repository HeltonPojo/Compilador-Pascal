from sintatico import AnalisadorSintatico

class Interpretador:
    def __init__(self):
        self.variaveis = {}
        self.labels = {}
        self.ponteiro = 0

    def carregar_labels(self, instrucoes):
        for i, instrucao in enumerate(instrucoes):
            if instrucao[0].lower() == 'label':
                self.labels[instrucao[1]] = i


    def jump_if_false(self, instrucao):
        _, label, condicao, _ = instrucao
        if not condicao:
            self.ponteiro = self.labels[label]
        else:
            self.ponteiro += 1            

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
            elif operador == 'JUMP_IF_FALSE':
                self.jump_if_false(instrucao)    
            elif operador == 'CALL':
                self.chamada_sistema(instrucao)
            elif operador == 'DECLARATION':
                self.declaracao(instrucao)
            elif operador == 'LABEL':
                pass
            elif operador in ('program', 'var', 'begin', 'end', ';'):
                # Ignorar tokens de estrutura de programa que não são executáveis
                pass
            else:
                raise ValueError(f"Operador desconhecido: {operador}")
            self.ponteiro += 1

    def operacao_aritmetica(self, instrucao):
        operador, guardar, operando1, operando2 = instrucao
        numero1 = self.variaveis.get(operando1, 0) if operando1 is not None else 0
        numero2 = self.variaveis.get(operando2, 0) if operando2 is not None else 0
        
        if operador == '+':
            self.variaveis[guardar] = numero1 + numero2
        elif operador == '-':
            self.variaveis[guardar] = numero1 - numero2
        elif operador == '*':
            self.variaveis[guardar] = numero1 * numero2
        elif operador == '/':
            self.variaveis[guardar] = numero1 / numero2
        elif operador == '%':
            self.variaveis[guardar] = numero1 % numero2
        elif operador == '//':
            self.variaveis[guardar] = numero1 // numero2
        # Suporte para operadores unários
        elif operador == '+' and operando2 is None:
            self.variaveis[guardar] = +numero1
        elif operador == '-' and operando2 is None:
            self.variaveis[guardar] = -numero1


    def operacao_logica(self, instrucao):
        operador, guardar, operando1, operando2 = instrucao
        if operador == '||':
            self.variaveis[guardar] = self.variaveis.get(operando1, False) or self.variaveis.get(operando2, False)
        elif operador == '&&':
            self.variaveis[guardar] = self.variaveis.get(operando1, False) and self.variaveis.get(operando2, False)
        elif operador == '!':
            self.variaveis[guardar] = not self.variaveis.get(operando1, False)


    def operacao_relacional(self, instrucao):
        operador, guardar, operando1, operando2 = instrucao
        numero1 = self.variaveis.get(operando1, 0)
        numero2 = self.variaveis.get(operando2, 0)

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
        _, variavel, valor = instrucao
        self.variaveis[variavel] = valor

    def condicional(self, instrucao):
        _, condicao, label1, label2 = instrucao
        if self.variaveis.get(condicao, False):
            self.ponteiro = self.labels[label1]
        else:
            self.ponteiro = self.labels[label2]

    def jump(self, instrucao):
        if len(instrucao) == 2:
            _, label = instrucao
        elif len(instrucao) >= 3:  # Para cobrir o caso de ter mais elementos na instrução
            _, label, *_ = instrucao  # Usa *_ para ignorar elementos extras
        
        if label in self.labels:
            self.ponteiro = self.labels[label]
        else:
            raise ValueError(f"Label '{label}' não encontrada nas labels: {self.labels}")




    def chamada_sistema(self, instrucao):
        operador, comando, valor, _ = instrucao
        if comando == 'PRINT':
            print(self.variaveis.get(valor, valor))
        elif comando == 'SCAN':
            self.variaveis[valor] = input()

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
        
if __name__ == "__main__":
    import lexico, sys
    if len(sys.argv) > 1:
        lista = lexico.main(sys.argv[1])
        AnSint = AnalisadorSintatico(lista)
        listaDoInterpretador = AnSint.function()
        # Carregar e executar o interpretador
        interpretador = Interpretador()
        interpretador.carregar_labels(listaDoInterpretador)
        interpretador.executar(listaDoInterpretador)