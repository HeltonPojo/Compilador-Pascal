
# lexico.py
# Este arquivo implementa o analisador léxico para o compilador de Pascal.
# Ele lê o código-fonte, identifica tokens e os classifica, preparando-os para a análise sintática.
# Funções de leitura de arquivos e verificação de tokens estão incluídas neste arquivo.

import re
import sys

# Função que lê o conteúdo de um arquivo de código-fonte
def ler_arquivo(nome_arquivo):
    # Abre o arquivo no modo de leitura e retorna uma lista de linhas
    with open(nome_arquivo, 'r') as arquivo:
        return arquivo.readlines()

# Função que lê os tokens de um arquivo de definição de tokens
def ler_tokens(nome_arquivo_tokens):
    # Abre o arquivo de tokens no modo de leitura e retorna uma lista de linhas
    with open(nome_arquivo_tokens, 'r') as arquivo_tokens:
        return arquivo_tokens.readlines()

# Função que verifica a correspondência de tokens em uma linha de código
def verificar_tokens(palavra_tkn, lista_tokens):
    linha_atual = 0  # Inicializa o contador de linhas
    for linha in lista_tokens:
        linha_atual += 1  # Incrementa o número da linha atual
        coluna_atual = 0  # Inicializa o contador de colunas
        # Encontra todas as palavras ou símbolos na linha usando expressão regular
        palavras = re.findall(r'\w+|==|<>|>|<|>=|<=|:=|\S', linha)
        for palavra in palavras:
            coluna_atual = linha.find(palavra, coluna_atual)  # Encontra a posição da palavra na linha
            if palavra_tkn == palavra:
                # Se o token corresponde à palavra, retorna a posição
                return (linha_atual, coluna_atual + 1)
            coluna_atual += len(palavra)  # Avança para a próxima coluna após a palavra
    return None  # Retorna None se o token não for encontrado

import re
import sys

def ler_arquivo(nome_arquivo):
# Lê o conteúdo do arquivo fornecido e retorna uma lista de linhas.
    with open(nome_arquivo, 'r') as arquivo:
        return arquivo.readlines()

# Lê o arquivo de tokens (tokens.txt) e retorna uma lista de tokens.
def ler_tokens(nome_arquivo_tokens):
    with open(nome_arquivo_tokens, 'r') as arquivo_tokens:
        return arquivo_tokens.readlines()
    
# Verifica se uma palavra está na lista de tokens e retorna a linha onde foi encontrada.
def verificar_tokens(palavra_tkn, lista_tokens):
    linha_atual = 0
    for linha in lista_tokens:
        linha_atual += 1
        coluna_atual = 0
        palavras = re.findall(r'\w+|==|<>|>|<|>=|<=|:=|\S|\s', linha)
        for palavra in palavras:
            coluna_atual = linha.find(palavra, coluna_atual)
            if palavra_tkn == palavra:
                return linha_atual, True
            coluna_atual += len(palavra)
    return linha_atual, False

# Processa o arquivo de entrada, identificando tokens em cada linha.
def parser(arquivo, lista_tokens):
    tokens_encontrados = []
    linha_atual = 0
    aspas_abertas = False
    string_lex = ''
    for linha in arquivo:
        linha_atual += 1
        coluna_atual = 0
        palavras = re.findall(r'\w+|==|<>|>|<|>=|<=|:=|\S|\s', linha)
        if '//' in linha:
            pass
        else:
            for palavra in palavras:
                if '"' == palavra or "'" == palavra and aspas_abertas:
                    string_lex += palavra
                    aspas_abertas = False
                    tokens_encontrados.append((45, string_lex, linha_atual, coluna_atual))
                    string_lex = ''
                elif '"' in palavra or "'" in palavra or aspas_abertas:
                    string_lex += palavra
                    aspas_abertas = True
                else:
                    coluna_atual = linha.find(palavra, coluna_atual)
                    token_linha, is_token = verificar_tokens(palavra, lista_tokens)
                    if is_token:
                        tokens_encontrados.append((token_linha, palavra, linha_atual, coluna_atual))
                    else:
                        tokens_encontrados.append((46, palavra, linha_atual, coluna_atual))
                    coluna_atual += len(palavra)
    return tokens_encontrados

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
    
