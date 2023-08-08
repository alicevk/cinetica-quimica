# -------------------- Importações:

from vpython import *
import random
import itertools

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

def colisao(particula1, particula2):
    '''
    Calcula os vetores resultantes de cada partícula após sua colisão.

    Args:
        particula1 (Particula): representa uma das partículas na colisão
        particula2 (Paerticula): representa a outra particula
        
    Returns:
        _return_ (_type_): 
    '''
    pass

# -------------------- Definindo uma classe para cada partícula:

class Particula:
    '''
    Classe utilizada para representar cada átomo.
    '''
    def __init__(self, r, vr, raio):
        x, y, z = r
        vx, vy, vz = vr
        self.pos = vector(x, y, z)
        self.vel = vector(vx, vy, vz)
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

caixaBot = curve(color=azul, radius=espessuraCaixa)
caixaBot.append([vector(-d,-d,-d), vector(-d,-d,d), vector(d,-d,d), vector(d,-d,-d), vector(-d,-d,-d), vector(-d,d,-d), vector(-d,d,d), vector(-d,-d,d)])
caixaTop = curve(color=azul, radius=espessuraCaixa)
caixaTop.append([vector(d,d,d), vector(d,d,-d), vector(-d,d,-d), vector(-d,d,d), vector(d,d,d), vector(d,-d,d), vector(d,-d,-d), vector(d,d,-d)])

particulas = []
posicoes = []
velocidades = []

# -------------------- Criando partículas:

for num in range(numParticulas):
    particula = Particula([random.randint(-L/2, L/2) for i in range(3)], [random.randint(10,20) for i in range(3)], 0.5)
    particulas.append(sphere(pos = particula.pos, radius = particula.raio, color = vermelho))
    posicoes.append(particula.pos)
    velocidades.append(particula.vel)

# -------------------- Animação:
 
colisao = False
while not colisao:
    rate(300)
    
    # Update
    for num in range(numParticulas): particulas[num].pos = posicoes[num] = posicoes[num] + (velocidades[num]/massa)*dt
    
    # Colisões (parede imaginária de lado L)
    for i in range(numParticulas):
        loc = posicoes[i]
        
        if abs(loc.x) >= L/2:
            velocidades[i].x = -velocidades[i].x
        
        if abs(loc.y) >= L/2:
            velocidades[i].y = -velocidades[i].y
            
        if abs(loc.z) >= L/2:
            velocidades[i].z = -velocidades[i].z

    # Colisão (entre as partículas)
    for particula1, particula2 in itertools.combinations(particulas,2):
        if (particula1 != particula2) and (calcular_distancia(particula1.pos, particula2.pos) <= 1):
            colisao = True
            print(f'Houve uma colisão!!! :)')