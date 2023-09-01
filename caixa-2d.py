# -------------------- Importações:

from vpython import *
from random import randrange, randint
from itertools import combinations
from numpy import histogram

# -------------------- Funções gerais:

def calcDist(r1, r2):
    '''
    Calcula a distância euclidiana bidimensional entre os vetores posição r1 e r2.

    Args:
        r1 (vpython vector): vetor posição (x1, y1, 0) da partícula 1
        r2 (vpython vector): vetor posição (x2, y2, 0) da partícula 2

    Returns:
        (float): distância euclidiana entre os vetores r1 e r2
    '''
    return mag(r1-r2)


def calcMassa(particulas):
    '''
    Calcula a massa média das partículas no sistema.

    Args:
        particulas (list): Lista dos objetos 'Partículas'; as partículas do sistema

    Returns:
        (float): massa média das partículas
    '''
    massas = [part.massa for part in particulas]
    return sum(massas)/len(massas)

def colisao(particula1, particula2):
    '''
    Calcula os vetores resultantes de cada partícula após sua colisão.

    Args:
        particula1 (Particula): representa uma das partículas na colisão
        particula2 (Particula): representa a outra particula
        
    Returns:
        v1_atualizada (vpython vector): vetor velocidade atualizado para a partícula 1
        v2_atualizada (vpython vector): vetor velocidade atualizado para a partícula 2
    '''
    v1 = particula1.vel
    v2 = particula2.vel
    m1 = particula1.massa
    m2 = particula2.massa
    x1 = particula1.esfera.pos
    x2 = particula2.esfera.pos
    v1_atualizada = v1 - ((2*m2)/(m1+m2))*(dot(v1-v2, x1-x2)/(mag2(x1-x2)))*(x1-x2)
    v2_atualizada = v2 - ((2*m1)/(m1+m2))*(dot(v2-v1, x2-x1)/(mag2(x2-x1)))*(x2-x1)
    print(f"Houve uma colisão entre as partículas {particula1.id} e {particula2.id}!")
    return v1_atualizada, v2_atualizada


def maxwellBoltzmann(v, massaMedia):
    '''
    Função para plotagem da distribuição de Maxwell Boltzmann.
    '''
    alpha = (dv**2/binning) * numParticulas
    first = (massaMedia / (2*pi*k*T))**1.5
    second = exp(-.5*massaMedia*v**2 / (k*T))*v**2

    return (alpha * first * second) / numParticulas

# -------------------- Funções da simulação:

def criarCaixa():
    '''
    Cria representação das arestas da caixa imaginária para conter a simulação de colisão.
    '''
    caixa = curve(color=azul, radius=espessuraCaixa)
    caixa.append([vector(-d,-d,0), vector(-d,d,0), vector(d,d,0), vector(d,-d,0), vector(-d,-d,0)])


def criarParticulas():
    '''
    Cria um número de instâncias da classe Partícula em uma lista.
    '''
    raio = 0.1
    massa = 4e-23
    for num in range(numParticulas):
        particula = Particula(
            [randrange(-L / 2 + 1, L / 2 - 1) for _ in range(2)],
            [randint(0, maxVel) for _ in range(2)],
            raio,
            massa,
            num,
            vermelho,
            pointer,
        )
        particulas.append(particula)


def criarHistograma():
    '''
    Cria um histograma com as velocidades das patículas, juntamente da curva de
    distribuição de Maxwell-Boltzmann.

    Args:
        particulas (list): Lista dos objetos 'Partículas'; as partículas do sistema
    '''
    histograma = graph(width=histogramaW, height=histogramaH, align='left', xmax=maxVel, ymax=1,
                        xtitle='Velocidade (m/s)', ytitle = 'Densidade de Probabilidade')
    histData = [mag(particulas[n].vel) for n in range(numParticulas)]
    histData = histogram(histData, binning, (0,maxVel))
    histVals = histData[0]/numParticulas
    vDist = gvbars(color=color.red, delta=dv)
    vDist.data = list(zip(histData[1], histVals))
    
    # Plotando a distribuição de Maxwell-Boltzmann
    maxboltz = gcurve(color=color.blue, width=2)
    for vx in arange(0,maxVel,0.1):
        vy = maxwellBoltzmann(vx, calcMassa(particulas))
        maxboltz.plot(vx, vy)
    return vDist


def loopAnimacao(histograma):
    '''
    Função de loop para os aspectos visuais da simulação.
    '''
    rate(300)
    histTemp = []
    
    # Update (partículas, pointers e histograma)
    for num in range(numParticulas):
        particulas[num].esfera.pos += particulas[num].vel*dt
        histTemp.append(mag(particulas[num].vel))
        if pointer:
            particulas[num].pointer.pos = particulas[num].esfera.pos
            particulas[num].pointer.axis = particulas[num].vel
            particulas[num].pointer.length = 0.75

    histData = histogram(histTemp, binning, (0, maxVel))
    histVals = histData[0]/numParticulas
    histograma.data = list(zip(histData[1],histVals))

    # Colisão (entre as partículas)
    for particula1, particula2 in combinations(particulas,2):
        distAtual = calcDist(particula1.esfera.pos, particula2.esfera.pos)
        distFutura = calcDist((particula1.esfera.pos + particula1.vel*dt),
                            ((particula1.esfera.pos + particula1.vel*dt)))
        if (distAtual <= (particula1.raio + particula2.raio)) and (distAtual > distFutura):
            v1_atualizada, v2_atualizada = colisao(particula1, particula2)
            id1, id2 = particula1.id, particula2.id
            particulas[id1].vel = v1_atualizada
            particulas[id2].vel = v2_atualizada
            
    # Colisões (parede imaginária de lado L)
    for i in range(numParticulas):
        part = particulas[i]
        posAtual = part.esfera.pos
        posFutura = part.esfera.pos + part.vel*dt
        
        if (abs(posAtual.x) >= (L/2-part.raio)) and (abs(posAtual.x) < abs(posFutura.x)):
            particulas[i].vel.x = -particulas[i].vel.x
        
        if (abs(posAtual.y) >= (L/2-part.raio)) and (abs(posAtual.y) < abs(posFutura.y)):
            particulas[i].vel.y = -particulas[i].vel.y


def simulacao():
    '''
    Função que roda a simulação.
    '''
    criarCaixa()
    criarParticulas()
    histograma = criarHistograma()
    while True:
        loopAnimacao(histograma)


# -------------------- Classe das partícula:

class Particula:
    '''
    Classe utilizada para representar cada átomo como uma esfera dura.
    '''
    def __init__(self, r, vr, raio, massa, id, cor, pointer):
        x, y = r
        vx, vy = vr
        self.pos = vector(x, y, 0)
        self.vel = vector(vx, vy, 0)
        self.raio = raio
        self.massa = massa
        self.id = id
        self.cor = cor
        self.esfera = sphere(pos=self.pos, radius=self.raio, color=self.cor)
        if pointer: self.pointer = arrow(pos=self.esfera.pos, axis=self.vel, length=.75, round=True)


# -------------------- Parâmetros iniciais:

# Configurações da janela
janelaW = 800
janelaH = 800
histogramaW = janelaW/2
histogramaH = janelaH/3

# Configurações da simulação
L = 10
espessuraCaixa = L/200
d = L/2 + espessuraCaixa

numParticulas = 25
pointer = False
particulas = []

azul = color.blue
vermelho = color.red

dt = 1e-3
dv = 4
maxVel = 40
binning = maxVel // dv
k = 1.38e-23
T = 24
animation = canvas(width=janelaW, height=janelaH, align='left')
animation.range = L

# -------------------- Simulação:

simulacao()