from Utils import *

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