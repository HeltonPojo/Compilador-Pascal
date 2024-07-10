# nota1 = int(input('Insira a nota1'))
# nota2 = int(input('Insira a nota2'))
# nota3 = int(input('Insira a nota3'))
# media = (nota1 + nota2 + nota3)/3
# if (media >= 6)
#     return true
# return false
from interpretador import Interpretador

def programa():
    l = [("CALL", "SCAN", "nota1", None),
         ("CALL", "SCAN", "nota2", None),
         ("CALL", "SCAN", "nota3", None),
         ("+", "media", "nota1", "nota2"),
         ("+", "media", "media", "nota3"),
         ("/", "media", "media", 3),
         (">=", "media", "media", 6),
         ("IF", "media", 9, 11),
         ("CALL", "PRINT", "Aprovado", None),
         ("JUMP", 12, None, None),
         ("CALL", "PRINT", "Reprovado", None)
         ]

    interpretador = Interpretador()
    interpretador.carregar_labels(l)
    interpretador.executar(l)

programa()
