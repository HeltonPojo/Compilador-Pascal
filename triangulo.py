
# nota1 = int(input('Insira a nota1'))
# nota2 = int(input('Insira a nota2'))
# nota3 = int(input('Insira a nota3'))
# media = (nota1 + nota2 + nota3)/3
# if (media >= 6)
#     return true
# return false
from interpretador import Interpretador

def programa():
    l = [("CALL", "SCAN", "lado1", None),
         ("CALL", "SCAN", "lado2", None),
         ("CALL", "SCAN", "lado3", None),
         ("+", "soma12", "lado1", "lado2"),
         ("+", "soma13", "lado1", "lado3"),
         ("+", "soma32", "lado3", "lado2"),
         (">", "valida1", "soma12", "lado3"),
         (">", "valida2", "soma13", "lado2"),
         (">", "valida3", "soma32", "lado1"),
         ("IF", "valida1", "EhTringulo1", "NaoEh"),
         ("LABEL", "EhTringulo1", None, None),
         ("IF", "valida2", "EhTringulo2", "NaoEh"),
         ("LABEL", "EhTringulo2", None, None),
         ("IF", "valida3", "EhTringulo3", "NaoEh"),
         ("LABEL", "EhTringulo3", None, None),
         ("CALL", "PRINT", "É Triangulo", None),
         ("JUMP", "Fim", None, None),
         ("LABEL", "NaoEh", None, None),
         ("CALL", "PRINT", "Não é triangulo", None),
         ("LABEL", "Fim", None, None)
         ]

    interpretador = Interpretador()
    interpretador.carregar_labels(l)
    interpretador.executar(l)

programa()
