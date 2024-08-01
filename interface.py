import streamlit as st
import os
from AutomatoFinito import AutomatoFinito

# Criação da interface Streamlit
st.title('Autômato Finito Determinístico')

automato = AutomatoFinito()

# Definição dos estados
num_estados = st.number_input('Número de estados', min_value=1, step=1)
for i in range(num_estados):
    estado = st.text_input(f'Nome do estado {i+1}', key=f'estado_{i}')
    inicial = st.checkbox(f'Estado inicial {i+1}', key=f'inicial_{i}')
    aceitacao = st.checkbox(f'Estado de aceitação {i+1}', key=f'aceitacao_{i}')
    if estado:
        automato.adicionar_estado(estado, inicial, aceitacao)

# Definição das transições
num_transicoes = st.number_input('Número de transições', min_value=1, step=1)
for i in range(num_transicoes):
    origem = st.text_input(f'Estado de origem {i+1}', key=f'origem_{i}')
    simbolo = st.text_input(f'Símbolo {i+1}', key=f'simbolo_{i}')
    destino = st.text_input(f'Estado de destino {i+1}', key=f'destino_{i}')
    if origem and simbolo and destino:
        automato.adicionar_transicao(origem, simbolo, destino)

# Gerar imagem
if st.button('Gerar imagem'):
    caminho_imagem = automato.criar_imagem()
    if os.path.exists(caminho_imagem):
        st.image(caminho_imagem, caption='Autômato Finito', use_column_width=True)
    else:
        st.error('Erro ao gerar a imagem do autômato.')