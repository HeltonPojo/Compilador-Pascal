
# nota1 = int(input('Insira a nota1'))
# nota2 = int(input('Insira a nota2'))
# nota3 = int(input('Insira a nota3'))
# media = (nota1 + nota2 + nota3)/3
# if (media >= 6)
#     return true
# return false
from interpretador import Interpretador

def programa():
    l = [("+", "i", 0, 0),
         ("LABEL", "Loop", None, None),
         ("+", "i", "i", 1),
         ("CALL", "PRINT", None, "i"),
         (">=", "valida", "i", 10),
         ("IF", "valida", "Fim", "Loop"),
         ("LABEL", "Fim", None, None)
         ]

    interpretador = Interpretador()
    interpretador.carregar_labels(l)
    interpretador.executar(l)

programa()
