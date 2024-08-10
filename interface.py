from Utils import *
import streamlit as st

# Criação da interface Streamlit
st.title('Autômato Finito Determinístico')

# Lista para armazenar autômatos
automatos = []

key = 0

# Carregar autômatos de arquivos salvos (opcional, se desejar manter persistência entre sessões)
if os.path.exists('uploads'):
    automatos = ler_automatos_pasta('uploads')


# Função para salvar autômatos em arquivos txt
def salvar_automato(automato,nome):
    pasta='uploads'
    texto =''
    if not(automato in automatos):
        texto+='estados:'
        for i in range(len(automato.estados)):
            texto+=str(list(automato.estados)[i])
            if i < len(automato.estados)-1:
                texto+=','
            else:
                texto+='\n'

        texto+='alfabeto:'
        for i in range(len(automato.alfabeto)):
            texto+=str(automato.alfabeto[i])
            if i < len(automato.alfabeto)-1:
                texto+=','
            else:
                texto+='\n'

        texto+='transicoes:'
        for (estado,simbolo),destino in automato.transicoes:
            texto+=f'{estado} {simbolo} {destino}'
            texto+='\n'

        texto+=f'estado_inicial:{automato.estado_inicial}\n'

        texto+='estados_aceitacao:'
        for i in range(len(automato.estados_aceitacao)):
            texto+=str(list(automato.estados_aceitacao)[i])
            if i < len(automato.estados_aceitacao)-1:
                texto+=','
            else:
                texto+='\n'

        with open(os.path.join(pasta, nome),'w') as f:
            f.write(texto)
            f.close()

# Função para gerar e exibir uma representação gráfica do autonomo
def exibir_imagem(automato, nome, key):
    pasta='Imagens'
    image = automato.criar_imagem()
    st.graphviz_chart(image,use_container_width=True)

    f = os.path.join(pasta, nome)+'.png'

    if not os.path.exists(f):
        f = automato.render_image(image,nome)
    
    image = open(f,'rb')
    st.download_button('Baixar',data=image,file_name=nome,mime="image/png", key=key)
    
    return key+1


arquivo_upload = st.file_uploader('Carregar arquivo de descrição do autômato', type=['txt'])

if arquivo_upload is not None:
    pasta='uploads'
    caminho_arquivo = os.path.join(pasta, f'automato{len(automatos)}.'+'txt')
    if not os.path.exists(pasta):
            os.makedirs(pasta)

    with open(caminho_arquivo, 'wb') as f:
        f.write(arquivo_upload.getbuffer())

    automato = ler_automato_arquivo(caminho_arquivo)
    automatos.append(automato)

# Seleção de autômatos para verificar equivalência e simular palavras
st.write('Selecione dois autômatos para verificar equivalência e simular palavras:')

op1 = st.selectbox('Selecione o primeiro autômato', range(len(automatos)), format_func=lambda x: f'Autômato {x+1}')

if op1!=None:
    automato = automatos[op1]
else:
    automato=AutomatoFinito()

num_estados = st.number_input('Número de estados',key=f'n_estados', min_value=0, step=1, value=len(automato.estados))
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

alfabeto = st.text_input('Alfabeto',key=f'alfabeto',value=(str(automato.alfabeto).replace('[','').replace(']','').replace('{','').replace('}','').replace('\'','') if len(automato.alfabeto)>0 else ''))
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


if op1 is None:
    op1 = 0

if automato.estado_inicial!=None:
    st.text("O automato inserido é um AFD" if automato.is_AFD() else "O automato inserido não é um AFD")
    if(not automato.is_AFD()):
        if st.button('Converter para AFD'):
            automato = automato.to_afd()
            salvar_automato(automato,f'automato_AFD{op1}.txt')
            key = exibir_imagem(automato,f'automato_AFD{op1}', key)

    st.text("O automato inserido é completo" if automato.is_complete() else "O automato inserido não é completo")
    st.text("Expressão Regular: "+automato.to_er())

    if st.button('Minimizar'):
        automato = automato.minimizar()
        salvar_automato(automato,f'automato_Min{op1}.txt')
        key = exibir_imagem(automato,f'automato_Min{op1}',key)
    else:
        key = exibir_imagem(automato,f'automato{op1}',key)

    automatos[op1] = automato




op2 = st.selectbox('Selecione o segundo autômato', range(len(automatos)), format_func=lambda x: f'Autômato {x+1}')
if op2 is None:
    automato = AutomatoFinito()
else:
    automato = automatos[op2]

if op2 is None:
    op2 = 0

if automato.estado_inicial!=None:
    st.text("O automato inserido é um AFD" if automato.is_AFD() else "O automato inserido não é um AFD")
    if(not automato.is_AFD()):
        if st.button('Converter para AFD',key=f'converter{op2}'):
            automato = automato.to_afd()
            salvar_automato(automato,f'automato_AFD{op2}.txt')
            key = exibir_imagem(automato,f'automato_AFD{op2}',key)

    st.text("O automato inserido é completo" if automato.is_complete() else "O automato inserido não é completo")
    st.text("Expressão Regular: "+automato.to_er())

    if st.button('Minimizar',key=f'minimizar{op2}'):
        automato = automato.minimizar()
        salvar_automato(automato,f'automato_Min{op2}.txt')
        key = exibir_imagem(automato,f'automato_Min{op2}',key)
    else:
        key = exibir_imagem(automatos[op2],f'automato{op2}',key)

    automatos[op2] = automato



if st.button('Verificar Equivalência'):
    equivalente =automatos_equivalentes(automatos[op1],automato)
    st.write('Os autômatos são equivalentes' if equivalente else 'Os autômatos não são equivalentes')

palavra = st.text_input('Digite a palavra para simulação')
if st.button('Simular Palavra'):
    resultado1 = automatos[op1].simular(palavra)
    resultado2 = automatos[op2].simular(palavra)
    st.write(f'Resultado no Autômato {op1+1}: {"Aceita" if resultado1 else "Rejeitada"}')
    st.write(f'Resultado no Autômato {op2+1}: {"Aceita" if resultado2 else "Rejeitada"}')
