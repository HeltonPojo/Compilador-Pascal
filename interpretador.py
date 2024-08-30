from sintatico import AnalisadorSintatico
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

            # Ignorar tokens não executáveis
            if operador in (17, 18, 19, 20, 21, 22, 23, 35, 36, 37, 38, 39, 40, 46):
                self.ponteiro += 1
                continue

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
            elif operador == 33:  # Caso específico para `write`
                self.chamada_sistema(instrucao)
            elif operador == 45:  # Tratamento para string literal
                self.tratar_string(instrucao) 
            elif operador == 34:  # Caso específico para `read`
                self.ler_entrada(instrucao)  
            elif operador == 30:  # Caso específico para `if`
                self.condicional(instrucao)        
            else:
                raise ValueError(f"Operador desconhecido: {operador}")

            self.ponteiro += 1
    def condicional(self, instrucao):
        condicao_var = instrucao[1]
        valor_condicao = self.variaveis.get(condicao_var, False)

        if valor_condicao:
            self.ponteiro += 1  # Executa a próxima instrução se a condição for verdadeira
        else:
            # Pula para a instrução depois do `else` ou fim do bloco `if`
            while self.ponteiro < len(self.instrucoes):
                self.ponteiro += 1
                proxima_instrucao = self.instrucoes[self.ponteiro]
                if proxima_instrucao[0] == 'LABEL' or proxima_instrucao[0] == 'JUMP':
                    break

    def ler_entrada(self, instrucao):
        var_name = instrucao[1]
        valor = input(f"Entrada para {var_name}: ")  # Solicita a entrada do usuário
        self.variaveis[var_name] = valor  # Armazena o valor na variável correspondente

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
    
    def tratar_string(self, instrucao):
        string_val = instrucao[1]
        print(string_val.strip("'"))  # Remove as aspas externas e imprime a string
    

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
        comando = instrucao[1]
        if comando == 'PRINT':
            valor = instrucao[2]
            if isinstance(valor, str) or instrucao[0] == 45:  # Verifica se é uma string literal
                print(valor.strip("'"))  # Imprime a string removendo as aspas externas
            else:
                print(self.variaveis.get(valor, valor))  # Imprime o valor da variável ou o valor diretamente
        elif comando == 'SCAN':
            var = instrucao[2]
            self.variaveis[var] = input()  # Lê entrada do usuário e armazena na variável


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