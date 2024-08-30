
# sintatico.py
# Este arquivo implementa o analisador sintático para o compilador de Pascal.
# A classe AnalisadorSintatico consome tokens e verifica a sintaxe do código-fonte.
# O código intermediário é gerado na forma de tuplas, que são posteriormente interpretadas e executadas.
# Contém funções para análise de declarações de variáveis, laços de repetição, e expressões condicionais.

class AnalisadorSintatico:
    # Construtor da classe. Inicializa os tokens e a lista de tokens a serem analisados.
    def __init__(self, lista) -> None:
        # Dicionário que mapeia símbolos e palavras-chave para seus respectivos tokens.
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
        # Índice atual da análise de tokens
        self.index = -1
        # Lista de tokens a serem analisados
        self.lista = lista
        # Lista de tuplas que representará o código intermediário
        self.lista_interpretador = []

    # Consome o próximo token da lista, verificando se é o esperado
    def consome(self, token_esperado):
        self.index += 1  # Incrementa o índice para avançar para o próximo token
        lista_tupla = self.lista[self.index]  # Obtém a tupla do token atual
        if lista_tupla[0] == token_esperado:
            return  # Se o token for o esperado, continua a execução
        else:
            # Caso contrário, imprime um erro e encerra a execução
            print('ERRO NA LINHA: ', lista_tupla)
            print('TOKEN ESPERADO: ', token_esperado)
            sys.exit()

    # Função principal que inicia a análise do código-fonte
    def function(self):
        # Consome o token 'program'
        self.consome(self.tokensnome['program'])
        # Consome o identificador do programa
        self.consome(self.tokensnome['IDENT'])
        # Consome o ponto e vírgula
        self.consome(self.tokensnome[';'])
        # Chama a análise de declarações de variáveis
        self.declarations()
        # Consome o token 'begin'
        self.consome(self.tokensnome['begin'])
        # Analisa a lista de comandos
        self.stmtList()
        # Consome o token 'end'
        self.consome(self.tokensnome['end'])
        # Consome o ponto final
        self.consome(self.tokensnome['.'])
        # Se chegou até aqui, significa que não houve erros
        print('passou sem erros')
        # Retorna a lista de código intermediário
        return self.lista_interpretador

    # Função para analisar declarações de variáveis
    def declarations(self):
        self.consome(self.tokensnome['var'])  # Consome o token 'var'
        self.declaration()  # Chama a função para analisar uma declaração
        self.restoDeclaration()  # Analisa possíveis declarações subsequentes
        return

    # Função que analisa uma declaração específica de variáveis
    def declaration(self):
        lista_variaveis = self.listaIdent()  # Obtém a lista de identificadores
        self.consome(self.tokensnome[':'])  # Consome o token ':'
        tipo = self.typefunc()  # Obtém o tipo das variáveis
        self.consome(self.tokensnome[';'])  # Consome o ponto e vírgula
        # Inicializa as variáveis conforme o tipo
        valor_inicial = 0 if tipo == "int" else 0.0 if tipo == "float" else '' if tipo == "string" else None
        for identificador in lista_variaveis:
            self.lista_interpretador.append(("=", identificador, valor_inicial, None))
        return

    # Função que analisa uma lista de identificadores
    def listaIdent(self):
        listaLocal = []  # Cria uma lista local para armazenar os identificadores
        self.consome(self.tokensnome['IDENT'])  # Consome o primeiro identificador
        listaLocal.append(lista[self.index][1])  # Adiciona o identificador à lista local
        listaResto = self.restoIdentList()  # Analisa possíveis identificadores subsequentes
        if listaResto:
            listaLocal.extend(listaResto)  # Adiciona os identificadores subsequentes à lista local
        return listaLocal  # Retorna a lista de identificadores

    # Função que analisa possíveis identificadores subsequentes em uma lista de identificadores
    def restoIdentList(self):
        prox_index = self.index + 1  # Obtém o próximo índice
        lista_tupla_prox = lista[prox_index]  # Obtém a tupla do próximo token
        listaLocal = []  # Cria uma lista local para armazenar os identificadores
        if(lista_tupla_prox[0] == self.tokensnome[',']):
            self.consome(self.tokensnome[','])  # Consome a vírgula
            self.consome(self.tokensnome['IDENT'])  # Consome o próximo identificador
            listaLocal.append(lista[self.index][1])  # Adiciona o identificador à lista local
        return listaLocal  # Retorna a lista de identificadores subsequentes

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
        self.lista_interpretador = []

    def consome(self, token_esperado):
        self.index+=1
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
        return self.lista_interpretador

    #------------------------------------
    # declaracoes de variaveis
    #------------------------------------

    def declarations(self):
        self.consome(self.tokensnome['var'])
        self.declaration()
        self.restoDeclaration()
        return


    def declaration(self):
        lista_variaveis = self.listaIdent()
        self.consome(self.tokensnome[':'])
        tipo = self.typefunc()
        self.consome(self.tokensnome[';'])
        valor_inicial = 0 if tipo == "int" else 0.0 if tipo == "float" else '' if tipo == "string" else None
        for identificador in lista_variaveis:
            self.lista_interpretador.append(("=", identificador, valor_inicial, None))
        return
        lista_variaveis = self.listaIdent()
        self.consome(self.tokensnome[':'])
        tipo = self.typefunc()
        self.consome(self.tokensnome[';'])
        for identificador in lista_variaveis :
            if (tipo == "int"):
                self.lista_interpretador.append(("=", identificador, 0,None))
            elif (tipo == "float"):
                self.lista_interpretador.append(("=", identificador, 0,None))
            elif (tipo == "string"):
                self.lista_interpretador.append(("=", identificador, '',None))
        return

    def listaIdent(self):
        listaLocal = []
        self.consome(self.tokensnome['IDENT'])
        listaLocal.append(lista[self.index][1])
        listaResto = self.restoIdentList()
        if listaResto:
            listaLocal.extend(listaResto)
        return listaLocal 

    def restoIdentList(self):
        prox_index = self.index + 1
        lista_tupla_prox = lista[prox_index]
        listaLocal = []
        if(lista_tupla_prox[0] == self.tokensnome[',']):
            self.consome(self.tokensnome[','])
            self.consome(self.tokensnome['IDENT'])
            listaLocal.append(lista[self.index][1])
            listaResto = self.restoIdentList()
            if listaResto:
                listaLocal.extend(listaResto)
        return listaLocal

    def restoDeclaration(self):
        prox_index = self.index + 1
        lista_tupla_prox = lista[prox_index]
        if(lista_tupla_prox[0] == self.tokensnome['IDENT']):
            self.declaration()
            self.restoDeclaration()
        else:
            return

    def typefunc(self):
        prox_index = self.index + 1
        lista_tupla_prox = lista[prox_index]
        if(lista_tupla_prox[0] == self.tokensnome['interger']):
            self.consome(self.tokensnome['interger'])
            return "int"
        elif(lista_tupla_prox[0] == self.tokensnome['real']):
            self.consome(self.tokensnome['real'])
            return "float"
        elif(lista_tupla_prox[0] == self.tokensnome['string']):
            self.consome(self.tokensnome['string'])
            return "string"
        else:
            print('ERRO NA LINHA: ', lista_tupla_prox)
            print('TOKENS ESPERADOS: interger real string')
            sys.exit()
            return
        return

    #------------------------------------
    # instrucoes dos programas
    #------------------------------------

    def bloco(self):
        self.consome(self.tokensnome['begin'])
        self.stmtList()
        self.consome(self.tokensnome['end'])
        self.consome(self.tokensnome[';'])
        return

    def stmtList(self):
        prox_index = self.index + 1
        lista_tupla_prox = lista[prox_index]
        if(lista_tupla_prox[0] in (self.tokensnome['interger'], self.tokensnome['for'], self.tokensnome['write'], self.tokensnome['read'], self.tokensnome['begin'], self.tokensnome['if'], self.tokensnome['IDENT'], self.tokensnome['while'], self.tokensnome[';'])):
            self.stmt()
            self.stmtList()
            return
        else:
            return

    def stmt(self):
        prox_index = self.index + 1
        lista_tupla_prox = lista[prox_index]
        if(lista_tupla_prox[0] == self.tokensnome['for']):
            self.forStmt()
        elif(lista_tupla_prox[0] == self.tokensnome['read'] or lista_tupla_prox[0] == self.tokensnome['write']):
            self.ioStmt()
        elif(lista_tupla_prox[0] == self.tokensnome['while']):
            self.whileStmt()
        elif(lista_tupla_prox[0] == self.tokensnome['IDENT']):
            self.atrib()
        elif(lista_tupla_prox[0] == self.tokensnome['if']):
            self.ifStmt()
        elif(lista_tupla_prox[0] == self.tokensnome['begin']):
            self.bloco()
        elif(lista_tupla_prox[0] == self.tokensnome[';']):
            self.consome(self.tokensnome[';'])
        else:
            print('ERRO NA LINHA: ', lista_tupla_prox)
            print('TOKENS ESPERADOS: begin if IDENT while read write for')
            sys.exit()
            return
        return

    #---------------------------
    # descricao das instrucoes
    #---------------------------

    # comando for
    # deixar o atrib igual ao declarations, colocar duas label(colocar gerador de label) antes de stmt verificar se o identificador chegou no endFor e chamar o jump para a label correspondente

    def forStmt(self):
        # Gerações de labels para controle do fluxo
        label_inicio = self.controle.geraLabel()
        label_fim = self.controle.geraLabel()

        # Consome a parte da atribuição
        self.consome(self.tokensnome['for'])
        atribuicao, listaAtribuicao = self.atrib()
        self.lista_interpretador.extend(listaAtribuicao)

        # Geração de código para a condição do loop
        self.consome(self.tokensnome['to'])
        self.lista_interpretador.append(("label", label_inicio, None, None))
        condicao, listaCondicao = self.expr()
        self.lista_interpretador.extend(listaCondicao)
        self.lista_interpretador.append(("IF_FALSE", condicao, label_fim, None))

        # Consome o corpo do loop
        self.consome(self.tokensnome['do'])
        listaStmt = self.stmt()
        self.lista_interpretador.extend(listaStmt)

        # Incremento e volta para a condição
        self.lista_interpretador.append(("JUMP", label_inicio, None, None))
        self.lista_interpretador.append(("label", label_fim, None, None))
        return
        self.consome(self.tokensnome['for'])
        self.atrib()
        self.consome(self.tokensnome['to'])
        self.endFor()
        self.consome(self.tokensnome['do'])
        self.stmt()
        return

    def endFor(self):
        prox_index = self.index + 1
        lista_tupla_prox = lista[prox_index]
        if(lista_tupla_prox[0] == self.tokensnome['IDENT']):
            self.consome(self.tokensnome['IDENT'])
        elif(lista_tupla_prox[0] == self.tokensnome['interger']):
            self.consome(self.tokensnome['interger'])
        else:
            print('ERRO NA LINHA: ', lista_tupla_prox)
            print('TOKENS ESPERADOS: IDENT interger')
            sys.exit()
            return    
        return

    # comandos de IO

    def ioStmt(self):
        prox_index = self.index + 1
        lista_tupla_prox = lista[prox_index]
        if(lista_tupla_prox[0] == self.tokensnome['read']):
            self.consome(self.tokensnome['read'])
            self.consome(self.tokensnome['('])
            self.consome(self.tokensnome['IDENT'])
            operador = lista[self.index][1]
            self.consome(self.tokensnome[')'])
            self.consome(self.tokensnome[';'])
            self.lista_interpretador.append(("CALL", "SCAN", operador, None))
        elif(lista_tupla_prox[0] == self.tokensnome['write']):
            self.consome(self.tokensnome['write'])
            self.consome(self.tokensnome['('])
            self.outList()
            self.consome(self.tokensnome[')'])
            self.consome(self.tokensnome[';'])
        return

    def outList(self):
        self.out()
        self.restoOut()
        return

    def restoOut(self):
        prox_index = self.index + 1
        lista_tupla_prox = lista[prox_index]
        if(lista_tupla_prox[0] == self.tokensnome[',']):
            self.consome(self.tokensnome[','])
            self.outList()
        return

    def out(self):
        prox_index = self.index + 1
        lista_tupla_prox = lista[prox_index]
        if(lista_tupla_prox[0] == self.tokensnome['STR']):
            self.consome(self.tokensnome['STR'])
            self.lista_interpretador.append(("CALL", "PRINT", lista[self.index][1], None))
        elif(lista_tupla_prox[0] == self.tokensnome['IDENT']):
            self.consome(self.tokensnome['IDENT'])
            self.lista_interpretador.append(("CALL", "PRINT", None, lista[self.index][1]))
        elif(lista_tupla_prox[0] == self.tokensnome['interger']):
            self.consome(self.tokensnome['interger'])
            self.lista_interpretador.append(("CALL", "PRINT", lista[self.index][1], None))
        elif(lista_tupla_prox[0] == self.tokensnome['real']):
            self.consome(self.tokensnome['real'])
            self.lista_interpretador.append(("CALL", "PRINT", lista[self.index][1], None))
        else:
            print('ERRO NA LINHA: ', lista_tupla_prox)
            print('TOKENS ESPERADOS: IDENT STR interger real')
            sys.exit()
            return
        return

    # comando while


    def whileStmt(self):
        # Gerações de labels para controle do fluxo
        label_inicio = self.controle.geraLabel()
        label_fim = self.controle.geraLabel()

        # Geração de código para a condição do loop
        self.consome(self.tokensnome['while'])
        self.lista_interpretador.append(("label", label_inicio, None, None))
        condicao, listaCondicao = self.expr()
        self.lista_interpretador.extend(listaCondicao)
        self.lista_interpretador.append(("IF_FALSE", condicao, label_fim, None))

        # Consome o corpo do loop
        self.consome(self.tokensnome['do'])
        listaStmt = self.stmt()
        self.lista_interpretador.extend(listaStmt)

        # Volta para a condição
        self.lista_interpretador.append(("JUMP", label_inicio, None, None))
        self.lista_interpretador.append(("label", label_fim, None, None))
        return
        self.consome(['while'])
        self.expr()
        self.stmt()
        return

    # comando if


    def ifStmt(self):
        # Geração de label para o bloco else ou final
        label_else = self.controle.geraLabel()
        label_fim = self.controle.geraLabel()

        # Consome a condição do if
        self.consome(self.tokensnome['if'])
        condicao, listaCondicao = self.expr()
        self.lista_interpretador.extend(listaCondicao)
        self.lista_interpretador.append(("IF_FALSE", condicao, label_else, None))

        # Consome o bloco do then
        self.consome(self.tokensnome['then'])
        listaStmtThen = self.stmt()
        self.lista_interpretador.extend(listaStmtThen)
        self.lista_interpretador.append(("JUMP", label_fim, None, None))

        # Consome o bloco do else, se existir
        self.lista_interpretador.append(("label", label_else, None, None))
        if self.lista[self.index][0] == self.tokensnome['else']:
            self.consome(self.tokensnome['else'])
            listaStmtElse = self.stmt()
            self.lista_interpretador.extend(listaStmtElse)

        self.lista_interpretador.append(("label", label_fim, None, None))
        return
        self.consome(self.tokensnome['if'])
        self.expr()
        self.consome(self.tokensnome['then'])
        self.stmt()
        self.elsePart()
        return

    def elsePart(self):
        prox_index = self.index + 1
        lista_tupla_prox = lista[prox_index]
        if(lista_tupla_prox[0] == self.tokensnome['else']):
            self.consome(self.tokensnome['else'])
            self.stmt()
        else:
            return
        return

    #------------------------------
    # expressoes
    #------------------------------

    def atrib(self):
        self.consome(self.tokensnome['IDENT'])
        self.consome(self.tokensnome['=:'])
        self.expr()
        return

    def expr(self):
        self.orfunc()
        return

    def orfunc(self):
        self.andfunc()
        self.restoOr()
        return

    def restoOr(self):
        prox_index = self.index + 1
        lista_tupla_prox = lista[prox_index]
        if(lista_tupla_prox[0] == self.tokensnome['or']):
            self.consome(self.tokensnome['or'])
            self.andfunc()
            self.restoOr()
        else:
            return
        return

    def andfunc(self):
        self.notfunc()
        self.restoAnd()
        return

    def restoAnd(self):
        prox_index = self.index + 1
        lista_tupla_prox = lista[prox_index]
        if(lista_tupla_prox[0] == self.tokensnome['and']):
            self.consome(self.tokensnome['and'])
            self.notfunc()
            self.restoAnd()
        else:
            return
        return

    def notfunc(self):
        prox_index = self.index + 1
        lista_tupla_prox = lista[prox_index]
        if(lista_tupla_prox[0] == self.tokensnome['not']):        
            self.consome(self.tokensnome['not'])
            self.notfunc()
        else:
            self.rel()
            return
        return

    def rel(self):
        self.add()
        self.restoRel()
        return

    def restoRel(self):
        prox_index = self.index + 1
        lista_tupla_prox = lista[prox_index]
        if(lista_tupla_prox[0] == self.tokensnome['==']):
            self.consome(self.tokensnome['=='])
            self.add()
        elif(lista_tupla_prox[0] == self.tokensnome['<>']):
            self.consome(self.tokensnome['<>'])
            self.add()
        elif(lista_tupla_prox[0] == self.tokensnome['<']):
            self.consome(self.tokensnome['<'])
            self.add()
        elif(lista_tupla_prox[0] == self.tokensnome['>']):
            self.consome(self.tokensnome['>'])
            self.add()
        elif(lista_tupla_prox[0] == self.tokensnome['<=']):
            self.consome(self.tokensnome['<='])
            self.add()
        elif(lista_tupla_prox[0] == self.tokensnome['>=']):
            self.consome(self.tokensnome['>='])
            self.add()
        else:
            return
        return

    def add(self):
        self.mult()
        self.restoAdd()
        return

    def restoAdd(self):
        prox_index = self.index + 1
        lista_tupla_prox = lista[prox_index]
        if(lista_tupla_prox[0] == self.tokensnome['+']):
            self.consome(self.tokensnome['+'])
            self.mult()
            self.restoAdd()
        elif(lista_tupla_prox[0] == self.tokensnome['-']):
            self.consome(self.tokensnome['-'])
            self.mult()
            self.restoAdd()
        else: 
            return
        return

    def mult(self):
        self.uno()
        self.restoMult()
        return

    def restoMult(self):
        prox_index = self.index + 1
        lista_tupla_prox = lista[prox_index]
        if(lista_tupla_prox[0] == self.tokensnome['*']):
            self.consome(self.tokensnome['*'])
            self.uno()
            self.restoMult()
        elif(lista_tupla_prox[0] == self.tokensnome['/']):
            self.consome(self.tokensnome['/'])
            self.uno()
            self.restoMult()
        elif(lista_tupla_prox[0] == self.tokensnome['mod']):
            self.consome(self.tokensnome['mod'])
            self.uno()
            self.restoMult()
        elif(lista_tupla_prox[0] == self.tokensnome['div']):
            self.consome(self.tokensnome['div'])
            self.uno()
            self.restoMult()
        else:
            return
        return

    def uno(self):
        prox_index = self.index + 1
        lista_tupla_prox = lista[prox_index]
        if(lista_tupla_prox[0] == self.tokensnome['+']):
            self.consome(self.tokensnome['+'])
            self.uno()
        elif(lista_tupla_prox[0] == self.tokensnome['-']):
            self.consome(self.tokensnome['-'])
            self.uno()
        else:
            self.factor()
        return

    def factor(self):
        prox_index = self.index + 1
        lista_tupla_prox = lista[prox_index]
        if(lista_tupla_prox[0] == self.tokensnome['interger']):
            self.consome(self.tokensnome['interger'])
        elif(lista_tupla_prox[0] == self.tokensnome['real']):
            self.consome(self.tokensnome['real'])
        elif(lista_tupla_prox[0] == self.tokensnome['IDENT']):
            self.consome(self.tokensnome['IDENT'])
        elif(lista_tupla_prox[0] == self.tokensnome['(']):
            self.consome(self.tokensnome['('])
            self.expr()
            self.consome(self.tokensnome[')'])
        elif(lista_tupla_prox[0] == self.tokensnome['STR']):
            self.consome(self.tokensnome['STR'])
        return

#---------
# the end
#---------	 

if __name__ == "__main__":
    import lexico, sys
    if len(sys.argv) > 1:
        lista = lexico.main(sys.argv[1])
        AnSint = AnalisadorSintatico(lista)
        listaDoInterpretador = AnSint.function()
        print(listaDoInterpretador)
