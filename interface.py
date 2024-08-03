import streamlit as st
from Utils import *
from AutomatoFinito import AutomatoFinito

# Criação da interface Streamlit
st.title('Autômato Finito Determinístico')

automato = AutomatoFinito()

arquivo_upload = st.file_uploader('Carregar arquivo de descrição do autômato', type=['txt'])

if arquivo_upload is not None:
    pasta='uploads'
    caminho_arquivo = os.path.join(pasta, arquivo_upload.name)
    if not os.path.exists(pasta):
            os.makedirs(pasta)

    with open(caminho_arquivo, 'wb') as f:
        f.write(arquivo_upload.getbuffer())

    automato = ler_automato_arquivo(caminho_arquivo)
    
    st.write('Estados:', ', '.join(automato.estados))
    st.write('Alfabeto:', ', '.join(automato.alfabeto))
    st.write('Estado Inicial:', automato.estado_inicial)
    st.write('Estados de Aceitação:', ', '.join(automato.estados_aceitacao))
    st.write('Transições:')
    for (origem, simbolo), destinos in automato.transicoes.items():
        for destino in destinos:
            st.write(f'{origem} --{simbolo}--> {destino}')
else:
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

    image = automato.criar_imagem()

    st.graphviz_chart(image,use_container_width=True)

    image = automato.render_image(image)

    image = open(image,'rb')
    st.download_button('Baixar',data=image,file_name='automato.png',mime="image/png")
else:
    st.write('Por favor, carregue um arquivo de descrição do autômato no formato especificado.')
