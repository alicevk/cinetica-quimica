# Importações:

from vpython import *
import random

# Definindo uma classe para cada partícula:

class Particula:
    def __init__(self, x, y, z, vx, vy, vz):
        self.pos = vector(x, y, z)
        self.vel = vector(vx, vy, vz)
        
# Parâmetros iniciais:

win = 1000
L = 10
numParticulas = 10
dt = 1e-3
raio = 0.5
massa = 1
d = L/2 + raio
espessuraCaixa = 0.05
azul = color.blue
vermelho = color.red

animation = canvas( width=win, height=win)
animation.range = L

# Caixa:

boxbottom = curve(color=azul, radius=espessuraCaixa)
boxbottom.append([vector(-d,-d,-d), vector(-d,-d,d), vector(d,-d,d), vector(d,-d,-d), vector(-d,-d,-d)])
boxtop = curve(color=azul, radius=espessuraCaixa)
boxtop.append([vector(-d,d,-d), vector(-d,d,d), vector(d,d,d), vector(d,d,-d), vector(-d,d,-d)])
vert1 = curve(color=azul, radius=espessuraCaixa)
vert2 = curve(color=azul, radius=espessuraCaixa)
vert3 = curve(color=azul, radius=espessuraCaixa)
vert4 = curve(color=azul, radius=espessuraCaixa)
vert1.append([vector(-d,-d,-d), vector(-d,d,-d)])
vert2.append([vector(-d,-d,d), vector(-d,d,d)])
vert3.append([vector(d,-d,d), vector(d,d,d)])
vert4.append([vector(d,-d,-d), vector(d,d,-d)])

particulas = []
posicoes = []
velocidades = []

# Criando partículas:

for num in range(numParticulas):
    particula = Particula(random.randint(0,1), random.randint(0,1),  random.randint(0,1),  random.randint(0,100),  random.randint(0,100),  random.randint(0,100))
    particulas.append(sphere(pos = particula.pos, radius = raio, color = vermelho))
    posicoes.append(particula.pos)
    velocidades.append(particula.vel)

# Animação:
 
while True:
    rate(300)
    
    # Update
    for num in range(numParticulas): particulas[num].pos = posicoes[num] = posicoes[num] + (velocidades[num]/massa)*dt
    
    # Colisões (parede lado L)
    for i in range(numParticulas):
        loc = posicoes[i]
        if abs(loc.x) > L/2:
            if loc.x < 0: velocidades[i].x =  abs(velocidades[i].x)
            else: velocidades[i].x =  -abs(velocidades[i].x)
        
        if abs(loc.y) > L/2:
            if loc.y < 0: velocidades[i].y = abs(velocidades[i].y)
            else: velocidades[i].y =  -abs(velocidades[i].y)
            
        if abs(loc.z) > L/2:
            if loc.z < 0: velocidades[i].z = abs(velocidades[i].z)
            else: velocidades[i].z =  -abs(velocidades[i].z)
