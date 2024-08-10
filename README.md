# Projeto de Autômato Finito

Este projeto implementa um autômato finito, incluindo uma interface visual para interagir com o autômato.

## Estrutura do Projeto

- **`Automatos`**: Pasta com arquivos txt, cada arquivo contendo a estrutura de um automato finito de entrada;
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

## Como Usar

1. Interface Gráfica: Para iniciar a interface gráfica, execute o script interface.py:
```bash
python interface.py
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

## Contribuições

Se deseja contribuir para o projeto, por favor, abra um pull request ou crie uma issue.

## Licença

Este projeto é licenciado sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.