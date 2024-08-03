from Utils import *

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
    print(f"\nÉ completo? {'Sim' if (automato.is_complete()) else 'Não'}")
    
    automato.render_image(automato.criar_imagem())

    # Teste das palavras com o método simular
    print("\nResultados da simulação das palavras:")
    for palavra in palavras:
        resultado = automato.simular(palavra)
        print(f"A palavra '{palavra}' é aceita pelo autômato 1? {'Sim' if resultado else 'Não'}")