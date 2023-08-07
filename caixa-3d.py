# Importações:

from vpython import *
import random

# Definindo uma classe para cada partícula:

class Particula:
    def __init__(self, r, vr):
        x, y, z = r
        vx, vy, vz = vr
        self.pos = vector(x, y, z)
        self.vel = vector(vx, vy, vz)
        
# Parâmetros iniciais:

janelaW = 1900
janelaH = 960
L = 10
numParticulas = 10
dt = 1e-3
raio = 0.5
massa = 1
d = L/2 + raio
espessuraCaixa = 0.05
azul = color.blue
vermelho = color.red

animation = canvas( width=janelaW, height=janelaH)
animation.range = L

# Caixa:

caixaBot = curve(color=azul, radius=espessuraCaixa)
caixaBot.append([vector(-d,-d,-d), vector(-d,-d,d), vector(d,-d,d), vector(d,-d,-d), vector(-d,-d,-d)])
caixaTop = curve(color=azul, radius=espessuraCaixa)
caixaTop.append([vector(-d,d,-d), vector(-d,d,d), vector(d,d,d), vector(d,d,-d), vector(-d,d,-d)])
aresta1 = curve(color=azul, radius=espessuraCaixa)
aresta1.append([vector(-d,-d,d), vector(-d,d,d)])
aresta2 = curve(color=azul, radius=espessuraCaixa)
aresta2.append([vector(-d,-d,-d), vector(-d,d,-d)])
aresta3 = curve(color=azul, radius=espessuraCaixa)
aresta3.append([vector(d,-d,-d), vector(d,d,-d)])
aresta4 = curve(color=azul, radius=espessuraCaixa)
aresta4.append([vector(d,-d,d), vector(d,d,d)])

particulas = []
posicoes = []
velocidades = []

# Criando partículas:

for num in range(numParticulas):
    particula = Particula([random.random() for i in range(3)], [random.randint(0,100) for i in range(3)])
    particulas.append(sphere(pos = particula.pos, radius = raio, color = vermelho))
    posicoes.append(particula.pos)
    velocidades.append(particula.vel)

# Animação:
 
while True:
    rate(300)
    
    # Update
    for num in range(numParticulas): particulas[num].pos = posicoes[num] = posicoes[num] + (velocidades[num]/massa)*dt
    
    # Colisões (parede imaginária lado L)
    for i in range(numParticulas):
        loc = posicoes[i]
        
        if abs(loc.x) > L/2:
            velocidades[i].x = -velocidades[i].x
        
        if abs(loc.y) > L/2:
            velocidades[i].y = -velocidades[i].y
            
        if abs(loc.z) > L/2:
            velocidades[i].z = -velocidades[i].z