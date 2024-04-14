import re
import sys

def ler_arquivo(nome_arquivo):
    with open(nome_arquivo, 'r') as arquivo:
        return arquivo.readlines()

def ler_tokens(nome_arquivo_tokens):
    with open(nome_arquivo_tokens, 'r') as arquivo_tokens:
        return arquivo_tokens.readlines()

def verificar_tokens(palavra_tkn, lista_tokens):
    linha_atual = 0
    for linha in lista_tokens:
        linha_atual += 1
        coluna_atual = 0
        palavras = re.findall(r'\w+|\S', linha)
        for palavra in palavras:
            coluna_atual = linha.find(palavra, coluna_atual)
            if palavra_tkn == palavra:
                return linha_atual, True
            coluna_atual += len(palavra)
    return linha_atual, False

def parser(arquivo, lista_tokens):
    tokens_encontrados = []
    linha_atual = 0
    for linha in arquivo:
        linha_atual += 1
        coluna_atual = 0
        palavras = re.findall(r'\w+|\S', linha)
        if '//' in linha:
            pass
        elif '"' in palavras or "'" in palavras:
            aspas_abertas = False
            string_lex = ''
            for i, palavra in enumerate(linha):
                if '"' == palavra or "'" == palavra and aspas_abertas:
                    string_lex += palavra
                    aspas_abertas = False
                    #Salvando String
                    tokens_encontrados.append((44, string_lex, linha_atual, coluna_atual))
                    string_lex = ''
                elif '"' in palavra or "'" in palavra or aspas_abertas:
                    string_lex += palavra
                    aspas_abertas = True
        else:
            for palavra in palavras:
                coluna_atual = linha.find(palavra, coluna_atual)
                token_linha, is_token = verificar_tokens(palavra, lista_tokens)
                if is_token:
                    tokens_encontrados.append((token_linha, palavra, linha_atual, coluna_atual))
                else:
                    #Salvando IDENT
                    tokens_encontrados.append((46, palavra, linha_atual, coluna_atual))
                coluna_atual += len(palavra)
    return tokens_encontrados



#def verificar_balanceamento_parentheses(arquivo):
#    abre_fecha = {'(': ')', '[': ']', '{': '}'}
#    pilha = []
#    for linha_num, linha in enumerate(arquivo, start=1):
#        for coluna_num, char in enumerate(linha, start=1):
#            if char in abre_fecha.keys():
#                pilha.append((char, linha_num, coluna_num))
#            elif char in abre_fecha.values():
#                if not pilha or abre_fecha[pilha.pop()[0]] != char:
#                    return False, (linha_num, coluna_num)
#    return not pilha, None

def main(nome_arquivo):
    nome_arquivo_tokens = 'tokens.txt'

    arquivo = ler_arquivo(nome_arquivo)
    lista_tokens = ler_tokens(nome_arquivo_tokens)

    tokens_encontrados = parser(arquivo, lista_tokens)

    lista_lexica = []
    for token_linha, lexima, linha, coluna in tokens_encontrados:
        lista_lexica.append((token_linha, lexima, linha, coluna))
    return lista_lexica

if __name__ == "__main__":
    if len(sys.argv) > 1:
        lista = main(sys.argv[1])
        print(lista)
    