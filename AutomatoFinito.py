class AutomatoFinito:
    def __init__(self, estados, alfabeto, transicoes, estado_inicial, estados_aceitacao):
        self.estados = estados
        self.alfabeto = alfabeto
        self.transicoes = transicoes
        self.estado_inicial = estado_inicial
        self.estados_aceitacao = estados_aceitacao
    
    def adicionar_transicao(self, estado_origem, simbolo, estado_destino):
        if (estado_origem, simbolo) not in self.transicoes:
            self.transicoes[(estado_origem, simbolo)] = set()
        self.transicoes[(estado_origem, simbolo)].add(estado_destino)
    
    def transicoes_estado(self, estado, simbolo):
        return self.transicoes.get((estado, simbolo), set())
    
    def eh_deterministico(self):
        for (estado, simbolo), estados_destino in self.transicoes.items():
            if isinstance(estados_destino, set) and len(estados_destino) > 1:
                return False
        return True

    def __simular_afd(self, palavra):
        estado_atual = self.estado_inicial
        for simbolo in palavra:
            # input(f'atual:{estado_atual}\ntransições:{self.transicoes}')
            if (estado_atual, simbolo) in self.transicoes:
                estado_atual = self.transicoes[(estado_atual, simbolo)]
            else:
                return False
        return estado_atual in self.estados_aceitacao

    def __simular_afn(self, palavra):
        return self.__simular_afn_recursivo(self.estado_inicial, palavra)

    def __simular_afn_recursivo(self, estado_atual, palavra):
        if not palavra:
            return estado_atual in self.estados_aceitacao

        simbolo = palavra[0]
        palavra_restante = palavra[1:]

        for proximo_estado in self.transicoes_estado(estado_atual, simbolo):
            if self.__simular_afn_recursivo(proximo_estado, palavra_restante):
                return True
        return False

    def simular(self, palavra):
        if self.eh_deterministico():
            return self.__simular_afd(palavra)
        else:
            return self.__simular_afn(palavra)
        
    def converter_afn_para_afd(self):
        novos_estados = set()
        novas_transicoes = {}
        novos_estados_aceitacao = set()

        estado_inicial_afd = frozenset([self.estado_inicial])
        estados_afd = [estado_inicial_afd]
        mapeamento = {estado_inicial_afd: 'q0'}
        novo_estado_mapeamento = {'q0': estado_inicial_afd}
        estado_contador = 1

        while estados_afd:
            estado_atual = estados_afd.pop()
            novos_estados.add(mapeamento[estado_atual])

            for simbolo in self.alfabeto:
                novos_destinos = frozenset(
                    destino for origem in estado_atual for destino in self.transicoes.get((origem, simbolo), set())
                )
                if novos_destinos:
                    if novos_destinos not in mapeamento:
                        novo_nome_estado = f'q{estado_contador}'
                        estado_contador += 1
                        mapeamento[novos_destinos] = novo_nome_estado
                        novo_estado_mapeamento[novo_nome_estado] = novos_destinos
                        estados_afd.append(novos_destinos)
                    novas_transicoes[(mapeamento[estado_atual], simbolo)] = {mapeamento[novos_destinos]}

                    if novos_destinos & self.estados_aceitacao:
                        novos_estados_aceitacao.add(mapeamento[novos_destinos])

        return AutomatoFinito(
            estados=novos_estados,
            alfabeto=self.alfabeto,
            transicoes=novas_transicoes,
            estado_inicial=mapeamento[estado_inicial_afd],
            estados_aceitacao=novos_estados_aceitacao
        )

    def minimizar(self):
        if not self.eh_deterministico():
            return self.converter_afn_para_afd().minimizar()

        P = [self.estados_aceitacao, self.estados - self.estados_aceitacao]
        W = [self.estados_aceitacao]

        while W:
            A = W.pop()
            for simbolo in self.alfabeto:
                X = {estado for estado in self.estados if self.transicoes.get((estado, simbolo), None) in A}
                novos_p = []
                for Y in P:
                    intersecao = Y.intersection(X)
                    diferenca = Y.difference(X)
                    if intersecao and diferenca:
                        novos_p.extend([intersecao, diferenca])
                        if Y in W:
                            W.remove(Y)
                            W.extend([intersecao, diferenca])
                        else:
                            W.append(intersecao if len(intersecao) <= len(diferenca) else diferenca)
                    else:
                        novos_p.append(Y)
                P = novos_p

        novo_estado_mapeamento = {estado: ('q'+str(idx)) for idx, subconjunto in enumerate(P) for estado in subconjunto}
        novos_estados = set(novo_estado_mapeamento.values())
        novos_estados_aceitacao = {novo_estado_mapeamento[estado] for estado in self.estados_aceitacao}
        novo_estado_inicial = novo_estado_mapeamento[self.estado_inicial]
        novas_transicoes = {}
        for (estado, simbolo), destinos in self.transicoes.items():
            novo_estado = novo_estado_mapeamento[estado]
            novo_destino = novo_estado_mapeamento[next(iter(destinos))]  # Considerando que é um AFD
            novas_transicoes[(novo_estado, simbolo)] = {novo_destino}

        return AutomatoFinito(
            estados=novos_estados,
            alfabeto=self.alfabeto,
            transicoes=novas_transicoes,
            estado_inicial=novo_estado_inicial,
            estados_aceitacao=novos_estados_aceitacao
        )

    
    def to_er(self):
        
        automato = self.minimizar()
        
        estados = list(automato.estados)
        alfabeto = list(automato.alfabeto)
        transicoes = automato.transicoes

        if automato.estado_inicial not in estados:
            estados.append(automato.estado_inicial)
        
        if not all(e in estados for e in automato.estados_aceitacao):
            for e in automato.estados_aceitacao:
                if e not in estados:
                    estados.append(e)

        regex_table = {e: {f: '' for f in estados} for e in estados}

        for (estado_origem, simbolo), estados_destino in transicoes.items():
            for estado_destino in estados_destino:
                if regex_table[estado_origem][estado_destino]:
                    regex_table[estado_origem][estado_destino] += f"|{simbolo}"
                else:
                    regex_table[estado_origem][estado_destino] = simbolo

        for k in estados:
            for i in estados:
                for j in estados:
                    r1 = regex_table[i][j]
                    r2 = regex_table[i][k]
                    r3 = regex_table[k][k]
                    r4 = regex_table[k][j]
                    regex_table[i][j] = f"{r1}|({r2}({r3})*{r4})" if r1 else f"({r2}({r3})*{r4})"

        expressao_regular = ''
        for estado in automato.estados_aceitacao:
            if expressao_regular:
                expressao_regular += f"|{regex_table[automato.estado_inicial][estado]}"
            else:
                expressao_regular = regex_table[automato.estado_inicial][estado]
        
        return expressao_regular
    
    def __repr__(self):
        return (f"Estados: {self.estados}\n"
                f"Alfabeto: {self.alfabeto}\n"
                f"Transições: {self.transicoes}\n"
                f"Estado Inicial: {self.estado_inicial}\n"
                f"Estados de Aceitação: {self.estados_aceitacao}")
    
    def __str__(self):
        def formatar_estado(estado):
            if isinstance(estado, frozenset):
                return "{" + ", ".join(sorted(estado)) + "}"
            return str(estado)

        def formatar_transicoes(transicoes):
            transicoes_formatadas = []
            for (origem, simbolo), destinos in transicoes.items():
                destinos_formatados = ", ".join(formatar_estado(destino) for destino in destinos)
                transicoes_formatadas.append(f"({formatar_estado(origem)}, '{simbolo}') -> {{{destinos_formatados}}}")
            return "\n".join(transicoes_formatadas)

        estados_formatados = ", ".join(formatar_estado(estado) for estado in self.estados)
        estados_aceitacao_formatados = ", ".join(formatar_estado(estado) for estado in self.estados_aceitacao)
        transicoes_formatadas = formatar_transicoes(self.transicoes)

        return (f"Estados: {estados_formatados}\n"
                f"Alfabeto: {self.alfabeto}\n"
                f"Transições:\n{transicoes_formatadas}\n"
                f"Estado Inicial: {formatar_estado(self.estado_inicial)}\n"
                f"Estados de Aceitação: {estados_aceitacao_formatados}")
    
