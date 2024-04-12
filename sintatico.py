lista, index = [] , 0

tokensnome = {'+' : 1,
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
              ',': 36,
              '.': 37,
              '(': 38,
              ')': 39,
              '[': 40,
              ']': 41,
              '{': 42,
              '}': 43,
              'STR': 44,
              'IDENT': 45}

def function():
    consome(tokensnome['program'])#program
    consome()#IDENT
    consome()#;
    declarations()
    consome()#begin
    stmtList()
    consome()#end
    consome()#.


def declarations():
    consome()#var
    declaration()
    restoDeclaration()
    return

def restoDeclaration():
    prox_index = index + 1
    lista_tupla_prox = lista[prox_index]
    if(lista_tupla_prox[2] == tokensnome['IDENT']):
        declaration()
        restoDeclaration()
    else:
        return

def declaration():
    lsitaIdent()
    consome()#:
    typefunc()
    consome()#;
    return

def lsitaIdent():
    consome()#IDENT
    restoIdentList()    
    return

def restoIdentList():
    prox_index = index + 1
    lista_tupla_prox = lista[prox_index]
    if(lista_tupla_prox[2] == tokensnome[',']):
        consome()#,
        consome()#IDENT
        restoIdentList()
    else:
        return

def typefunc():
    prox_index = index + 1
    lista_tupla_prox = lista[prox_index]
    if(lista_tupla_prox[2] == tokensnome['interger']):
        consome(tokensnome['interger'])
    elif(lista_tupla_prox[2] == tokensnome['real']):
        consome(tokensnome['real'])
    elif(lista_tupla_prox[2] == tokensnome['string']):
        consome(tokensnome['string'])
    else:
        #expect
        return
    
def consome(token_esperado):
    index+=1
    lista_tupla = lista[index]
    if lista_tupla[2] == token_esperado:
       print('Terminal inesperado')
       return
    else:
        print('Argumento não esperado')
        #execpt
        return

def stmtList():
    prox_index = index + 1
    lista_tupla_prox = lista[prox_index]
    if(lista_tupla_prox[2] == tokensnome['interger']):
        stmt()
    return

def stmt():
    prox_index = index + 1
    lista_tupla_prox = lista[prox_index]
    if(lista_tupla_prox[2] == tokensnome['interger']):
        ioStmt()
    return

def ioStmt():
    prox_index = index + 1
    lista_tupla_prox = lista[prox_index]
    if(lista_tupla_prox[2] == tokensnome['read']):
        consome(tokensnome['read'])
        consome(tokensnome['('])
        consome(tokensnome['IDENT'])
        consome(tokensnome[')'])
        consome(tokensnome[';'])
    elif(lista_tupla_prox[2] == tokensnome['write']):
        consome(tokensnome['write'])
        consome(tokensnome['('])
        out()
        consome(tokensnome[')'])
        consome(tokensnome[';'])
    return

def out():
    return