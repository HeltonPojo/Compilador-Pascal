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

    def consome(self, token_esperado):
        self.index+=1
        lista_tupla = self.lista[self.index]
        if lista_tupla[0] == token_esperado:
            return
        else:
            print('ERRO NA LINHA(consome): ', lista_tupla)
            print('TOKEN ESPERADO', token_esperado)
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

    #------------------------------------
    # declaracoes de variaveis
    #------------------------------------

    def declarations(self):
        self.consome(self.tokensnome['var'])
        self.declaration()
        self.restoDeclaration()
        return

    def declaration(self):
        self.listaIdent()
        self.consome(self.tokensnome[':'])
        self.typefunc()
        self.consome(self.tokensnome[';'])
        return

    def listaIdent(self):
        self.consome(self.tokensnome['IDENT'])
        self.restoIdentList()    
        return

    def restoIdentList(self):
        prox_index = self.index + 1
        lista_tupla_prox = lista[prox_index]
        if(lista_tupla_prox[0] == self.tokensnome[',']):
            self.consome(self.tokensnome[','])
            self.consome(self.tokensnome['IDENT'])
            self.restoIdentList()
        else:
            return

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
        elif(lista_tupla_prox[0] == self.tokensnome['real']):
            self.consome(self.tokensnome['real'])
        elif(lista_tupla_prox[0] == self.tokensnome['string']):
            self.consome(self.tokensnome['string'])
        else:
            print('ERRO NA LINHA: ', self.index)
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
        if(lista_tupla_prox[0] == self.tokensnome['interger']):
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
        else:
            print('ERRO NA LINHA: ', self.index)
            sys.exit()
            return
        return

    #---------------------------
    # descricao das instrucoes
    #---------------------------

    # comando for
    def forStmt(self):
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
            print('ERRO NA LINHA: ', self.index)
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
            self.consome(self.tokensnome[')'])
            self.consome(self.tokensnome[';'])
        elif(lista_tupla_prox[0] == self.tokensnome['write']):
            self.consome(self.tokensnome['write'])
            self.consome(self.tokensnome['('])
            self.out()
            self.consome(self.tokensnome[')'])
            self.consome(self.tokensnome[';'])
        return

    def out(self):
        prox_index = self.index + 1
        lista_tupla_prox = lista[prox_index]
        if(lista_tupla_prox[0] == self.tokensnome['STR']):
            self.consome(self.tokensnome['STR'])
        elif(lista_tupla_prox[0] == self.tokensnome['IDENT']):
            self.consome(self.tokensnome['IDENT'])
        elif(lista_tupla_prox[0] == self.tokensnome['interger']):
            self.consome(self.tokensnome['interger'])
        elif(lista_tupla_prox[0] == self.tokensnome['real']):
            self.consome(self.tokensnome['real'])
        else:
            print('ERRO NA LINHA: ', self.index)
            sys.exit()
            return
        return

    # comando while

    def whileStmt(self):
        self.consome(['while'])
        self.expr()
        self.stmt()
        return

    # comando if

    def ifStmt(self):
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
        AnSint.function()