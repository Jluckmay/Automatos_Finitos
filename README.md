# Projeto de Autômato Finito

Este projeto implementa um autômato finito, incluindo uma interface visual para interagir com o autômato.

## Estrutura do Projeto

- **`Automatos`**: Pasta com arquivos txt, cada arquivo contendo a estrutura de um Automato Finito de entrada;
- **`Maquina de Turing`**: Pasta com arquivos txt, cada arquivo contendo a estrutura de uma Máquina de Turing de entrada;
- **`AutomatoFinito.py`**: Script contendo a implementação principal do autômato finito;
- **`interface.py`**: Script para a interface visual do projeto;
- **`projeto.py`**: Script que integra diferentes componentes do projeto sem o uso de interface gráfica;
- **`automato.html`** e **`interface.html`**: Arquivos HTML usados para exibir a interface do autômato;
- **`palavras.txt`**: Arquivo de texto contendo dados de entrada para o autômato;
- **`requirements.txt`**: Arquivo contendo as dependências do projeto.

## Dependências

Certifique-se de ter o Python 3.7+ instalado. Para instalar as dependências, execute:

```bash
pip install -r requirements.txt
```

Para a geração de representações gráficas é necessário instalar o [Graphviz](https://graphviz.org/).

## Como Usar

1. Interface Gráfica: Para iniciar a interface gráfica, execute o script utilizando o pacote streamlit interface.py:
```bash
streamlit run interface.py
```

2. Uso sem interface gráfica: Para utilizar diretamente o autômato sem interface gráfica, execute o script projeto.py:
```bash
python projeto.py
```
Certifique-se de configurar corretamente os arquivos de entrada de palavras a serem testadas **`palavras.txt`** e da estrutura dos automatos a serem testados, os quais devem estar na pasta **`Automatos`** em formato txt com a seguinte formatação:

```txt
estados:t0,t1,t2,t3,t4
alfabeto:i,j
transicoes:
t1 i t0
t0 i t3
t0 j t2
t2 i t4
t3 j t2
t3 i t3
t4 i t3
t4 j t2
estado_inicial:t1
estados_aceitacao:t3
```

Sendo:

- **`estados`**: Lista de estados do autômato;
- **`alfabeto`**: Conjunto de símbolos aceitos;
- **`transicoes`**: Mapeamento das transições entre estados;
- **`estado_inicial`**: O estado inicial do autômato;
- **`estados_aceitacao`**: Conjunto de estados de aceitação.


## Detalhes Técnicos

- O projeto foi desenvolvido em Python e utiliza bibliotecas específicas mencionadas no arquivo **`requirements.txt`**.

## Classe AutomatoFinito
A classe AutomatoFinito representa um autômato finito, com funcionalidades para adicionar estados e transições, simular o autômato, converter para um autômato finito determinístico (AFD), minimizar o autômato e converter para uma expressão regular. Abaixo está uma descrição detalhada de cada método:

- Métodos da Classe
- **`__init__(self, estados=set(), alfabeto=set(), transicoes={}, estado_inicial=None, estados_aceitacao=set())`**
Inicializa um autômato finito com os parâmetros fornecidos:

estados: Conjunto de estados do autômato.
alfabeto: Conjunto de símbolos do alfabeto.
transicoes: Dicionário de transições onde as chaves são tuplas (estado, simbolo) e os valores são conjuntos de estados de destino.
estado_inicial: Estado inicial do autômato.
estados_aceitacao: Conjunto de estados de aceitação.
adicionar_estado(self, estado, inicial=False, aceitacao=False)
Adiciona um novo estado ao autômato. Se o estado é inicial, define-o como o estado inicial. Se o estado é de aceitação, adiciona-o ao conjunto de estados de aceitação.

- **`adicionar_transicao(self, estado_origem, simbolo, estado_destino)`**
Adiciona uma transição ao autômato. Se não houver uma transição definida para (estado_origem, simbolo), inicializa-a com um conjunto vazio e depois adiciona estado_destino ao conjunto de destinos.

- **`transicoes_estado(self, estado, simbolo)`**
Retorna o conjunto de estados de destino para uma dada transição (estado, simbolo). Retorna uma string vazia se não houver transições definidas.

- **`is_AFD(self)`**
Verifica se o autômato é um Autômato Finito Determinístico (AFD). Um autômato é considerado um AFD se não possui transições vazias e se para cada estado e símbolo, existe no máximo um estado de destino.

- **`simular(self, palavra)`**
Simula o autômato finito não determinístico (AFN) para uma palavra dada. Usa uma função recursiva interna para realizar a simulação.

- **`__simular_recursivo(self, estado_atual, palavra)`**
Função recursiva para simular o AFN. Verifica se a palavra é aceita a partir do estado_atual e com a palavra restante.

- **`is_complete(self)`**
Verifica se o autômato é completo, ou seja, se todas as combinações de estado e símbolo têm uma transição definida.

- **`to_afd(self)`**
Converte um autômato finito não determinístico (AFN) para um autômato finito determinístico (AFD). Se o autômato já for um AFD, retorna o autômato atual.

- **`minimizar(self)`**
Minimiza o autômato determinístico (AFD). Se o autômato não for um AFD, primeiro o converte para um AFD antes da minimização. Usa o algoritmo de minimização para reduzir o número de estados.

- **`to_er(self)`**
Converte o autômato para uma expressão regular. Adiciona estados inicial e final únicos e constrói a tabela de transições para eliminar estados intermediários.

- **`criar_imagem(self, color='gray')`**
Cria uma imagem do autômato usando o Graphviz. Configura a cor dos estados e transições e adiciona uma representação visual do autômato.

- **`render_image(self, imagem, nome)`**
Renderiza e salva a imagem do autômato no formato PNG. Organiza o nome da imagem para garantir que ele seja único e salva a imagem em um diretório chamado "Imagens".

- **`__repr__(self)`**
Representação detalhada do autômato em formato de string. Inclui estados, alfabeto, transições, estado inicial e estados de aceitação.

- **`__str__(self)`**
Representação em string do autômato. Formata estados, alfabeto, transições, estado inicial e estados de aceitação para uma visualização mais amigável.

## Classe MaquinaTuring
A classe MaquinaTuring estende a classe AutomatoFinito para representar uma Máquina de Turing. Inclui métodos para inicializar a fita, mover a cabeça de leitura/gravação, e executar a máquina. Abaixo está uma descrição detalhada de cada método:

- Métodos da Classe
- **`__init__(self, estados=set(), alfabeto=set(), fita_alfabeto=set(), transicoes={}, estado_inicial=None, branco=None, estados_aceitacao=set())`**
Inicializa uma Máquina de Turing com os parâmetros fornecidos:

**`estados`**: Conjunto de estados da máquina.
**`alfabeto`**: Conjunto de símbolos de entrada.
**`fita_alfabeto`**: Conjunto de símbolos que podem aparecer na fita.
**`transicoes`**: Dicionário de transições onde as chaves são tuplas (estado, simbolo) e os valores são tuplas (novo_estado, novo_simbolo, direcao).
**`estado_inicial`**: Estado inicial da máquina.
**`branco`**: Símbolo que representa uma célula em branco na fita.
**`estados_aceitacao`**: Conjunto de estados de aceitação.
-**`inicializar_fita(self, entrada)`**
Inicializa a fita da Máquina de Turing com a entrada fornecida. A entrada é convertida em uma lista de símbolos e células em branco são adicionadas ao final da fita para garantir que haja espaço suficiente para a execução.

- **`mover_cabeca(self, direcao)`**
Move a cabeça de leitura/gravação da fita na direção especificada:

'R': Move para a direita.
'L': Move para a esquerda.
executar_passo(self)
Executa um único passo da Máquina de Turing. Lê o símbolo atual na fita, verifica a transição correspondente, e atualiza o símbolo na fita, o estado atual e a posição da cabeça de acordo com a transição definida. Se a transição para o estado atual e símbolo não estiver definida, levanta um erro.

- **`executar(self, entrada)`**
Executa a Máquina de Turing com a entrada fornecida. Inicializa a fita com a entrada, e executa passos até que a máquina entre em um estado de aceitação. Retorna o conteúdo final da fita, removendo quaisquer células em branco adicionais.

- **`__str__(self)`**
Representação em string do estado atual da Máquina de Turing. Inclui o estado atual, o conteúdo da fita e a posição da cabeça de leitura/gravação.

## Contribuições

Se deseja contribuir para o projeto, por favor, abra um pull request ou crie uma issue.

## Licença

Este projeto é licenciado sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.