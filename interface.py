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


num_estados = st.number_input('Número de estados', min_value=0, step=1, value=len(automato.estados))
estados = list(automato.estados)
estados.sort()

# Definição dos estados
for i in range(num_estados):
    if i<len(automato.estados):
        estado = st.text_input(f'Nome do estado {i}', key=f'estado_{i}',value=(estados[i]))
        inicial = st.checkbox(f'Estado inicial {i}', key=f'inicial_{i}',value=(automato.estado_inicial==estados[i]))
        aceitacao = st.checkbox(f'Estado de aceitação {i}', key=f'aceitacao_{i}',value=(estados[i] in automato.estados_aceitacao))
    else:
        estado = st.text_input(f'Nome do estado {i}', key=f'estado_{i}')
        inicial = st.checkbox(f'Estado inicial {i}', key=f'inicial_{i}')
        aceitacao = st.checkbox(f'Estado de aceitação {i}', key=f'aceitacao_{i}')
    if estado:
        automato.adicionar_estado(estado, inicial, aceitacao)

alfabeto = st.text_input('Alfabeto',key='alfabeto',value=(str(automato.alfabeto).replace('{','').replace('}','').replace('\'','') if len(automato.alfabeto)>0 else ''))
alfabeto = alfabeto.replace(' ','').split(',')
if alfabeto == ['']:
    alfabeto = []
    
automato.alfabeto = alfabeto
# Definição das transições
for i in range(len(automato.estados)):
    for j in alfabeto:

        destino = st.text_input(f'Destino da transição {estados[i]} {j}', key=f'origem_{i}{j}',value=str(automato.transicoes_estado(estados[i],j)).replace('{','').replace('\'','').replace('}',''))

        if (destino in automato.estados):
            if(',' in destino):
                for no in destino.replace(' ','').split(','):
                    automato.adicionar_transicao(estados[i], j, no)
            else:
                automato.adicionar_transicao(estados[i], j, destino)

if automato.estado_inicial!=None:
    st.text("O automato inserido é um AFD" if automato.is_AFD() else "O automato inserido não é um AFD")
    st.text("O automato inserido é completo" if automato.is_complete() else "O automato inserido não é completo")
    st.text("Expressão Regular: "+automato.to_er())

    if st.button('Minimizar'):
        automato = automato.minimizar()

    image = automato.criar_imagem()
    st.graphviz_chart(image,use_container_width=True)
    image = automato.render_image(image)
    image = open(image,'rb')
    st.download_button('Baixar',data=image,file_name='automato.png',mime="image/png")