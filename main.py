from ursina import *
from radar import Radar
from target import Target
import math
from perlin_noise import PerlinNoise


app = Ursina()

# 🌌 Skybox para o ambiente
sky = Sky()

# 🎛️ Gerar Perlin Noise para o terreno
noise = PerlinNoise(octaves=3, seed=random.randint(1, 1000000))

# Tamanho do terreno
terrain_size = 50  # Número de tiles no terreno
height_multiplier = 5  # Ajusta a altura do terreno

# Criar o terreno proceduralmente
terrain = []
for x in range(-terrain_size // 2, terrain_size // 2):
    for z in range(-terrain_size // 2, terrain_size // 2):
        y = noise([x * 0.1, z * 0.1])  # Normaliza a entrada do Perlin Noise
        y = math.floor(y * height_multiplier)  # Ajusta a altura do terreno

        # Criar cada tile do terreno
        block = Entity(
            model='cube',
            scale=(1, 1, 1),
            position=(x, y, z),
            texture='white_cube',
            color=color.green,
            collider='box'
        )
        terrain.append(block)


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
