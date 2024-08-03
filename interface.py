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

estados = list(automato.estados)
estados.sort()

num_estados = st.number_input('Número de estados', min_value=0, step=1, value=len(automato.estados))

# Definição dos estados
for i in range(num_estados):
    estado = st.text_input(f'Nome do estado {i+1}', key=f'estado_{i}',value=estados[i])
    inicial = st.checkbox(f'Estado inicial {i+1}', key=f'inicial_{i}',value=(automato.estado_inicial==estados[i]))
    aceitacao = st.checkbox(f'Estado de aceitação {i+1}', key=f'aceitacao_{i}',value=(estados[i] in automato.estados_aceitacao))
    if estado:
        automato.adicionar_estado(estado, inicial, aceitacao)

# Definição das transições
num_transicoes = st.number_input('Número de transições', min_value=0, step=1,value=(len(automato.transicoes)))
for i in range(num_estados):
    for j in automato.alfabeto:
        origem = st.text_input(f'Estado de origem {i+1}', key=f'origem_{i}{j}',value=estados[i])
        simbolo = st.text_input(f'Símbolo {i+1}', key=f'simbolo_{i}{j}', value=j)
        destino = st.text_input(f'Estado de destino {i+1}', key=f'destino_{i}{j}',value=str(automato.transicoes_estado(estados[i],j)).replace('{','').replace('\'','').replace('}',''))
        if origem and simbolo and destino:
            if(',' in destino):
                for no in destino.replace(' ','').split(','):
                    automato.adicionar_transicao(origem, simbolo, no)

# Gerar imagem
if st.button('Gerar imagem'):

    image = automato.criar_imagem()

    st.graphviz_chart(image,use_container_width=True)

    image = automato.render_image(image)

    image = open(image,'rb')
    st.download_button('Baixar',data=image,file_name='automato.png',mime="image/png")
else:
    st.write('Por favor, carregue um arquivo de descrição do autômato no formato especificado.')
