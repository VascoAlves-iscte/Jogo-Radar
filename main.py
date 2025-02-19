from ursina import *
from radar import Radar
from target import Target
import math

app = Ursina()

# 🌌 Skybox para o ambiente
sky = Sky()

# 🟩 Chão (Floor)
floor = Entity(
    model='plane',
    scale=(100, 2, 100),
    texture='white_cube',
    texture_scale=(50, 50),
    color=color.green,
    collider='box'
)
floor.position = (0, 0, 0)

# ✈️ Carregar o modelo F-16
f16_model = load_model('f16CleanWings.obj')

# 🎯 Criar Targets (outros alvos)
targets = [
    Target(model_name='sphere', position=(-5, 1, 0), color=color.red, scale=1, collider='box'),
    Target(model_name='cube', position=(5, 1, 0), color=color.blue, scale=1, collider='box'),
    Target(model_name='sphere', position=(-5, 10, 70), color=color.red, scale=1, collider='box'),
    Target(model_name='cube', position=(5, 25, 35), color=color.blue, scale=1, collider='box')
]

# 🎯 Criar o target do F-16 que se moverá continuamente ao longo do eixo X.
f16_target = Target(model=f16_model, position=(0, 3, 50), color=color.pink, scale=1, collider='box')
targets.append(f16_target)

# Parâmetros de movimento
speed = 5           # Velocidade constante (unidades por segundo)
direction = 1       # 1 para mover para a direita, -1 para mover para a esquerda
x_max = 20          # Limite máximo do eixo X
x_min = -20         # Limite mínimo do eixo X

def update():
    global direction

    # Atualiza a posição do f16_target no eixo X
    f16_target.x += direction * speed * time.dt

    # Verifica os limites e inverte a direção 
    if f16_target.x >= x_max and direction == 1:
        f16_target.x = x_max
        direction = -1  # Muda a direção para a esquerda

    elif f16_target.x <= x_min and direction == -1:
        f16_target.x = x_min
        direction = 1  # Muda a direção para a direita

# 🎯 Criar o Radar e passar os targets
radar = Radar(position=(0, 0, -20), targets=targets)

app.run()
