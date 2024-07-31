from AutomatoFinito import AutomatoFinito
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

# Exemplo de uso
estados = {"q0", "q1", "q2"}
alfabeto = {"a", "b"}
transicoes = {
    ("q0", "a"): {"q1"},
    ("q1", "a"): {"q0"},
    ("q1", "b"): {"q1"},
    ("q0", "b"): {"q2"},
    ("q2", "b"): {"q1", "q0"}
}
estado_inicial = "q0"
estados_aceitacao = {"q1", "q2"}
automatoex = AutomatoFinito(estados, alfabeto, transicoes, estado_inicial, estados_aceitacao)

# Leitura do autômato e das palavras
automatos = ler_automatos_pasta('Automatos')
palavras = ler_palavras_arquivo('palavras.txt')

for automato in automatos:
    aux = automato.minimizar()
    # Impressão dos autômatos minimizados e expressões regulares
    print("\n\nAutomato:")
    print(automato)
    print("\nMinimização:")
    print(aux)
    print("\nER:")
    print(automato.to_er())

    # Teste das palavras com o método simular
    print("\nResultados da simulação das palavras:")
    for palavra in palavras:
        resultado = automato.simular(palavra)
        print(f"A palavra '{palavra}' é aceita pelo autômato 1? {'Sim' if resultado else 'Não'}")