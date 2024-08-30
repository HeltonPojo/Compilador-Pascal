class AnalisadorSintatico:
    def __init__(self, lista) -> None:
        self.tokensnome = {
            "+": 1,
            "-": 2,
            "/": 3,
            "*": 4,
            "mod": 5,
            "div": 6,
            "or": 7,
            "and": 8,
            "not": 9,
            "==": 10,
            "<>": 11,
            ">": 12,
            "<": 13,
            ">=": 14,
            "<=": 15,
            ":=": 16,
            "program": 17,
            "var": 18,
            "interger": 19,
            "real": 20,
            "string": 21,
            "begin": 22,
            "end": 23,
            "for": 24,
            "to": 25,
            "while": 26,
            "do": 27,
            "break": 28,
            "continue": 29,
            "if": 30,
            "else": 31,
            "then": 32,
            "write": 33,
            "read": 34,
            ";": 35,
            ":": 36,
            ",": 37,
            ".": 38,
            "(": 39,
            ")": 40,
            "[": 41,
            "]": 42,
            "{": 43,
            "}": 44,
            "STR": 45,
            "IDENT": 46,
        }
        self.index = -1
        self.lista = lista
        self.lista_interpretador = []
        self.contadorLabels = 0

    def gerarLabel(self, funcao):
        self.contadorLabels += 1
        return funcao + str(self.contadorLabels)

    def consome(self, token_esperado):
        self.index += 1
        lista_tupla = self.lista[self.index]
        if lista_tupla[0] == token_esperado:
            return
        else:
            print("ERRO NA LINHA: ", lista_tupla)
            print("TOKEN ESPERADO: ", token_esperado)
            sys.exit()
            return

    # ------------------------------------
    # funcao principal
    # ------------------------------------

    def function(self):
        self.consome(self.tokensnome["program"])
        self.consome(self.tokensnome["IDENT"])
        self.consome(self.tokensnome[";"])
        self.declarations()
        self.consome(self.tokensnome["begin"])
        self.stmtList()
        self.consome(self.tokensnome["end"])
        self.consome(self.tokensnome["."])
        print("passou sem erros")
        return self.lista_interpretador

    # ------------------------------------
    # declaracoes de variaveis
    # ------------------------------------

    def declarations(self):
        self.consome(self.tokensnome["var"])
        self.declaration()
        self.restoDeclaration()
        return

    def declaration(self):
        lista_variaveis = self.listaIdent()
        self.consome(self.tokensnome[":"])
        tipo = self.typefunc()
        self.consome(self.tokensnome[";"])
        for identificador in lista_variaveis:
            if tipo == "int":
                self.lista_interpretador.append(("=", identificador, 0, None))
            elif tipo == "float":
                self.lista_interpretador.append(("=", identificador, 0, None))
            elif tipo == "string":
                self.lista_interpretador.append(("=", identificador, "", None))
        return

    def listaIdent(self):
        listaLocal = []
        self.consome(self.tokensnome["IDENT"])
        listaLocal.append(lista[self.index][1])
        listaResto = self.restoIdentList()
        if listaResto:
            listaLocal.extend(listaResto)
        return listaLocal

    def restoIdentList(self):
        prox_index = self.index + 1
        lista_tupla_prox = lista[prox_index]
        listaLocal = []
        if lista_tupla_prox[0] == self.tokensnome[","]:
            self.consome(self.tokensnome[","])
            self.consome(self.tokensnome["IDENT"])
            listaLocal.append(lista[self.index][1])
            listaResto = self.restoIdentList()
            if listaResto:
                listaLocal.extend(listaResto)
        return listaLocal

    def restoDeclaration(self):
        prox_index = self.index + 1
        lista_tupla_prox = lista[prox_index]
        if lista_tupla_prox[0] == self.tokensnome["IDENT"]:
            self.declaration()
            self.restoDeclaration()
        else:
            return

    def typefunc(self):
        prox_index = self.index + 1
        lista_tupla_prox = lista[prox_index]
        if lista_tupla_prox[0] == self.tokensnome["interger"]:
            self.consome(self.tokensnome["interger"])
            return "int"
        elif lista_tupla_prox[0] == self.tokensnome["real"]:
            self.consome(self.tokensnome["real"])
            return "float"
        elif lista_tupla_prox[0] == self.tokensnome["string"]:
            self.consome(self.tokensnome["string"])
            return "string"
        else:
            print("ERRO NA LINHA: ", lista_tupla_prox)
            print("TOKENS ESPERADOS: interger real string")
            sys.exit()
            return
        return

    # ------------------------------------
    # instrucoes dos programas
    # ------------------------------------

    def bloco(self):
        self.consome(self.tokensnome["begin"])
        self.stmtList()
        self.consome(self.tokensnome["end"])
        self.consome(self.tokensnome[";"])
        return

    def stmtList(self):
        prox_index = self.index + 1
        lista_tupla_prox = lista[prox_index]
        if lista_tupla_prox[0] in (
            self.tokensnome["interger"],
            self.tokensnome["for"],
            self.tokensnome["write"],
            self.tokensnome["read"],
            self.tokensnome["begin"],
            self.tokensnome["if"],
            self.tokensnome["IDENT"],
            self.tokensnome["while"],
            self.tokensnome[";"],
        ):
            self.stmt()
            self.stmtList()
            return
        else:
            return

    # Com base na gramatica miniC e usar o sintatico que o Eduardo mandou para fazer essa parte (desconsiderar a multiplicação) tem que mudar a string no expr
    def stmt(self):
        prox_index = self.index + 1
        lista_tupla_prox = lista[prox_index]
        if lista_tupla_prox[0] == self.tokensnome["for"]:
            self.forStmt()
        elif (
            lista_tupla_prox[0] == self.tokensnome["read"]
            or lista_tupla_prox[0] == self.tokensnome["write"]
        ):
            self.ioStmt()
        elif lista_tupla_prox[0] == self.tokensnome["while"]:
            self.whileStmt()
        elif lista_tupla_prox[0] == self.tokensnome["IDENT"]:
            self.atrib()
        elif lista_tupla_prox[0] == self.tokensnome["if"]:
            self.ifStmt()
        elif lista_tupla_prox[0] == self.tokensnome["begin"]:
            self.bloco()
        elif lista_tupla_prox[0] == self.tokensnome[";"]:
            self.consome(self.tokensnome[";"])
        else:
            print("ERRO NA LINHA: ", lista_tupla_prox)
            print("TOKENS ESPERADOS: begin if IDENT while read write for")
            sys.exit()
        return

    # ---------------------------
    # descricao das instrucoes
    # ---------------------------

    # comando for
    # TODO: deixar o atrib igual ao declarations, colocar duas label(colocar gerador de label) antes de stmt verificar se o identificador chegou no endFor e chamar o jump para a label correspondente
    def forStmt(self):
        self.consome(self.tokensnome["for"])
        self.atrib()
        self.consome(self.tokensnome["to"])
        isIdentificador, valor = self.endFor()
        self.consome(self.tokensnome["do"])
        self.stmt()
        labelVerdadeiro = self.gerarLabel("forVerdadeiro")
        labelFalso = self.gerarLabel("forFalso")
        self.lista_interpretador.append(("JUMP", labelVerdadeiro, None, None))
        self.lista_interpretador.append(("JUMP", labelFalso, None, None))
        return

    def endFor(self):
        prox_index = self.index + 1
        lista_tupla_prox = lista[prox_index]
        if lista_tupla_prox[0] == self.tokensnome["IDENT"]:
            self.consome(self.tokensnome["IDENT"])
            return True, lista[self.index][1]
        elif lista_tupla_prox[0] == self.tokensnome["interger"]:
            self.consome(self.tokensnome["interger"])
            return False, lista[self.index][1]
        else:
            print("ERRO NA LINHA: ", lista_tupla_prox)
            print("TOKENS ESPERADOS: IDENT interger")
            sys.exit()

    # comandos de IO

    def ioStmt(self):
        prox_index = self.index + 1
        lista_tupla_prox = lista[prox_index]
        if lista_tupla_prox[0] == self.tokensnome["read"]:
            self.consome(self.tokensnome["read"])
            self.consome(self.tokensnome["("])
            self.consome(self.tokensnome["IDENT"])
            operador = lista[self.index][1]
            self.consome(self.tokensnome[")"])
            self.consome(self.tokensnome[";"])
            self.lista_interpretador.append(("CALL", "SCAN", operador, None))
        elif lista_tupla_prox[0] == self.tokensnome["write"]:
            self.consome(self.tokensnome["write"])
            self.consome(self.tokensnome["("])
            self.outList()
            self.consome(self.tokensnome[")"])
            self.consome(self.tokensnome[";"])
        return

    def outList(self):
        self.out()
        self.restoOut()
        return

    def restoOut(self):
        prox_index = self.index + 1
        lista_tupla_prox = lista[prox_index]
        if lista_tupla_prox[0] == self.tokensnome[","]:
            self.consome(self.tokensnome[","])
            self.outList()
        return

    def out(self):
        prox_index = self.index + 1
        lista_tupla_prox = lista[prox_index]
        if lista_tupla_prox[0] == self.tokensnome["STR"]:
            self.consome(self.tokensnome["STR"])
            self.lista_interpretador.append(
                ("CALL", "PRINT", lista[self.index][1], None)
            )
        elif lista_tupla_prox[0] == self.tokensnome["IDENT"]:
            self.consome(self.tokensnome["IDENT"])
            self.lista_interpretador.append(
                ("CALL", "PRINT", None, lista[self.index][1])
            )
        elif lista_tupla_prox[0] == self.tokensnome["interger"]:
            self.consome(self.tokensnome["interger"])
            self.lista_interpretador.append(
                ("CALL", "PRINT", lista[self.index][1], None)
            )
        elif lista_tupla_prox[0] == self.tokensnome["real"]:
            self.consome(self.tokensnome["real"])
            self.lista_interpretador.append(
                ("CALL", "PRINT", lista[self.index][1], None)
            )
        else:
            print("ERRO NA LINHA: ", lista_tupla_prox)
            print("TOKENS ESPERADOS: IDENT STR interger real")
            sys.exit()
            return
        return

    # comando while

    def whileStmt(self):
        self.consome(self.tokensnome["while"])
        labelInicio = self.gerarLabel("whileInicio")
        labelFim = self.gerarLabel("whileFim")
        self.lista_interpretador.append(("LABEL", labelInicio, None, None))
        self.expr()
        self.lista_interpretador.append(("JUMP_IF_FALSE", labelFim, None, None))
        self.stmt()
        self.lista_interpretador.append(("JUMP", labelInicio, None, None))
        self.lista_interpretador.append(("LABEL", labelFim, None, None))
        return

    # comando if

    def ifStmt(self):
        self.consome(self.tokensnome["if"])
        self.expr()
        self.consome(self.tokensnome["then"])
        self.stmt()
        self.elsePart()
        return

    def elsePart(self):
        prox_index = self.index + 1
        lista_tupla_prox = lista[prox_index]
        if lista_tupla_prox[0] == self.tokensnome["else"]:
            self.consome(self.tokensnome["else"])
            self.stmt()
        else:
            return
        return

    # ------------------------------
    # expressoes
    # ------------------------------

    def atrib(self):
        self.consome(self.tokensnome["IDENT"])
        identificador = self.lista[self.index][1]
        self.consome(self.tokensnome[":="])  # Corrigir para ":=" em vez de "=:"
        valor = self.expr()
        self.lista_interpretador.append(("=", identificador, valor, None))
        return

    def expr(self):
        valor = self.orfunc()
        return valor

    def orfunc(self):
        self.andfunc()
        self.restoOr()
        return

    def restoOr(self):
        prox_index = self.index + 1
        lista_tupla_prox = lista[prox_index]
        if lista_tupla_prox[0] == self.tokensnome["or"]:
            self.consome(self.tokensnome["or"])
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
        if lista_tupla_prox[0] == self.tokensnome["and"]:
            self.consome(self.tokensnome["and"])
            self.notfunc()
            self.restoAnd()
        else:
            return
        return

    def notfunc(self):
        prox_index = self.index + 1
        lista_tupla_prox = lista[prox_index]
        if lista_tupla_prox[0] == self.tokensnome["not"]:
            self.consome(self.tokensnome["not"])
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
        if lista_tupla_prox[0] == self.tokensnome["=="]:
            self.consome(self.tokensnome["=="])
            self.add()
        elif lista_tupla_prox[0] == self.tokensnome["<>"]:
            self.consome(self.tokensnome["<>"])
            self.add()
        elif lista_tupla_prox[0] == self.tokensnome["<"]:
            self.consome(self.tokensnome["<"])
            self.add()
        elif lista_tupla_prox[0] == self.tokensnome[">"]:
            self.consome(self.tokensnome[">"])
            self.add()
        elif lista_tupla_prox[0] == self.tokensnome["<="]:
            self.consome(self.tokensnome["<="])
            self.add()
        elif lista_tupla_prox[0] == self.tokensnome[">="]:
            self.consome(self.tokensnome[">="])
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
        if lista_tupla_prox[0] == self.tokensnome["+"]:
            self.consome(self.tokensnome["+"])
            self.mult()
            self.restoAdd()
        elif lista_tupla_prox[0] == self.tokensnome["-"]:
            self.consome(self.tokensnome["-"])
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
        if lista_tupla_prox[0] == self.tokensnome["*"]:
            self.consome(self.tokensnome["*"])
            self.uno()
            self.restoMult()
        elif lista_tupla_prox[0] == self.tokensnome["/"]:
            self.consome(self.tokensnome["/"])
            self.uno()
            self.restoMult()
        elif lista_tupla_prox[0] == self.tokensnome["mod"]:
            self.consome(self.tokensnome["mod"])
            self.uno()
            self.restoMult()
        elif lista_tupla_prox[0] == self.tokensnome["div"]:
            self.consome(self.tokensnome["div"])
            self.uno()
            self.restoMult()
        else:
            return
        return

    def uno(self):
        prox_index = self.index + 1
        lista_tupla_prox = lista[prox_index]
        if lista_tupla_prox[0] == self.tokensnome["+"]:
            self.consome(self.tokensnome["+"])
            self.uno()
        elif lista_tupla_prox[0] == self.tokensnome["-"]:
            self.consome(self.tokensnome["-"])
            self.uno()
        else:
            self.factor()
        return

    def factor(self):
        prox_index = self.index + 1
        lista_tupla_prox = self.lista[prox_index]
        if (
            lista_tupla_prox[0] == self.tokensnome["interger"]
        ):  # Corrigir para "integer"
            self.consome(self.tokensnome["interger"])  # Corrigir para "integer"
            return self.lista[self.index][1]
        elif lista_tupla_prox[0] == self.tokensnome["real"]:
            self.consome(self.tokensnome["real"])
            return self.lista[self.index][1]
        elif lista_tupla_prox[0] == self.tokensnome["IDENT"]:
            self.consome(self.tokensnome["IDENT"])
            return self.lista[self.index][1]
        elif lista_tupla_prox[0] == self.tokensnome["("]:
            self.consome(self.tokensnome["("])
            valor = self.expr()
            self.consome(self.tokensnome[")"])
            return valor
        elif lista_tupla_prox[0] == self.tokensnome["STR"]:
            self.consome(self.tokensnome["STR"])
            return self.lista[self.index][1]
        return None


# ---------
# the end
# ---------

if __name__ == "__main__":
    import lexico, sys

    if len(sys.argv) > 1:
        lista = lexico.main(sys.argv[1])
        AnSint = AnalisadorSintatico(lista)
        listaDoInterpretador = AnSint.function()
        print(listaDoInterpretador)