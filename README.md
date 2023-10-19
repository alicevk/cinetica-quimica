<hr>

# Simulação Computacional de Cinética Química

<hr>

## Conteúdo

1. [Visão Geral](#visão-geral)
2. [Requisitos](#requisitos)
3. [Instalação](#instalação)
4. [Uso](#uso)
5. [Autores](#autores)

## Visão Geral

Neste repositório, você encontrará:

- Modelos de simulação de dinâmica molecular para análise de aspectos da cinética química.
- Exemplos de aplicação e scripts de uso.
- Documentação e recursos adicionais para entender os conceitos por trás das simulações.

Neste repositório, ficaram depositadas os scripts (`.py`) e notebooks (`.ipynb`) referentes às atividades da matéria de Cinética Química, no Bacharelado de Ciência e Tecnologia da Ilum - Escola de Ciência, ministrada pelo professor Amauri Jardim de Paula. Nesta, buscamos simular os mecanismos que fazem ocorrer uma reação química, além de entender seus princípios físicos. 

Num primeiro momento, foram feitas simulações em 2D, partindo de moléculas de mesma massa e tamanho, para entendermos a física das colisões entre partículas. Entendido isso, será escolhida uma reação para que os discentes possam trabalhar, buscando a simulação de uma reação real.

Como continuação, foi implementada uma simulação de reação simples do tipo $A + A \rightarrow B$, acompanhada de um gráfico de concentração das moléculas (reagentes e produtos).

## Requisitos

Antes de começar, certifique-se de ter as seguintes ferramentas instaladas:

|   |   |
| - | - |
| <a href="https://www.python.org/"><img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original-wordmark.svg" width="40" height="40"></a> | <a href="https://www.python.org/"><img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/jupyter/jupyter-original-wordmark.svg" width="40" height="40"></a> |
|

assim como as seguintes bibliotecas/módulos:

- [VPython](https://vpython.org/)
- [NumPy](https://numpy.org/)
- [Itertools](https://docs.python.org/3/library/itertools.html)
- [Random](https://docs.python.org/3/library/random.html)

para a simulação em [`simulacao.py`](simulacao.py), além de:

- [Pandas](https://pandas.pydata.org)
- [SciPy](https://scipy.org)

para a análise dos gráficos em [`graficos.ipynb`](graficos.ipynb).

Você pode instalar as dependências usando o gerenciador de pacotes [pip](https://pip.pypa.io/en/stable/):

    pip install nome-da-biblioteca
    
## Instalação

Para utilizar o script localmente, comece clonando este repositório:

    git clone https://github.com/seu-usuario/simulacao-cinetica-quimica.git

Acesse o diretório do projeto, e instale as dependências (veja a seção [Requisitos](#requisitos) acima).

## Uso

Para usar a simulação de cinética química disponível neste repositório, siga os passos abaixo:

1. Certifique-se de ter instalado todas as dependências necessárias conforme mencionado na seção Requisitos.

2. Execute o script de simulação Python no terminal:

```
python simulacao.py
```

A simulação será iniciada, e você poderá observar a cinética química em ação.

## Autores

<table>
  <tr>
    <td align="center"><a href="https://github.com/alicevk"><img style="border-radius: 50%;" src="https://avatars.githubusercontent.com/u/107062251?v=4" width="100px;" alt=""/><br /><sub><b>Alice Kageyama </b></sub></a><br /></td>
    <td align="center"><a href="https://github.com/Thomazellinho"><img style="border-radius: 50%;" src="https://avatars.githubusercontent.com/u/106624831?v=4" width="100px;" alt=""/><br /><sub><b> Pedro Thomazelli</b></sub></a><br /></td>
  </tr>
</table>
