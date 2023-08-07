# Importações:

from vpython import *
import random

# Definindo uma classe para cada partícula:

class Particula:
    def __init__(self, r, vr, raio):
        x, y = r
        vx, vy = vr
        self.pos = vector(x, y, 0)
        self.vel = vector(vx, vy, 0)
        self.raio = raio
        
# Parâmetros iniciais:

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

# Caixa:

caixa = curve(color=azul, radius=espessuraCaixa)
caixa.append([vector(-d,-d,0), vector(-d,d,0), vector(d,d,0), vector(d,-d,0), vector(-d,-d,0)])

particulas = []
posicoes = []
velocidades = []

# Criando partículas:

for num in range(numParticulas):
    particula = Particula([random.random() for i in range(2)], [random.randint(0,100) for i in range(2)], 0.5)
    particulas.append(sphere(pos = particula.pos, radius = particula.raio, color = vermelho))
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
