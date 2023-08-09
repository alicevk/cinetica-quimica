# -------------------- Importações:

from vpython import *
import random
import itertools
import numpy as np

# -------------------- Funções:

def calcular_distancia(r1,r2):
    '''
    Calcula a distância euclidiana tridimensional entre os vetores posição r1 e r2.

    Args:
        r1 (vpython vector): vetor posição (x1, y1, z1) da partícula 1
        r2 (vpython vector): vetor posição (x2, y2, z2) da partícula 2

    Returns:
        distancia (float): distância euclidiana entre os vetores r1 e r2
    '''
    x1 = r1.x
    x2 = r2.x
    y1 = r1.y
    y2 = r2.y
    z1 = r1.z
    z2 = r2.z
    distancia = sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z1 - z2)**2)
    return distancia

def angulo_vetorial(v1, v2):
    '''
    Calcula o ângulos entre os vetores de velocidade em radianos.

    Args:
        v1 (vpython vector): vetor velocidade da partícula 1
        v2 (vpython vector): vetor velocidade da partícula 2

    Returns:
        alpha_radianos (float): ângulo formado pelos vetores velocidade de ambas partículas
    '''
    alpha_radianos = np.arccos((v1.x*v2.x + v1.y*v2.y)
                            /(sqrt((v1.x**2 + v1.y**2))
                              * sqrt(v2.x**2 + v2.y**2)))
    return alpha_radianos

def magnitude_vetorial(vr):
    '''
    Calcula a magnitude de um vetor.

    Args:
        vr (vpython vector): vetor velocidade

    Returns:
        magnitude (float): magnitude do vetor vr
    '''
    magnitude = sqrt(vr.x**2 + vr.y**2)
    return magnitude


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

# -------------------- Definindo uma classe para cada partícula:

class Particula:
    '''
    Classe utilizada para representar cada átomo.
    '''
    def __init__(self, r, vr, raio, massa, id, cor, pointer):
        x, y, z = r
        vx, vy, vz = vr
        self.pos = vector(x, y, z)
        self.vel = vector(vx, vy, vz)
        self.raio = raio
        self.massa = massa
        self.id = id
        self.cor = cor
        self.esfera = sphere(pos=self.pos, radius=self.raio, color=self.cor)
        if pointer: self.pointer = arrow(pos=self.esfera.pos, axis=self.vel, length=.75, round=True)
        
# -------------------- Parâmetros iniciais:

janelaW = 1000
janelaH = 1000
L = 10
numParticulas = 10
dt = 1e-3
d = L/2 + 0.5
espessuraCaixa = 0.05
pointer = False
azul = color.blue
vermelho = color.red

animation = canvas(width=janelaW, height=janelaH)
animation.range = L

# -------------------- Caixa:

caixaBot = curve(color=azul, radius=espessuraCaixa)
caixaBot.append([vector(-d,-d,-d), vector(-d,-d,d), vector(d,-d,d), vector(d,-d,-d), vector(-d,-d,-d), vector(-d,d,-d), vector(-d,d,d), vector(-d,-d,d)])
caixaTop = curve(color=azul, radius=espessuraCaixa)
caixaTop.append([vector(d,d,d), vector(d,d,-d), vector(-d,d,-d), vector(-d,d,d), vector(d,d,d), vector(d,-d,d), vector(d,-d,-d), vector(d,d,-d)])

particulas = []

# -------------------- Criando partículas:

for num in range(numParticulas):
    particula = Particula([random.randrange(-L/2,L/2) for i in range(3)],
                          [random.randint(10,20) for i in range(3)],
                          0.3 , 1, num, vermelho, pointer)
    particulas.append(particula)

# -------------------- Animação:

while True:
    rate(300)
    
    # Update
    for num in range(numParticulas):
        particulas[num].esfera.pos += particulas[num].vel*dt
        if pointer:
            particulas[num].pointer.pos = particulas[num].esfera.pos
            particulas[num].pointer.axis = particulas[num].vel
            particulas[num].pointer.length = 0.75

    # Colisão (entre as partículas)
    for particula1, particula2 in itertools.combinations(particulas,2):
        if (calcular_distancia(particula1.esfera.pos, particula2.esfera.pos) <= particula1.raio + particula2.raio):
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
            
        if abs(loc.z) >= L/2:
            particulas[i].vel.z = -particulas[i].vel.z
