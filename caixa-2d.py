# -------------------- Importações:

from vpython import *
from random import randrange, randint
from itertools import combinations
import numpy as np

# -------------------- Funções gerais:

def calcDist(r1, r2):
    '''
    Calcula a distância euclidiana bidimensional entre os vetores posição r1 e r2.

    Args:
        r1 (vpython vector): vetor posição (x1, y1, 0) da partícula 1
        r2 (vpython vector): vetor posição (x2, y2, 0) da partícula 2

    Returns:
        distancia (float): distância euclidiana entre os vetores r1 e r2
    '''
    distancia = mag(r1-r2)
    return distancia


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
    for num in range(numParticulas):
        particula = Particula([randrange(-L/2,L/2) for i in range(2)],
                            [randint(10,20) for i in range(2)],
                            0.3 , 1, num, vermelho, pointer)
        particulas.append(particula)
       
        
def loopAnimacao():
    '''
    Função de loop para os aspectos visuais da simulação.
    '''
    rate(300)
    
    # Update
    for num in range(numParticulas):
        particulas[num].esfera.pos += particulas[num].vel*dt
        if pointer:
            particulas[num].pointer.pos = particulas[num].esfera.pos
            particulas[num].pointer.axis = particulas[num].vel
            particulas[num].pointer.length = 0.75

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
        loc = particulas[i].esfera.pos
        
        if abs(loc.x) >= L/2:
            particulas[i].vel.x = -particulas[i].vel.x
        
        if abs(loc.y) >= L/2:
            particulas[i].vel.y = -particulas[i].vel.y
           
            
def simulacao():
    criarCaixa()
    criarParticulas()
    while True:
        loopAnimacao()


# -------------------- Classe das partícula:

class Particula:
    '''
    Classe utilizada para representar cada átomo.
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

janelaW = 800
janelaH = 800
L = 10
numParticulas = 10
dt = 1e-3
d = L/2 + 0.5
espessuraCaixa = 0.05
pointer = False
azul = color.blue
vermelho = color.red

animation = canvas(width=janelaW, height=janelaH, align='left')
animation.range = L

particulas = []


simulacao()