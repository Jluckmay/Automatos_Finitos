from AutomatoFinito import AutomatoFinito
from MaquinaTuring import MaquinaTuring
import os

# Função para ler um autômato de um arquivo
def ler_automato_arquivo(arquivo):
    with open(arquivo, 'r') as f:
        linhas = f.readlines()

    # Leitura dos estados
    estados = set(linhas[0].strip().split(":")[1].split(","))
    # Leitura do alfabeto
    alfabeto = set(linhas[1].strip().split(":")[1].split(","))
    # Inicialização das transições
    transicoes = {}
    for transicao in linhas[3:-2]:
        partes = transicao.strip().split()
        estado_origem = partes[0]
        simbolo = partes[1]
        estados_destino = set(partes[2].split(","))
        transicoes[(estado_origem, simbolo)] = estados_destino

    # Leitura do estado inicial
    estado_inicial = linhas[-2].strip().split(":")[1]
    # Leitura dos estados de aceitação
    estados_aceitacao = set(linhas[-1].strip().split(":")[1].split(","))

    return AutomatoFinito(estados, alfabeto, transicoes, estado_inicial, estados_aceitacao)

# Função para ler palavras de um arquivo
def ler_palavras_arquivo(arquivo):
    with open(arquivo, 'r') as f:
        palavras = f.read().splitlines()
    return palavras

# Função para ler arquivos de automatos em uma pasta
def ler_automatos_pasta(pasta):

    if not os.path.exists(pasta):
            os.makedirs(pasta)
            
    automatos = []
    for nome_arquivo in os.listdir(pasta):
        if nome_arquivo.endswith('.txt'):
            caminho_arquivo = os.path.join(pasta, nome_arquivo)
            automato = ler_automato_arquivo(caminho_arquivo)
            automatos.append(automato)
    return automatos

# Método para verificar se dois autômatos mínimos são equivalentes
def automatos_equivalentes(automato1, automato2):
    return (automato1.to_er() == automato2.to_er())

# Função para ler uma Máquina de Turing de um arquivo
def ler_arquivo_maquina_turing(caminho_arquivo):
    with open(caminho_arquivo, 'r') as arquivo:
        linhas = arquivo.readlines()

    estados = set()
    alfabeto = set()
    fita_alfabeto = set()
    transicoes = {}
    estado_inicial = None
    simbolo_branco = None
    estados_aceitacao = set()

    for linha in linhas:
        linha = linha.strip()
        if not linha or linha.startswith('#'):
            continue
        
        if linha.startswith('estados:'):
            estados = set(linha.split(':')[1].split(','))
        elif linha.startswith('alfabeto:'):
            alfabeto = set(linha.split(':')[1].split(','))
        elif linha.startswith('fita_alfabeto:'):
            fita_alfabeto = set(linha.split(':')[1].split(','))
        elif linha.startswith('transicoes:'):
            continue
        elif linha.startswith('estado_inicial:'):
            estado_inicial = linha.split(':')[1]
        elif linha.startswith('simbolo_branco:'):
            simbolo_branco = linha.split(':')[1]
        elif linha.startswith('estados_aceitacao:'):
            estados_aceitacao = set(linha.split(':')[1].split(','))
        else:
            partes = linha.split()
            if len(partes) == 5:
                estado_atual, simbolo_atual, novo_estado, novo_simbolo, direcao = partes
                transicoes[(estado_atual, simbolo_atual)] = (novo_estado, novo_simbolo, direcao)

    maquina = MaquinaTuring(estados,alfabeto,fita_alfabeto,transicoes,estado_inicial,simbolo_branco,estados_aceitacao)
    return maquina

