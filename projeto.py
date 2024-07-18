from AutomatoFinito import AutomatoFinito

def ler_automato_arquivo(arquivo):
    with open(arquivo, 'r') as f:
        linhas = f.readlines()

    estados = set(linhas[0].strip().split(":")[1].split(","))
    alfabeto = set(linhas[1].strip().split(":")[1].split(","))
    transicoes = {}
    for transicao in linhas[3:-2]:
        partes = transicao.strip().split()
        estado_origem = partes[0]
        simbolo = partes[1]
        estados_destino = set(partes[2].split(","))
        transicoes[(estado_origem, simbolo)] = estados_destino

    estado_inicial = linhas[-2].strip().split(":")[1]
    estados_aceitacao = set(linhas[-1].strip().split(":")[1].split(","))

    return AutomatoFinito(estados, alfabeto, transicoes, estado_inicial, estados_aceitacao)

def ler_palavras_arquivo(arquivo):
    with open(arquivo, 'r') as f:
        palavras = f.read().splitlines()
    return palavras

# Método para verificar se dois autômatos mínimos são equivalentes
def automatos_sao_equivalentes(automato1, automato2):
    return (automato1.converter_para_er()==automato2.converter_para_er())


# # Exemplo de uso
# estados = {"q0", "q1", "q2"}
# alfabeto = {"a", "b"}
# transicoes = {
#     ("q0", "a"): {"q1"},
#     ("q0", "b"): {"q2"},
#     ("q1", "a"): {"q0"},
#     ("q1", "b"): {"q1"},
#     ("q2", "b"): {"q1","q0"}
# }
# estado_inicial = "q0"
# estados_aceitacao = {"q2","q1"}

# Leitura do automato e das palavras
automato2 = ler_automato_arquivo('automato2.txt')
automato = ler_automato_arquivo('automato.txt')
palavras = ler_palavras_arquivo('palavras.txt')

# Impressão
print("Automato 1:")
print(automato)
print("\nAutomato 2:")
print(automato2)
print("\nER1:")
print(automato.to_er())
print("\nER2:")
print(automato2.to_er())

if automatos_sao_equivalentes(automato,automato2):
    print("\nOs automatos são equivalentes")
else:
    print("\nOs automatos não são equivalentes")

print(f"ER: {automato.minimizar().to_er()}")