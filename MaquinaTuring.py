from AutomatoFinito import AutomatoFinito

class MaquinaTuring(AutomatoFinito):
    def __init__(self, estados=set(), alfabeto=set(), fita_alfabeto=set(), transicoes={}, estado_inicial=None, branco=None, estados_aceitacao=set()):
        super().__init__(estados, alfabeto, transicoes, estado_inicial, estados_aceitacao)
        self.fita_alfabeto = fita_alfabeto
        self.branco = branco
        self.fita = []
        self.posicao_cabeca = 0
        self.estado_atual = estado_inicial

    def inicializar_fita(self, entrada):
        self.fita = list(entrada) + [self.branco] * 10  # Adiciona células em branco ao final da fita

    def mover_cabeca(self, direcao):
        if direcao == 'R':
            self.posicao_cabeca += 1
        elif direcao == 'L':
            self.posicao_cabeca -= 1

    def executar_passo(self):
        simbolo_atual = self.fita[self.posicao_cabeca]
        if (self.estado_atual, simbolo_atual) in self.transicoes:
            novo_estado, novo_simbolo, direcao = self.transicoes[(self.estado_atual, simbolo_atual)]
            self.fita[self.posicao_cabeca] = novo_simbolo
            self.mover_cabeca(direcao)
            self.estado_atual = novo_estado
        else:
            # return False
            raise ValueError(f"Transição indefinida para o estado {self.estado_atual} com o símbolo {simbolo_atual}.")

    def executar(self, entrada):
        self.inicializar_fita(entrada)
        while self.estado_atual not in self.estados_aceitacao:
            self.executar_passo()
        return ''.join(self.fita).strip(self.branco)

    def __str__(self):
        return "Estado Atual: {} | Fita: {} | Cabeça: {}".format(self.estado_atual, ''.join(self.fita), self.posicao_cabeca)
