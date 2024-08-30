class AnalisadorSintatico:
    def __init__(self, lista):  
        # Inicializa o analisador sintático com uma lista de tokens.
        self.lista = lista
        self.index = -1  # Define o índice atual para -1 (indica que nenhum token foi processado ainda).
        self.tokensnome = {  # Mapeamento de tokens para seus respectivos códigos numéricos.
            '+' : 1,
            '-' : 2,
            '/' : 3,
            '*' : 4,
            'mod' : 5,
            'div' : 6,
            'or' : 7,
            'and' : 8,
            'not' : 9,
            '==' : 10,
            '<>' : 11,
            '>' : 12,
            '<' : 13,
            '>=' : 14,
            '<=' : 15,
            ':=' : 16,
            'program' : 17,
            'var' : 18,
            'integer' : 19,  # Corrigido para "integer"
            'real' : 20,
            'string' : 21,
            'begin' : 22,
            'end' : 23,
            'for' : 24,
            'to' : 25,
            'while' : 26,
            'do' : 27,
            'break' : 28,
            'continue' : 29,
            'if' : 30,
            'else' : 31,
            'then' : 32,
            'write' : 33,
            'read' : 34,
            ';' : 35,
            ':' : 36,
            ',' : 37,
            '.' : 38,
            '(' : 39,
            ')' : 40,
            '[' : 41,
            ']' : 42,
            '{' : 43,
            '}' : 44,
            'STR' : 45,  # Literal de string
            'IDENT' : 46  # Identificadores (ex.: nomes de variáveis)
        }
        
        self.gerador = GeradorDeLabelsETemporarias()  # Instancia o gerador de labels e temporários.

    def consome(self, token_esperado):
        # Avança para o próximo token na lista e verifica se é o token esperado.
        self.index += 1  # Avança o índice.
        lista_tupla = self.lista[self.index]  # Obtém o token atual.
        if lista_tupla[0] == token_esperado:
            return  # Se o token for o esperado, a função retorna sem erro.
        else:
            # Se o token não for o esperado, gera uma exceção.
            raise Exception(f"ERRO NA LINHA: {lista_tupla}, TOKEN ESPERADO: {token_esperado}")
        
    def function(self):
        # Inicia a análise sintática a partir do método stmtList.
        self.stmtList()

    def stmtList(self):
        # Analisa uma lista de declarações.
        prox_index = self.index + 1  # Determina o próximo índice a ser analisado.
        lista_tupla_prox = self.lista[prox_index]  # Obtém o próximo token.
        if lista_tupla_prox[0] in (
            self.tokensnome['integer'], self.tokensnome['for'], self.tokensnome['write'],
            self.tokensnome['read'], self.tokensnome['begin'], self.tokensnome['if'],
            self.tokensnome['IDENT'], self.tokensnome['while'], self.tokensnome[';']):
            # Se o token pertence a um dos tokens esperados, analisa a declaração e continua a análise.
            self.stmt()
            self.restoStmtList()

    def restoStmtList(self):
        # Analisa o restante da lista de declarações.
        prox_index = self.index + 1  # Próximo índice.
        lista_tupla_prox = self.lista[prox_index]  # Próximo token.
        if lista_tupla_prox[0] in (
            self.tokensnome['integer'], self.tokensnome['for'], self.tokensnome['write'],
            self.tokensnome['read'], self.tokensnome['begin'], self.tokensnome['if'],
            self.tokensnome['IDENT'], self.tokensnome['while'], self.tokensnome[';']):
            # Continua analisando se o token pertence a um dos tokens esperados.
            self.stmt()
            self.restoStmtList()

    def stmt(self):
        # Analisa uma declaração específica, chamando o método apropriado para cada tipo de declaração.
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
        # Analisa uma declaração condicional (if).
        self.consome(self.tokensnome['if'])  # Consome o token 'if'.
        self.expr()  # Analisa a expressão condicional.
        if self.lista[self.index + 1][0] != self.tokensnome['then']:
            # Verifica se o próximo token é 'then'; se não, lança uma exceção.
            raise Exception(f"ERRO: Esperado 'then' na linha {self.index + 1}")
        self.consome(self.tokensnome['then'])  # Consome o token 'then'.
        self.stmt()  # Analisa a declaração associada ao 'if'.
        self.elsePart()  # Analisa a parte 'else', se existir.

    def forStmt(self):
        # Analisa uma declaração de loop 'for'.
        self.consome(self.tokensnome['for'])  # Consome o token 'for'.
        inicializacao = self.lista[self.index + 1][1]  # Pega o identificador da variável de inicialização.
        self.consome(self.tokensnome['IDENT'])  # Consome o identificador.
        self.consome(self.tokensnome[':='])  # Consome o operador de atribuição ':='.
        valor_inicial = self.lista[self.index + 1][1]  # Pega o valor inicial da variável de loop.
        self.consome(self.tokensnome['IDENT'])  # Consome o identificador.
        self.consome(self.tokensnome['to'])  # Consome o token 'to'.
        valor_final = self.lista[self.index + 1][1]  # Pega o valor final do loop.
        self.consome(self.tokensnome['IDENT'])  # Consome o identificador.
        label_inicio = self.gerador.gerar_label()  # Gera um label para o início do loop.
        label_fim = self.gerador.gerar_label()  # Gera um label para o fim do loop.
        self.lista_interpretador.append(('LABEL', label_inicio, None, None))  # Adiciona o label de início ao código intermediário.
        self.lista_interpretador.append(('IF', ('<=', inicializacao, valor_final), label_fim, None))  # Adiciona a condição do loop.
        self.consome(self.tokensnome['do'])  # Consome o token 'do'.
        self.consome(self.tokensnome['begin'])  # Consome o token 'begin'.
        while self.lista[self.index + 1][0] != self.tokensnome['end']:
            # Analisa as declarações dentro do bloco 'begin-end'.
            self.stmt()
            self.consome(self.tokensnome[';'])  # Consome o ponto e vírgula ';'.
        self.consome(self.tokensnome['end'])  # Consome o token 'end'.
        self.lista_interpretador.append(('JUMP', label_inicio, None, None))  # Adiciona uma instrução de salto para o início do loop.
        self.lista_interpretador.append(('LABEL', label_fim, None, None))  # Adiciona o label de fim do loop ao código intermediário.

    def expr(self):
        # Analisa uma expressão.
        self.exprFinalCorrecao()  # Chama a função de correção para a análise da expressão.

    def orfunc(self):
        # Analisa uma expressão com o operador 'or'.
        self.andfunc()  # Analisa a expressão com 'and'.
        while self.restoOr():  # Continua enquanto houver operadores 'or'.
            pass

    def andfunc(self):
        # Analisa uma expressão com o operador 'and'.
        self.notfunc()  # Analisa a expressão com 'not'.
        while self.restoAnd():  # Continua enquanto houver operadores 'and'.
            pass

    def notfunc(self):
        # Analisa uma expressão com o operador 'not'.
        prox_index = self.index + 1
        lista_tupla_prox = self.lista[prox_index]
        if lista_tupla_prox[0] == self.tokensnome['not']:
            # Se o próximo token for 'not', consome-o e analisa o restante.
            self.consome(self.tokensnome['not'])
            self.restoNot()
        else:
            self.restoNot()  # Se não for 'not', continua a análise normalmente.

    def restoOr(self):
        # Analisa o restante de uma expressão com 'or'.
        prox_index = self.index + 1
        lista_tupla_prox = self.lista[prox_index]
        if lista_tupla_prox[0] == self.tokensnome['or']:
            self.consome(self.tokensnome['or'])  # Consome o token 'or'.
            self.andfunc()  # Analisa a expressão após 'or'.
            return True
        return False

    def restoAnd(self):
        # Analisa o restante de uma expressão com 'and'.
        prox_index = self.index + 1
        lista_tupla_prox = self.lista[prox_index]
        if lista_tupla_prox[0] == self.tokensnome['and']:
            self.consome(self.tokensnome['and'])  # Consome o token 'and'.
            self.notfunc()  # Analisa a expressão após 'and'.
            return True
        return False

    def restoNot(self):
        # Analisa o restante de uma expressão com 'not'.
        prox_index = self.index + 1
        lista_tupla_prox = self.lista[prox_index]
        if lista_tupla_prox[0] in (self.tokensnome['IDENT'], self.tokensnome['STR'], self.tokensnome['(']):
            # Se o próximo token for um identificador, string ou parêntese, consome-o.
            self.consome(lista_tupla_prox[0])
        return False

# Gerador de Labels e Variáveis Temporárias
class GeradorDeLabelsETemporarias:
    def __init__(self):
        # Inicializa o gerador com contadores para labels e temporárias.
        self.contador_labels = 0
        self.contador_temporarias = 0

    def gerar_label(self):
        # Gera um novo label único.
        label = f"L{self.contador_labels}"
        self.contador_labels += 1
        return label

    def gerar_temporaria(self):
        # Gera uma nova variável temporária única.
        temp = f"TEMP{self.contador_temporarias}"
        self.contador_temporarias += 1
        return temp

# Definição do método corrigido para consumo completo da expressão
def exprFinalCorrecao(self):
    # Processa uma expressão composta por operadores lógicos e aritméticos.
    self.orfunc()  # Processa a expressão começando por operadores 'or'.
    prox_index = self.index + 1
    lista_tupla_prox = self.lista[prox_index]
    
    while lista_tupla_prox[0] in (self.tokensnome['='], self.tokensnome['<>'], self.tokensnome['>'], 
                                  self.tokensnome['<'], self.tokensnome['>='], self.tokensnome['<=']):
        # Enquanto o token for um operador de comparação, continue consumindo a expressão.
        self.consome(lista_tupla_prox[0])
        
        prox_index = self.index + 1
        lista_tupla_prox = self.lista[prox_index]
        if lista_tupla_prox[0] in (self.tokensnome['IDENT'], self.tokensnome['STR'], self.tokensnome['(']):
            self.consome(lista_tupla_prox[0])
            prox_index = self.index + 1
            lista_tupla_prox = self.lista[prox_index]
        else:
            raise Exception(f"ERRO: Esperado operando na linha {prox_index + 1}, encontrado {lista_tupla_prox}")
        
    if lista_tupla_prox[0] == self.tokensnome['then']:
        self.consome(self.tokensnome['then'])  # Consome o token 'then' se encontrado após a expressão.
    else:
        raise Exception(f"ERRO: Esperado 'then' na linha {prox_index + 1}, encontrado {lista_tupla_prox}")

# Substituição do método expr original pelo corrigido
setattr(AnalisadorSintatico, 'expr', exprFinalCorrecao)

if __name__ == "__main__":
    import lexico, sys
    if len(sys.argv) > 1:
        lista = lexico.main(sys.argv[1])
        AnSint = AnalisadorSintatico(lista)
        listaDoInterpretador = AnSint.function()
        print(listaDoInterpretador)
