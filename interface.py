from Utils import *
import streamlit as st
from MaquinaTuring import MaquinaTuring



# Inicializando a sessão para armazenar o modo selecionado
if 'modo' not in st.session_state:
    st.session_state.modo = 'Automato Finito'



def definir_transicoes(maquina):
    transicoes = {}

    if maquina.transicoes != transicoes:
        transicoes = maquina.transicoes


    num_transicoes = st.number_input("Número de transições", min_value=0, value=len(transicoes), step=1)
    
    if(transicoes != {}):
        i=0
        for (atual, simbolo), (novo,simbolo_novo,dir) in transicoes.items():
            with st.expander(f"Transição {i+1}"):
                estado_atual = st.text_input(f"Estado atual (Transição {i+1})", value=atual)
                simbolo_atual = st.text_input(f"Símbolo atual na fita (Transição {i+1})",value=simbolo)
                novo_estado = st.text_input(f"Novo estado (Transição {i+1})",value=novo)
                novo_simbolo = st.text_input(f"Novo símbolo na fita (Transição {i+1})",value=simbolo_novo)
                direcao = st.selectbox(f"Direção da cabeça (Transição {i+1})", ['R', 'L','N'],index=['R', 'L','N'].index(dir))
                if estado_atual and simbolo_atual and novo_estado and novo_simbolo and direcao:
                    transicoes[(estado_atual, simbolo_atual)] = (novo_estado, novo_simbolo, direcao)
                i+=1
    else:
        for i in range(num_transicoes):
            with st.expander(f"Transição {i+1}"):
                estado_atual = st.text_input(f"Estado atual (Transição {i+1})")
                simbolo_atual = st.text_input(f"Símbolo atual na fita (Transição {i+1})")
                novo_estado = st.text_input(f"Novo estado (Transição {i+1})")
                novo_simbolo = st.text_input(f"Novo símbolo na fita (Transição {i+1})")
                direcao = st.selectbox(f"Direção da cabeça (Transição {i+1})", ['R', 'L'])
                if estado_atual and simbolo_atual and novo_estado and novo_simbolo and direcao:
                    transicoes[(estado_atual, simbolo_atual)] = (novo_estado, novo_simbolo, direcao)

    return transicoes

def interface_maquina_turing():
    st.title("Modo: Máquina de Turing")

    maquina = MaquinaTuring()

    arquivo_upload = st.file_uploader('Carregar arquivo de descrição do autômato', type=['txt'])

    if arquivo_upload is not None:
        pasta='uploads/turing'
        caminho_arquivo = os.path.join(pasta, f'maquinaTuring.'+'txt')
        if not os.path.exists(pasta):
                os.makedirs(pasta)

        with open(caminho_arquivo, 'wb') as f:
            f.write(arquivo_upload.getbuffer())

        maquina = ler_arquivo_maquina_turing(caminho_arquivo)

    # Entrada para definir os estados
    estados = st.text_input("Estados (separados por vírgula)", value=str(maquina.estados).replace('{','').replace('}','').replace('\'',''))
    estados = estados.split(',') if estados else []

    # Entrada para definir o alfabeto da fita
    fita_alfabeto = st.text_input("Alfabeto da fita (separado por vírgula)", value = str(maquina.alfabeto).replace('{','').replace('}','').replace('\'',''))
    fita_alfabeto = fita_alfabeto.split(',') if fita_alfabeto else []

    # Definir o símbolo branco
    branco = st.text_input("Símbolo branco", value=maquina.branco)

    # Estado inicial
    estado_inicial = st.text_input("Estado inicial", value=maquina.estado_inicial)

    # Definir estados finais
    estados_finais = st.text_input("Estados finais (separados por vírgula)",value=str(maquina.estados_aceitacao).replace('{','').replace('}','').replace('\'',''))
    estados_finais = estados_finais.split(',') if estados_finais else []

    # Definir transições
    st.subheader("Definir Transições")
    transicoes = definir_transicoes(maquina)

    # Entrada para a fita inicial
    fita_entrada = st.text_input("Fita de entrada")

    # Botão para executar a Máquina de Turing
    if st.button("Executar Máquina de Turing"):
        if estados and fita_alfabeto and transicoes and estado_inicial and estados_finais and fita_entrada:
            maquina = MaquinaTuring(estados, fita_alfabeto, fita_alfabeto, transicoes, estado_inicial, branco, estados_finais)
            
            try:
                resultado = maquina.executar(fita_entrada)
            except ValueError as erro:
                st.error(erro)
            else:
                st.success(f"Fita Final: {resultado}")
        else:
            st.error("Por favor, preencha todos os campos necessários.")

# Função para trocar o modo
def trocar_modo():
    if st.session_state.modo == 'Automato Finito':
        st.session_state.modo = 'Máquina de Turing'
    else:
        st.session_state.modo = 'Automato Finito'

# Exibindo o botão para trocar de modo
st.button("Trocar Modo", on_click=trocar_modo)

# Mostrando o modo atual
st.write(f"Modo Atual: {st.session_state.modo}")

# Exibindo a interface baseada no modo selecionado
if st.session_state.modo == 'Automato Finito':
    
    
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
        pasta='uploads/automatos'
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



else:

    interface_maquina_turing()

