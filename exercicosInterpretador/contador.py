
# nota1 = int(input('Insira a nota1'))
# nota2 = int(input('Insira a nota2'))
# nota3 = int(input('Insira a nota3'))
# media = (nota1 + nota2 + nota3)/3
# if (media >= 6)
#     return true
# return false
from interpretador import Interpretador

def programa():
    l = [("CALL", "PRINT", 0, None)]

    interpretador = Interpretador()
    interpretador.carregar_labels(l)
    interpretador.executar(l)

programa()
