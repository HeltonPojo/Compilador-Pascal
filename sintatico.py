class AnalisadorSintatico:
    def __init__(self, lista) -> None:
        self.tokensnome = {
            'program' : 17,
            'var' : 18,
            'integer' : 19,
            'real' : 20,
            'string' : 21,
            'begin' : 22,
            'end' : 23,
            'for' : 24,
            'to' : 25,
            'while' : 26,
            'do' : 27,
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
            'IDENT' : 46,
            'NUM' : 47,
            '+' : 1,
            '-' : 2,
            '/' : 3,
            '*' : 4,
            '=' : 14,
            '==' : 10,
            '<>' : 11,
            '>' : 12,
            '<' : 13,
            '>=' : 14,
            '<=' : 15,
            ':=' : 16,
            'STR' : 45,
        }
        self.index = -1
        self.lista = lista
        self.lista_interpretador = []
        self.label_count = 0
        self.temp_var_count = 0
        
    def gera_label(self):
        label = f"label_{self.label_count}"
        self.label_count += 1
        print(f"Gerando label: {label}")  # Adiciona este print para depuração
        return label


    def gera_temp_var(self):
        temp_var = f"temp_{self.temp_var_count}"
        self.temp_var_count += 1
        return temp_var    

    def consome(self, token_esperado):
        self.index += 1
        if self.index >= len(self.lista):
            raise Exception('Fim inesperado do arquivo.')

        token_atual = self.lista[self.index]
        print(f"Consumindo token: {token_atual}, Esperado: {token_esperado}")

        if token_atual[0] == token_esperado:
            print(f"Token {token_atual[1]} consumido com sucesso.")
            return
        else:
            raise Exception(f"ERRO NA LINHA: {self.index} TOKEN ESPERADO: {token_esperado}, TOKEN ENCONTRADO: {token_atual[0]}, VALOR DO TOKEN: {token_atual[1]}")

    def function(self):
        self.consome(self.tokensnome['program'])  # Consome 'program'
        self.consome(self.tokensnome['IDENT'])  # Espera um identificador como nome do programa
        self.consome(self.tokensnome[';'])  # Consome o ';' após o nome do programa
        
        if self.lookahead() == self.tokensnome['var']:  # Verifica se 'var' está presente
            self.declaration()  # Processa as declarações de variáveis
        
        self.consome(self.tokensnome['begin'])  # Consome 'begin' para começar o corpo do programa
        self.stmtList()  # Processa as instruções do corpo do programa
        self.consome(self.tokensnome['end'])  # Consome 'end'
        self.consome(self.tokensnome['.'])  # Consome o ponto final do programa
        return self.lista_interpretador  # Retorna a lista de instruções executáveis


    def listaIdent(self):
        lista_ident = [self.lista[self.index + 1][1]]  # Adiciona o primeiro identificador
        self.consome(self.tokensnome['IDENT'])  # Consome o identificador
        
        while self.lookahead() == self.tokensnome[',']:
            self.consome(self.tokensnome[','])  # Consome a vírgula
            lista_ident.append(self.lista[self.index + 1][1])  # Adiciona o próximo identificador
            self.consome(self.tokensnome['IDENT'])  # Consome o próximo identificador
            
        return lista_ident

    def restoIdentList(self):
        prox_index = self.index + 1
        token_prox = self.lista[prox_index]
        listaLocal = []
        if token_prox[0] == self.tokensnome[',']:
            self.consome(self.tokensnome[','])
            self.consome(self.tokensnome['IDENT'])
            listaLocal.append(self.lista[self.index][1])
            listaResto = self.restoIdentList()
            if listaResto:
                listaLocal.extend(listaResto)
        return listaLocal
    def declaration(self):
        self.consome(self.tokensnome['var'])  # Consome a palavra-chave 'var'
        
        while self.lookahead() == self.tokensnome['IDENT']:  # Processa todas as declarações de variáveis
            ident_list = self.listaIdent()  # Processa a lista de identificadores
            self.consome(self.tokensnome[':'])  # Consome ':'
            tipo = self.type()  # Processa o tipo da variável
            
            for ident in ident_list:
                self.lista_interpretador.append(('DECLARATION', ident, tipo))
            
            self.consome(self.tokensnome[';'])  # Consome ';' após cada declaração
    def restoDeclaration(self):
        prox_index = self.index + 1
        lista_tupla_prox = self.lista[prox_index]
        if lista_tupla_prox[0] == self.tokensnome["IDENT"]:
            self.declaration()
            self.restoDeclaration()
        else:
            return
    def type(self):
        prox_token = self.lookahead()
        if prox_token == self.tokensnome['integer']:
            self.consome(self.tokensnome['integer'])
            return 'integer'
        elif prox_token == self.tokensnome['real']:
            self.consome(self.tokensnome['real'])
            return 'real'
        elif prox_token == self.tokensnome['string']:
            self.consome(self.tokensnome['string'])
            return 'string'
        else:
            raise Exception(f"Tipo desconhecido: {prox_token}")
            
    def typefunc(self):
        prox_index = self.index + 1
        token_prox = self.lista[prox_index]
        token_type = token_prox[0]

        if token_type == self.tokensnome['integer']:
            self.consome(self.tokensnome['integer'])
            return self.tokensnome['integer']
        elif token_type == self.tokensnome['real']:
            self.consome(self.tokensnome['real'])
            return self.tokensnome['real']
        elif token_type == self.tokensnome['string']:
            self.consome(self.tokensnome['string'])
            return self.tokensnome['string']
        else:
            raise Exception(f"ERRO NA LINHA: {prox_index} TOKEN ESPERADO: {token_type}")

    def bloco(self):
        self.consome(self.tokensnome['begin'])
        self.stmtList()
        self.consome(self.tokensnome['end'])

    def stmtList(self):
        prox_token = self.lista[self.index + 1]
        print(f"Iniciando stmtList, próximo token: {prox_token}")

        if prox_token[0] in (
            self.tokensnome["if"],
            self.tokensnome["while"],
            self.tokensnome["write"],
            self.tokensnome["read"],
            self.tokensnome["begin"],
            self.tokensnome["IDENT"],
            self.tokensnome[";"],
        ):
            self.stmt()
            self.stmtList()  # Recursão para processar a lista de statements
        else:
            print(f"Encerrando stmtList, token não esperado: {prox_token}")
            return


    def stmt(self):
        prox_token = self.lista[self.index + 1]
        print(f"Processando instrução, próximo token: {prox_token}")

        if prox_token[0] == self.tokensnome['if']:
            self.ifStmt()
        elif prox_token[0] == self.tokensnome['while']:
            self.whileStmt()
        elif prox_token[0] == self.tokensnome['write']:
            self.ioStmt()  # Função que processa instruções de IO, como write e read
        elif prox_token[0] == self.tokensnome['read']:
            self.ioStmt()  # Função que processa instruções de IO, como write e read
        elif prox_token[0] == self.tokensnome['IDENT']:
            self.atrib()  # Processa atribuições
        elif prox_token[0] == self.tokensnome['begin']:
            self.bloco()  # Processa blocos de código
        elif prox_token[0] == self.tokensnome[';']:
            self.consome(self.tokensnome[';'])
        else:
            raise Exception(f"Token inesperado ao processar instrução: {prox_token}")




    def forStmt(self):
        self.consome(self.tokensnome['for'])
        
        self.atrib()  # Atribuição inicial
        
        label_start = self.gera_label()
        self.lista_interpretador.append(("label", label_start, None, None))
        
        temp_var = self.gera_temp_var()
        self.lista_interpretador.append(("CMP", temp_var, "end", None))
        label_end = self.gera_label()
        self.lista_interpretador.append(("JUMP_IF_FALSE", label_end, None, None))
        
        self.consome(self.tokensnome['to'])
        self.endFor()
        self.consome(self.tokensnome['do'])
        
        self.stmt()  # Corpo do loop
        
        self.lista_interpretador.append(("INCR", "control_var", None, None))
        self.lista_interpretador.append(("JUMP", label_start, None, None))
        
        self.lista_interpretador.append(("label", label_end, None, None))
        return

    def endFor(self):
        prox_index = self.index + 1
        token_prox = self.lista[prox_index]
        if token_prox[0] == self.tokensnome["IDENT"]:
            self.consome(self.tokensnome["IDENT"])
            return True, self.lista[self.index][1]
        elif token_prox[0] == self.tokensnome["integer"]:
            self.consome(self.tokensnome["integer"])
            return False, self.lista[self.index][1]
        else:
            raise Exception(f"ERRO NA LINHA: {prox_index} TOKEN ESPERADO: {token_prox}")

    def ioStmt(self):
        prox_index = self.index + 1
        token_prox = self.lista[prox_index]
        if token_prox[0] == self.tokensnome['read']:
            self.consome(self.tokensnome['read'])
            self.consome(self.tokensnome['('])
            operador = self.lista[self.index + 1][1]
            self.consome(self.tokensnome['IDENT'])
            self.consome(self.tokensnome[')'])
            self.consome(self.tokensnome[';'])
            self.lista_interpretador.append(("CALL", "SCAN", operador, None))
        elif token_prox[0] == self.tokensnome['write']:
            self.consome(self.tokensnome['write'])
            self.consome(self.tokensnome['('])
            
            while True:
                if self.lista[self.index + 1][0] == self.tokensnome['STR']:
                    operador = self.lista[self.index + 1][1]
                    self.consome(self.tokensnome['STR'])
                elif self.lista[self.index + 1][0] == self.tokensnome['IDENT']:
                    operador = self.lista[self.index + 1][1]
                    self.consome(self.tokensnome['IDENT'])
                    
                    # Verifique se há uma operação aritmética (+, -, etc.)
                    if self.lista[self.index + 1][0] in [self.tokensnome['+'], self.tokensnome['-'], self.tokensnome['*'], self.tokensnome['/']]:
                        operador_aritmetico = self.lista[self.index + 1][1]
                        self.consome(self.lista[self.index + 1][0])
                        proximo_operador = self.lista[self.index + 1][1]
                        self.consome(self.tokensnome['IDENT'])  # Consome o próximo identificador na operação
                        
                        # Adicione a operação aritmética à lista de interpretador
                        self.lista_interpretador.append((operador_aritmetico, operador, proximo_operador, None))
                        operador = proximo_operador  # Atualiza o operador para o próximo ciclo
                    
                # Verifique se há uma vírgula para continuar processando ou se deve fechar o parêntese
                if self.lista[self.index + 1][0] == self.tokensnome[',']:
                    self.consome(self.tokensnome[','])
                elif self.lista[self.index + 1][0] == self.tokensnome[')']:
                    break
                else:
                    raise Exception(f"ERRO: Token inesperado na linha {self.index}: {self.lista[self.index + 1]}")
            
            self.consome(self.tokensnome[')'])
            self.consome(self.tokensnome[';'])
            self.lista_interpretador.append(("CALL", "PRINT", operador, None))
    
    def lookahead(self):
        if self.index + 1 < len(self.lista):
            return self.lista[self.index + 1][0]
        else:
            return None  # Fim dos tokens
    
    def whileStmt(self):
        label_start = self.gera_label()
        self.lista_interpretador.append(("label", label_start, None, None))

        self.consomeconsome(self.tokensnome['while'])

        temp_var = self.gera_temp_var()
        condicao = self.expr()

        self.lista_interpretador.append(("CMP", temp_var, condicao, None))

        label_end = self.gera_label()
        self.lista_interpretador.append(("JUMP_IF_FALSE", label_end, temp_var, None))

        self.consome(self.tokensnome['do'])
        self.stmt()

        self.lista_interpretador.append(("JUMP", label_start, None, None))
        self.lista_interpretador.append(("label", label_end, None, None))

    def ifStmt(self):
        print("Iniciando processamento de ifStmt")
        self.consome(self.tokensnome['if'])  # Consome o token 'if'
        
        prox_token = self.lookahead()
        print(f"Próximo token após 'if': {prox_token}")

        # Verifica se o próximo token é válido para iniciar uma expressão
        if prox_token in [self.tokensnome['IDENT'], self.tokensnome.get('NUM', None)]:
            condicao = self.expr()  # Processa a expressão condicional
            
            # Agora, deve-se esperar e consumir um operador relacional como '=', '>', '<', etc.
            operador_relacional = self.lookahead()
            if operador_relacional in [self.tokensnome['=='], self.tokensnome['<>'], self.tokensnome['>'], self.tokensnome['<'], self.tokensnome['<='], self.tokensnome['>='], self.tokensnome['=']]:
                self.consome(operador_relacional)  # Consome o operador relacional
                comparado = self.expr()  # Consome a expressão à direita do operador

            # Depois que a condição completa for processada, continue verificando o 'then'
            self.consome(self.tokensnome['then'])  # Consome o token 'then'
            
            # Processa o restante da instrução if
            label_else = self.gera_label()
            label_end = self.gera_label()

            self.lista_interpretador.append(('JUMP_IF_FALSE', label_else, condicao, None))
            self.stmt()  # Processa o corpo do 'if'
            
            self.lista_interpretador.append(('JUMP', label_end, None, None))
            self.lista_interpretador.append(('label', label_else, None, None))
            
            if self.lookahead()[0] == self.tokensnome['else']:
                self.consome(self.tokensnome['else'])
                self.stmt()

            self.lista_interpretador.append(('label', label_end, None, None))
            print("Finalizando processamento de ifStmt")
        else:
            raise Exception(f"Erro de fluxo: Token inesperado após 'if': {prox_token}")







    def atrib(self):
        var_name = self.lista[self.index + 1][1]
        self.consome(self.tokensnome['IDENT'])
        self.consome(self.tokensnome[':='])
        valor = self.expr()
        self.lista_interpretador.append(("=", var_name, valor, None))

    def expr(self):
        print(f"Iniciando expr com self.index: {self.index}")
        token = self.lookahead()
        print(f"Token atual em expr: {token}")

        # Verifica se o token é um identificador ou número e consome adequadamente
        if token == self.tokensnome['IDENT']:
            # Consome o identificador
            self.consome(self.tokensnome['IDENT'])
            return self.lista[self.index][1]  # Retorna o identificador

        elif token == self.tokensnome.get('NUM', None):
            # Consome um número
            self.consome(self.tokensnome['NUM'])
            return self.lista[self.index][1]  # Retorna o número

        else:
            raise Exception(f"Token inesperado em expr: {token}")




    def orfunc(self):
        left_temp = self.andfunc()
        return self.restoOr(left_temp)

    def restoOr(self, left_temp):
        prox_index = self.index + 1
        token_prox = self.lista[prox_index]
        if token_prox[0] == self.tokensnome['or']:
            self.consome(self.tokensnome['or'])
            right_temp = self.andfunc()
            result_temp = self.gera_temp_var()
            self.lista_interpretador.append(("OR", result_temp, left_temp, right_temp))
            return self.restoOr(result_temp)
        else:
            return left_temp

    def andfunc(self):
        left_temp = self.notfunc()
        return self.restoAnd(left_temp)
    
    def restoAnd(self, left_temp):
        prox_index = self.index + 1
        token_prox = self.lista[prox_index]
        if token_prox[0] == self.tokensnome['and']:
            self.consome(self.tokensnome['and'])
            right_temp = self.notfunc()
            result_temp = self.gera_temp_var()
            self.lista_interpretador.append(("AND", result_temp, left_temp, right_temp))
            return self.restoAnd(result_temp)
        else:
            return left_temp

    def notfunc(self):
        prox_index = self.index + 1
        token_prox = self.lista[prox_index]
        if token_prox[0] == self.tokensnome['not']:
            self.consome(self.tokensnome['not'])
            operand_temp = self.notfunc()
            result_temp = self.gera_temp_var()
            self.lista_interpretador.append(("NOT", result_temp, operand_temp, None))
            return result_temp
        else:
            return self.rel()
        
    def rel(self):
        left_temp = self.add()
        return self.restoRel(left_temp)
    
    def restoRel(self, left_temp):
        prox_index = self.index + 1
        token_prox = self.lista[prox_index]
        if token_prox[0] in [self.tokensnome['=='], self.tokensnome['<>'], self.tokensnome['<'], self.tokensnome['>'], self.tokensnome['<='], self.tokensnome['>=']]:
            op = token_prox[0]
            self.consome(op)
            right_temp = self.add()
            result_temp = self.gera_temp_var()
            self.lista_interpretador.append((self.lista[prox_index][1], result_temp, left_temp, right_temp))
            return result_temp
        else:
            return left_temp

    def add(self):
        left_temp = self.mult()
        return self.restoAdd(left_temp)

    def restoAdd(self, left_temp):
        prox_index = self.index + 1
        token_prox = self.lista[prox_index]
        if token_prox[0] in [self.tokensnome['+'], self.tokensnome['-']]:
            op = token_prox[0]
            self.consome(op)
            right_temp = self.mult()
            result_temp = self.gera_temp_var()
            self.lista_interpretador.append((self.lista[prox_index][1], result_temp, left_temp, right_temp))
            return self.restoAdd(result_temp)
        else:
            return left_temp

    def mult(self):
        left_temp = self.uno()
        return self.restoMult(left_temp)

    def restoMult(self, left_temp):
        prox_index = self.index + 1
        token_prox = self.lista[prox_index]
        if token_prox[0] in [self.tokensnome['*'], self.tokensnome['/'], self.tokensnome['mod'], self.tokensnome['div']]:
            op = token_prox[0]
            self.consome(op)
            right_temp = self.uno()
            result_temp = self.gera_temp_var()
            self.lista_interpretador.append((self.lista[prox_index][1], result_temp, left_temp, right_temp))
            return self.restoMult(result_temp)
        else:
            return left_temp

    def uno(self):
        prox_index = self.index + 1
        token_prox = self.lista[prox_index]
        if token_prox[0] in [self.tokensnome['+'], self.tokensnome['-']]:
            op = token_prox[0]
            self.consome(op)
            operand_temp = self.uno()
            result_temp = self.gera_temp_var()
            self.lista_interpretador.append((op, result_temp, operand_temp, None))
            return result_temp
        else:
            return self.factor()

    def factor(self):
        prox_index = self.index + 1
        token_prox = self.lista[prox_index]
        if token_prox[0] == self.tokensnome['integer']:
            value = self.lista[self.index + 1][1]
            self.consome(self.tokensnome['integer'])
            return value
        elif token_prox[0] == self.tokensnome['real']:
            value = self.lista[self.index + 1][1]
            self.consome(self.tokensnome['real'])
            return value
        elif token_prox[0] == self.tokensnome['IDENT']:
            ident = self.lista[self.index + 1][1]
            self.consome(self.tokensnome['IDENT'])
            return ident
        elif token_prox[0] == self.tokensnome['(']:
            self.consome(self.tokensnome['('])
            expr_result = self.expr()
            self.consome(self.tokensnome[')'])
            return expr_result
        elif token_prox[0] == self.tokensnome['STR']:
            value = self.lista[self.index + 1][1]
            self.consome(self.tokensnome['STR'])
            return value
        return

if __name__ == "__main__":
    import lexico, sys

    if len(sys.argv) > 1:
        
        lista = lexico.main(sys.argv[1])
        AnSint = AnalisadorSintatico(lista)
        listaDoInterpretador = AnSint.function()
        print("Lista de instruções gerada pelo sintático:")
        print(listaDoInterpretador)
