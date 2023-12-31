# ---------------------------------------------------------------------------- #
#                                  Importações                                 #
# ---------------------------------------------------------------------------- #

from vpython import *
from vpython.no_notebook import stop_server
from random import random, randrange
from numpy import array, unique, savetxt


# ---------------------------------------------------------------------------- #
#                                    Classes                                   #
# ---------------------------------------------------------------------------- #

class Particula(simple_sphere):
    '''
    Classe utilizada para representar cada átomo como uma esfera.
    (Hard spheres model)
    '''
    def __init__(self, id:int, pos:vector, vel:vector, raio:float, massa:float,
                tipo:str, cor:vector, probReac:float):
        super().__init__(pos=pos, radius=raio, color=cor)
        self.color = cor
        self.id = id
        self.vel = vel
        self.massa = massa
        self.tipo = tipo
        self.vizinhos = []
        self.probReacao = probReac
        self.modificadorPR = 0
        


# ---------------------------------------------------------------------------- #
#                                    Funções                                   #
# ---------------------------------------------------------------------------- #

# --------------------------------- Dinâmica --------------------------------- #

def dist(r1:vector, r2:vector):
    '''
    Calcula a distância euclidiana bidimensional entre os vetores posição r1 e
    r2.

    Args:
        r1 (vpython vector): vetor posição (x1, y1, 0) da partícula 1
        r2 (vpython vector): vetor posição (x2, y2, 0) da partícula 2

    Returns:
        (float): distância euclidiana entre os vetores r1 e r2
    '''
    return mag(r1-r2)


def colElastica(p1:Particula, p2:Particula):
    '''
    Calcula e atualiza os vetores velocidade resultantes de cada partícula após
    sua colisão, considerando uma colisão elástica.

    Args:
        p1 (Particula): representa uma das partículas na colisão
        p2 (Particula): representa a outra partícula
'''
    v1, m1, x1 = p1.vel, p1.massa, p1.pos
    v2, m2, x2 = p2.vel, p2.massa, p2.pos
    v1_ = v1 - ((2*m2)/(m1+m2))*(dot(v1-v2, x1-x2)/(mag2(x1-x2)))*(x1-x2)
    v2_ = v2 - ((2*m1)/(m1+m2))*(dot(v2-v1, x2-x1)/(mag2(x2-x1)))*(x2-x1)
    print(f'\nColisão entre as partículas {p1.id} e {p2.id}!')
    p1.vel, p2.vel = v1_, v2_


def colInelastica(p1:Particula, p2:Particula):
    '''
    Calcula e atualiza os vetores velocidade resultantes da partícula após a
    colisão, considerando uma reação e colisão inelástica.

    Args:
        p1 (Particula): representa uma das partículas na colisão
        p2 (Particula): representa a outra partícula
    '''
    v1, m1, x1 = p1.vel, p1.massa, p1.pos
    v2, m2, x2 = p2.vel, p2.massa, p2.pos
    m_ = (m1+m2)/2
    v_ = (m1*v1+m2*v2)/m_
    x_ = (x1+x2)/2
    print(f'\nColisão entre as partículas {p1.id} e {p2.id}!')
    p1.vel, p1.pos = v_, x_


def reacao(p1:Particula, p2:Particula):
    '''
    Realiza a reação A + A --> B entre as partículas p1 e p2.

    Args:
        p1 (Particula): representa uma das partículas na reação
        p2 (Particula): representa a outra particula
    '''
    global propProduto, pInativas, nReag, nProd
    
    colInelastica(p1, p2)
    p1.radius = propProduto['raio']
    p1.massa = propProduto['massa']
    p1.tipo = propProduto['tipo']
    p1.color = propProduto['cor']
    if (p2 not in pInativas): pInativas.append(p2)
    nReag -= 2
    nProd += 1


def colisao(p1:Particula, p2:Particula):
    '''
    Chama uma colisão elástica ou inelástica dependendo da probabilidade de
    reação.

    Args:
        p1 (Particula): representa uma das partículas na colisão
        p2 (Particula): representa a outra particula
    '''
    t1, t2, probReacao = p1.tipo, p2.tipo, max(p1.probReacao, p2.probReacao)
    condReacao = random() <= probReacao
    condTipo = (t1 == t2 == 'A')
    if condReacao and condTipo: reacao(p1, p2)
    else: colElastica(p1, p2)
    
    
def atualizaVizinhos(p:Particula):
    '''
    Atualiza a lista de partículas vizinhas a uma partícula.

    Args:
        p (Particula): particula a ter seus vizinhos recalculados
    '''
    global pAtivas
    
    p.vizinhos.clear()
    x, r = p.pos, p.radius
    for p2 in pAtivas:
        x2 = p2.pos
        if (dist(x, x2) <= r+2.5) and (p != p2): p.vizinhos.append(p2)
    
    
def atualizaPos(p:Particula):
    '''
    Atualiza a posição de uma partícula.
    '''
    global dt

    p.pos += p.vel*dt
    
    
def colCheckPartPart(p1:Particula, p2:Particula):
    '''
    Checa colisão entre duas partículas.

    Args:
        p1 (Particula): representa uma das partículas na colisão
        p2 (Particula): representa a outra partícula
    '''
    global dt
    
    x1, v1, r1 = p1.pos, p1.vel, p1.radius
    x2, v2, r2 = p2.pos, p2.vel, p2.radius
    distMinima = r1+r2
    distancia = dist(x1, x2)
    distancia_ = dist(x1+(v1*dt), x2+(v2*dt))
    if (distancia <= distMinima) and (distancia > distancia_):
        colisao(p1, p2)


def colCheckPartParede(p:Particula):
    '''
    Checa colisão entre uma partícula e as paredes da caixa. Aumenta modificador
    de probabilidade de reação da partícula no caso de colisão (ação
    catalizadora).

    Args:
        p (Particula): partícula a ser examinada
    '''
    global dt, ladoCaixa
    
    r = p.radius
    pos = p.pos
    pos_  = p.pos+(p.vel*dt)
    if (abs(pos.x) >= (ladoCaixa/2-r)) and (abs(pos.x) < abs(pos_.x)):
        p.vel.x = -p.vel.x
        p.modificadorPR=60
    if (abs(pos.y) >= (ladoCaixa/2-r)) and (abs(pos.y) < abs(pos_.y)):
        p.vel.y = -p.vel.y
        p.modificadorPR=60
    
    
def atualizaVelMedia(p:Particula):
    '''
    Atualiza a velocidade média de uma partícula e adiciona esse valor à
    variável de média global.

    Args:
        p (Particula): partícula a ter sua velocidade calculada
    '''
    global mVelMediaQuad
    
    m, v = p.massa, p.vel
    mVelMediaQuad += m*mag2(v)
    
    
def atualizaTemp():
    '''
    Atualiza temperatura global do sistema em função da velocidade média
    global.
    '''
    global temperatura
    
    temperatura = mVelMediaQuad/(3*kB)
    
    
def atualizaProbReac(p:Particula):
    '''
    Atualiza probabilidade de reação em função da colisão com as paredes, os
    agentes catalisadores do sistema.
    
    Args:
        p (Particula): partícula a ter sua probabilidade de reação atualizada
    '''
    p.probReacao = propReagente['probReacao']*(1+p.modificadorPR)
    if p.modificadorPR!=0: p.modificadorPR -= 1
    
    
# ---------------------------------- Visual ---------------------------------- #

def criaCaixa():
    '''
    Cria representação das arestas da caixa imaginária para conter a simulação.
    '''
    global ladoCaixa
    
    d = ladoCaixa/2 + 1e-2
    caixa = curve(color=vector(1,1,1), radius=1e-2)
    caixa.append([vector(-d,-d,0), vector(-d,d,0), vector(d,d,0),
                  vector(d,-d,0), vector(-d,-d,0)])


def criaParticulas():
    '''
    Cria instâncias da classe Partícula ma lista de partículas ativas.
    '''
    global pInicial, ladoCaixa, velLimite, propReagente, pAtivas
    
    for num in range(pInicial):
        pos = [randrange(-ladoCaixa/2+1, ladoCaixa/2-1) for _ in range (2)]
        pos = vector(pos[0], pos[1], 0)
        vel = [(random() * velLimite) for _ in range(2)]
        vel = vector(vel[0], vel[1], 0)
        p = Particula(
            num, pos, vel,
            propReagente['raio'],
            propReagente['massa'],
            propReagente['tipo'],
            propReagente['cor'],
            propReagente['probReacao']
        )
        pAtivas.append(p)
        
        
def criaGraficos():
    '''
    Cria gráficos que acompanham a simulação.
    '''
    global grafComp, grafAlt, velLimite, pAtivas, pInicial, listaGrafConc,\
    listaGrafTemp
    
    # Gráfico 1:
    grafico1 = graph(title='Distribuição de velocidades', width=grafComp,
                    height=grafAlt, align='left', xmax=velLimite, ymax=8,
                    xtitle='Velocidade', ytitle='Número de partículas')
    histData = array([int(mag(p.vel)) for p in pAtivas])
    histX, histY = unique(histData, return_counts=True)
    histograma = gvbars(data=list(zip(histX, histY)),
                        color=vector(1,1,0))
    graficos.append(histograma)
    
    # Gráfico 2:
    grafico2 = graph(title='Concentração', width=grafComp,
                    height=grafAlt, align='left', ymax=pInicial,
                    xtitle='Tempo (Frames)', ytitle='Número de partículas')
    concReag = gcurve(data=list(zip(listaGrafConc[0], listaGrafConc[1])),
                    color=vector(1,0,0), label='Reagente')
    concProd = gcurve(data=list(zip(listaGrafConc[0], listaGrafConc[2])),
                    color=vector(0,0,1), label='Produto')
    graficos.extend([concReag, concProd])
    
    # Gráfico 3:
    grafico3 = graph(title='Temperatura', width=grafComp,
                    height=grafAlt, align='left',
                    xtitle='Tempo (Frames)', ytitle='Temperatura do sistema')
    tempSist = gcurve(data=list(zip(listaGrafTemp[0], listaGrafTemp[1])),
                    color=vector(1,0,0))
    graficos.extend([tempSist])
    

def atualizaGraficos():
    '''
    Atualiza os gráficos que acompanham a simulação.
    '''
    global pAtivas, graficos, listaGrafConc, listaGrafTemp
    
    # Gráfico 1:
    histograma = graficos[0]
    histData = array([int(mag(p.vel)) for p in pAtivas])
    histX, histY = unique(histData, return_counts=True)
    histograma.data = list(zip(histX, histY))
    
    # Gráfico 2:
    concReag, concProd = graficos[1], graficos[2]
    concReag.data = list(zip(listaGrafConc[0], listaGrafConc[1]))
    concProd.data = list(zip(listaGrafConc[0], listaGrafConc[2]))
    
    # Gráfico 3:
    tempSist = graficos[3]
    tempSist.data = list(zip(listaGrafTemp[0], listaGrafTemp[1]))
        

def atualizaListas(t:int):
    '''
    Atualiza listas para a plotagem dos gráficos.

    Args:
        t (int): tempo (frame) atual da simulação
    '''
    global listaGrafConc
    
    listaGrafConc[0].append(t)
    listaGrafConc[1].append(nReag)
    listaGrafConc[2].append(nProd)
    listaGrafTemp[1].append(temperatura)
    
    
# --------------------------------- Simulação -------------------------------- #

def delParticula(p:Particula):
    '''
    Deleta partícula da simulação.

    Args:
        p (Particula): partícula a ser deletada
    '''
    global pAtivas
    
    p.visible = False
    pAtivas.remove(p)
    del p
    
    
def exportarDados():
    '''
    Exporta os dados do gráfico de concentração.
    '''
    global listaGrafConc, pInicial
    
    # dados de concentração
    dadosC = [i for i in zip(listaGrafConc[0],listaGrafConc[1],listaGrafConc[2])]
    savetxt(f'dados/Conc/C-Num={pInicial}.csv', dadosC, delimiter=', ',
            fmt='% s')
    # dados de temperatura
    dadosT = [i for i in zip(listaGrafTemp[0], listaGrafTemp[1])]
    savetxt(f'dados/Temp/T-Num={pInicial}.csv', dadosT, delimiter=', ',
            fmt='% s')
    
    
def pararSimulacao():
    '''
    Para a simulação e exporta os dados de concentração
    '''
    global parar
    
    parar = True
    exportarDados()
    

def step():
    '''
    Passo da simulação:
        * Deleta todas as partículas inativas;
        * Reseta a lista de particulas inativas;
        * Atualiza gráficos;
        * Atualiza vizinhos;
        * Atualiza posições das partículas;
        * Atualiza probabilidade de reação;
        * Atualiza mVelMediaQuad;
        * Check de colisão partícula-partícula;
        * Check de colisão partícula-parede;
        * Atualiza temperatura
    '''
    global pInativas, pAtivas, mVelMediaQuad
    
    # * Deleta todas as partículas inativas:
    [delParticula(p) for p in pInativas]
    # * Reseta a lista de particulas inativas
    pInativas.clear()
    # * Atualiza gráficos:
    atualizaGraficos()
    # * Atualiza posições das partículas:
    for p in pAtivas:
        atualizaPos(p)
    # * Atualiza probabilidade de reação;
        atualizaProbReac(p)
    # * Atualiza mVelMediaQuad:
        atualizaVelMedia(p)
    # * Atualiza vizinhos:
        atualizaVizinhos(p)
    # * Check de colisão partícula-partícula:
        for p2 in p.vizinhos:
            colCheckPartPart(p, p2)
    # * Check de colisão partícula-parede:
        colCheckPartParede(p)
    # * Atualiza temperatura:
    mVelMediaQuad /= len(pAtivas)
    atualizaTemp()


def simulacao():
    '''
    Função responsável pela simulação completa.
    '''
    global nReag, listaGrafConc, nProd
    
    t = 0
    criaCaixa()
    criaParticulas()
    criaGraficos()
    while (not parar):
        step()
        t += 1
        atualizaListas(t)
    print('\nFim da simulação!')
    stop_server()



################################################################################



# ---------------------------------------------------------------------------- #
#                            Parâmetros da simulação                           #
# ---------------------------------------------------------------------------- #

dt = 1e-3 # Variação no tempo em cada frame
velLimite = 40 # Limite de velocidade inicial para as partículas
mVelMediaQuad = 0
temperatura = 0
kB = 1.380649*10**(-23)

pInicial = 150 # Número de partículas inicial
nReag = pInicial # Número de partículas de reagente
nProd = 0 # Número de partículas de produto

pAtivas = [] # Lista de partículas ativas
pInativas = [] # Lista de partículas inativas

ladoCaixa = 20 # Lado da caixa imaginária contendo a simulação

# Propriedades das partículas:
propReagente = {
    'raio':0.1,
    'massa':4e-23,
    'tipo':'A',
    'cor':vector(1,0,0),
    'probReacao':.05
}

propProduto = {
    'raio':0.12,
    'massa':6e-23,
    'tipo':'B',
    'cor':vector(0,0,1),
    'probReacao':0
}

# Gráfico de concentração:
graficos = []
listaTempo = [0]
listaReag = [nReag]
listaProd = [nProd]
listaGrafConc = [listaTempo, listaReag, listaProd]

# Gráfico de temperatura:
listaTemp = [temperatura]
listaGrafTemp = [listaTempo, listaTemp]


# ---------------------------------------------------------------------------- #
#                                 Setup VPython                                #
# ---------------------------------------------------------------------------- #

# Configurações da janela:
ladoJanela = 800
grafComp = ladoJanela/2
grafAlt = ladoJanela/3

# Criando a animação:
animacao = canvas(width=ladoJanela, height=ladoJanela, align='left')
animacao.range = ladoCaixa
animacao.camera.pos = vector(0,0,ladoCaixa)

parar = False

animacao.append_to_caption('\n\n\n                                            ')
botaoParar = button(pos=animacao.caption_anchor, text='Parar simulação',
                    bind=pararSimulacao, left=50)
animacao.append_to_caption('\n\n\n\n')


# ---------------------------------------------------------------------------- #
#                                   Simulação                                  #
# ---------------------------------------------------------------------------- #

simulacao()