import os
from graphviz import Digraph

class AutomatoFinito:
    # Inicializa um autômato finito com estados, alfabeto, transições, estado inicial e estados de aceitação
    def __init__(self, estados=set(), alfabeto=set(), transicoes={}, estado_inicial=None, estados_aceitacao=set()):
        self.estados = estados
        self.alfabeto = alfabeto
        self.transicoes = transicoes
        self.estado_inicial = estado_inicial
        self.estados_aceitacao = estados_aceitacao

    def adicionar_estado(self, estado, inicial=False, aceitacao=False):
        self.estados.add(estado)
        if inicial:
            self.estado_inicial = estado
        if aceitacao:
            self.estados_aceitacao.add(estado)
    
    # Adiciona uma transição ao autômato
    def adicionar_transicao(self, estado_origem, simbolo, estado_destino):
        # Se não houver transição definida para (estado_origem, simbolo), inicializa com um conjunto vazio
        if (estado_origem, simbolo) not in self.transicoes:
            self.transicoes[(estado_origem, simbolo)] = set()
        # Adiciona o estado_destino ao conjunto de destinos
        self.transicoes[(estado_origem, simbolo)].add(estado_destino)
    
    # Retorna o conjunto de estados de destino para uma dada transição
    def transicoes_estado(self, estado, simbolo):
        return self.transicoes.get((estado, simbolo), '')
    
    # Verifica se o autômato é um AFD (Autômato Finito Determinístico)
    def is_AFD(self):
        for (estado, simbolo), estados_destino in self.transicoes.items():
            # Se há transição vazia, é AFN
            if ((simbolo == 'ε') or (simbolo == '')):
                return False
            
            # Se um estado e símbolo têm múltiplos destinos, é um AFN
            if isinstance(estados_destino, set) and len(estados_destino) > 1:
                return False
            
        # Se não é AFN, é AFD
        return True

    # Simula o autômato finito não determinístico (AFN) para uma palavra
    def simular(self, palavra):
        return self.__simular_recursivo(self.estado_inicial, palavra)

    # Função recursiva para simular o AFN
    def __simular_recursivo(self, estado_atual, palavra):
        if not palavra:
            return estado_atual in self.estados_aceitacao

        simbolo = palavra[0]
        palavra_restante = palavra[1:]

        for proximo_estado in self.transicoes_estado(estado_atual, simbolo):
            if self.__simular_recursivo(proximo_estado, palavra_restante):
                return True
        return False
        
    # Função para verificar se o automato é completo
    def is_complete(self):

        for estado in self.estados:
            for simbolo in self.alfabeto:
                if not((estado,simbolo) in self.transicoes):
                    return False
                
        return True

    # Converte um autômato finito não determinístico para um autômato finito determinístico (AFD)
    def to_afd(self):
        # Se já é AFD, retorna o autômato atual
        if self.is_AFD():
            return self

        novos_estados = set()
        novas_transicoes = {}
        novos_estados_aceitacao = set()

        # Estado inicial do AFD é um conjunto contendo o estado inicial do AFN
        estado_inicial_afd = frozenset([self.estado_inicial])
        estados_afd = [estado_inicial_afd]
        mapeamento = {estado_inicial_afd: 'q0'}
        novo_estado_mapeamento = {'q0': estado_inicial_afd}
        estado_contador = 1

        # Processa todos os estados do AFD a partir do estado inicial
        while estados_afd:
            estado_atual = estados_afd.pop()
            novos_estados.add(mapeamento[estado_atual])

            for simbolo in self.alfabeto:
                novos_destinos = frozenset(
                    destino for origem in estado_atual for destino in self.transicoes.get((origem, simbolo), set())
                )
                if novos_destinos:
                    # Se novos_destinos não está no mapeamento, cria um novo estado
                    if novos_destinos not in mapeamento:
                        novo_nome_estado = f'q{estado_contador}'
                        estado_contador += 1
                        mapeamento[novos_destinos] = novo_nome_estado
                        novo_estado_mapeamento[novo_nome_estado] = novos_destinos
                        estados_afd.append(novos_destinos)
                    novas_transicoes[(mapeamento[estado_atual], simbolo)] = {mapeamento[novos_destinos]}

                    # Adiciona o novo estado como estado de aceitação se necessário
                    if novos_destinos & self.estados_aceitacao:
                        novos_estados_aceitacao.add(mapeamento[novos_destinos])

        # Cria um novo autômato com os estados e transições determinísticos
        return AutomatoFinito(
            estados=novos_estados,
            alfabeto=self.alfabeto,
            transicoes=novas_transicoes,
            estado_inicial=mapeamento[estado_inicial_afd],
            estados_aceitacao=novos_estados_aceitacao
        )

    # Minimiza o autômato determinístico (AFD)
    def minimizar(self):
        # Converte para AFD se necessário antes da minimização
        if not self.is_AFD():
            return self.to_afd().minimizar()

        # Inicializa as partições: estados de aceitação e não aceitação
        particoes = [self.estados_aceitacao, self.estados - self.estados_aceitacao]
        conjuntos_pendentes = [self.estados_aceitacao] if self.estados_aceitacao else [self.estados - self.estados_aceitacao]

        # Processa as partições enquanto houver conjuntos pendentes
        while conjuntos_pendentes:
            conjunto_atual = conjuntos_pendentes.pop()
            for simbolo in self.alfabeto:
                # Conjunto de estados que fazem transição para o conjunto atual sob o símbolo atual
                estados_com_transicao = {estado for estado in self.estados if any(destino in conjunto_atual for destino in self.transicoes.get((estado, simbolo), []))}
                novas_particoes = []
                for particao in particoes:
                    # Divide a partição em interseção e diferença
                    intersecao = particao.intersection(estados_com_transicao)
                    diferenca = particao.difference(estados_com_transicao)
                    if intersecao and diferenca:
                        # Adiciona novas partições e atualiza conjuntos pendentes
                        novas_particoes.extend([intersecao, diferenca])
                        if particao in conjuntos_pendentes:
                            conjuntos_pendentes.remove(particao)
                            conjuntos_pendentes.extend([intersecao, diferenca])
                        else:
                            conjuntos_pendentes.append(intersecao if len(intersecao) <= len(diferenca) else diferenca)
                    else:
                        novas_particoes.append(particao)
                particoes = novas_particoes

        # Mapeia estados antigos para novos estados minimizados
        novo_estado_nome = {}
        novo_estado_contador = 0
        for subconjunto in sorted(particoes, key=lambda x: (len(x), sorted(x))):
            nome_novo_estado = f'q{novo_estado_contador}'
            for estado in subconjunto:
                novo_estado_nome[estado] = nome_novo_estado
            novo_estado_contador += 1

        # Cria o conjunto de novos estados e ordena os estados de aceitação
        novos_estados = set(novo_estado_nome.values())
        novos_estados_aceitacao = sorted({novo_estado_nome[estado] for estado in self.estados_aceitacao}, reverse=True)
        novo_estado_inicial = novo_estado_nome[self.estado_inicial]

        # Constrói as novas transições com base no mapeamento de estados
        novas_transicoes = {}
        for (estado, simbolo), destinos in self.transicoes.items():
            novo_estado_origem = novo_estado_nome[estado]
            novo_estado_destino = novo_estado_nome[next(iter(destinos))]
            novas_transicoes[(novo_estado_origem, simbolo)] = {novo_estado_destino}

        # Retorna o autômato minimizado
        return AutomatoFinito(
            estados=novos_estados,
            alfabeto=self.alfabeto,
            transicoes=novas_transicoes,
            estado_inicial=novo_estado_inicial,
            estados_aceitacao=set(novos_estados_aceitacao)
        )
   
    # Converte o autômato para uma expressão regular
    def to_er(self):
        automato = self.minimizar()
        # Adiciona estados inicial e final únicos
        inicial = 'qi'
        final = 'qf'
        automato.estados.add(inicial)
        automato.estados.add(final)

        for estado in automato.estados_aceitacao:
            automato.adicionar_transicao(estado, 'ε', final)

        automato.adicionar_transicao(inicial, 'ε', automato.estado_inicial)

        automato.estado_inicial = inicial
        automato.estados_aceitacao = {final}

        # Construindo a tabela de transições
        tabela = {}
        for origem in automato.estados:
            tabela[origem] = {}
            for destino in automato.estados:
                tabela[origem][destino] = ''
        
        for (origem, simbolo), destinos in automato.transicoes.items():
            for destino in destinos:
                if tabela[origem][destino]:
                    tabela[origem][destino] += '+'
                tabela[origem][destino] += simbolo or ''

        # Eliminando estados intermediários
        estados = list(automato.estados - {inicial, final})
        estados.sort()
        
        while estados:
            remover = estados.pop(0)
            entradas = [origem for origem in automato.estados if remover in tabela.get(origem, {}) and tabela[origem][remover]]
            saidas = [destino for destino in automato.estados if destino in tabela and tabela[remover].get(destino) != '']
            entradas.sort()
            saidas.sort()

            for entrada in entradas:
                for saida in saidas:
                    r1 = tabela[entrada][remover] 
                    r2 = tabela[remover][remover] 
                    r3 = tabela[remover][saida]
                    # Cria a nova transição eliminando o estado intermediário
                    nova_transicao = f"{r1}({r2})*{r3}" if not (r2 in {'', 'ε'}) else f"{r1}{r3}"
                    if not (tabela[entrada][saida] in {'', 'ε'}):
                        tabela[entrada][saida] += '+'
                    tabela[entrada][saida] += nova_transicao

            # Remove o estado intermediário das transições
            for origem in automato.estados:
                if remover in tabela.get(origem, {}):
                    tabela[origem].pop(remover, None)
            tabela.pop(remover, None)

        # Retorna a expressão regular resultante
        return tabela[inicial][final].replace('ε', '')

    def criar_imagem(self, color='gray'):

        imagem = Digraph()

        imagem.attr(bgcolor='transparent')

        imagem.attr(rankdir='LR')

        for estado in self.estados:
                imagem.node(estado,shape='doublecircle' if estado in self.estados_aceitacao else 'circle', color=color, fontcolor=color)
                for simbolo in self.alfabeto:
                    destinos = self.transicoes_estado(estado,simbolo)
                    for destino in destinos:
                        imagem.edge(estado,destino,label=simbolo, color=color, fontcolor=color)

        if self.estado_inicial!=None:
            imagem.node('',shape='point', color=color)
            imagem.edge('',self.estado_inicial, color=color)

        return imagem

    def render_image(self, imagem, nome):
         # Configuração de pasta e nome de imagem
        pasta = 'Imagens'
        if not os.path.exists(pasta):
            os.makedirs(pasta)

        automatos = os.listdir(pasta)
        automatos.sort()

        if ".png" in nome:
            nome = nome.split('.')[0]

        if not automatos:
            nome_imagem = 'automato0'
        else:
    
            nome_imagem = automatos[-1].split('.')[0].replace('automato','').replace('_AFD','').replace('_Min','')
            nome_imagem = nome + str(int(nome_imagem))

            while ((nome_imagem+'.png') in automatos):
                automatos.pop()
                nome_imagem = automatos[-1].split('.')[0].replace('automato','').replace('_AFD','').replace('_Min','')
                nome_imagem = nome + str(int(nome_imagem) + 1)

        caminho = os.path.join(pasta, nome_imagem)

        imagem.render(caminho,cleanup=True,format='png')
        
        return caminho+'.png'

    # Representação em string detalhada do autômato
    def __repr__(self):
        estados_ordenados = sorted(self.estados)
        alfabeto_ordenado = sorted(self.alfabeto)
        transicoes_ordenadas = sorted(self.transicoes.items())
        estados_aceitacao_ordenados = sorted(self.estados_aceitacao)
        
        transicoes_formatadas = [
            f"({estado}, '{simbolo}') -> {destinos}" for (estado, simbolo), destinos in transicoes_ordenadas
        ]
        
        return (f"Estados: {estados_ordenados}\n"
                f"Alfabeto: {alfabeto_ordenado}\n"
                f"Transições:" + "\n".join(transicoes_formatadas) + "\n"
                f"Estado Inicial: {self.estado_inicial}\n"
                f"Estados de Aceitação: {estados_aceitacao_ordenados}")

    # Representação em string do autômato
    def __str__(self):
        def formatar_estado(estado):
            if isinstance(estado, frozenset):
                return "{" + ", ".join(sorted(estado)) + "}"
            return str(estado)
        
        def formatar_transicoes(transicoes):
            transicoes_ordenadas = sorted(transicoes.items())
            transicoes_formatadas = [
                f"({formatar_estado(origem)}, '{simbolo}') -> {{{', '.join(sorted(map(formatar_estado, destinos)))}}}" 
                for (origem, simbolo), destinos in transicoes_ordenadas
            ]
            return "\n".join(transicoes_formatadas)
        
        estados_formatados = ", ".join(sorted(map(formatar_estado, self.estados)))
        estados_aceitacao_formatados = ", ".join(sorted(map(formatar_estado, self.estados_aceitacao)))
        transicoes_formatadas = formatar_transicoes(self.transicoes)
        alfabeto_formatado = ", ".join(sorted(self.alfabeto))

        return (f"Estados: {estados_formatados}\n"
                f"Alfabeto: {alfabeto_formatado}\n"
                f"Transições:\n{transicoes_formatadas}\n"
                f"Estado Inicial: {formatar_estado(self.estado_inicial)}\n"
                f"Estados de Aceitação: {estados_aceitacao_formatados}")
