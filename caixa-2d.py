# -------------------- Importações:

from vpython import *
import random
import itertools

# -------------------- Funções:

def calcular_distancia(r1, r2):
    '''
    Calcula a distância euclidiana bidimensional entre os vetores posição r1 e r2.

    Args:
        r1 (vpython vector): vetor posição (x1, y1, 0) da partícula 1
        r2 (vpython vector): vetor posição (x2, y2, 0) da partícula 2

    Returns:
        distancia (float): distância euclidiana entre os vetores r1 e r2
    '''
    x1 = r1.x
    x2 = r2.x
    y1 = r1.y
    y2 = r2.y
    distancia = sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return distancia

def colisao(particula1, particula2):
    '''
    Calcula os vetores resultantes de cada partícula após sua colisão.

    Args:
        particula1 (Particula): representa uma das partículas na colisão
        particula2 (Paerticula): representa a outra particula
        
    Returns:
        _return_ (_type_): 
    '''

# -------------------- Definindo uma classe para cada partícula:

class Particula:
    '''
    Classe utilizada para representar cada átomo.
    '''
    def __init__(self, r, vr, raio):
        x, y = r
        vx, vy = vr
        self.pos = vector(x, y, 0)
        self.vel = vector(vx, vy, 0)
        self.raio = raio
        
# -------------------- Parâmetros iniciais:

janelaW = 1000
janelaH = 1000
L = 10
numParticulas = 10
dt = 1e-3
massa = 1
d = L/2 + 0.5
espessuraCaixa = 0.05
azul = color.blue
vermelho = color.red

animation = canvas(width=janelaW, height=janelaH)
animation.range = L

# -------------------- Caixa:

caixa = curve(color=azul, radius=espessuraCaixa)
caixa.append([vector(-d,-d,0), vector(-d,d,0), vector(d,d,0), vector(d,-d,0), vector(-d,-d,0)])

particulas = []
posicoes = []
velocidades = []

# -------------------- Criando partículas:

for num in range(numParticulas):
    particula = Particula([random.randint(-L/2,L/2) for i in range(2)], [random.randint(10,20) for i in range(2)], 0.5)
    particulas.append(sphere(pos = particula.pos, radius = particula.raio, color = vermelho))
    posicoes.append(particula.pos)
    velocidades.append(particula.vel)

# -------------------- Animação:

colisao = False
while not colisao:
    rate(300)
    
    # Update
    for num in range(numParticulas): particulas[num].pos = posicoes[num] = posicoes[num] + velocidades[num]*dt
    
    # Colisões (parede imaginária de lado L)
    for i in range(numParticulas):
        loc = posicoes[i]
        
        if abs(loc.x) >= L/2:
            velocidades[i].x = -velocidades[i].x
        
        if abs(loc.y) >= L/2:
            velocidades[i].y = -velocidades[i].y

    # Colisão (entre as partículas)
    for particula1, particula2 in itertools.combinations(particulas,2):
        if (calcular_distancia(particula1.pos, particula2.pos) <= 1):
            colisao = True
            print(f'Houve uma colisão!!! :)')