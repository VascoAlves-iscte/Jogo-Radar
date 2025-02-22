from ursina import *
from radar import Radar
from target import Target
import math
from perlin_noise import PerlinNoise
import random

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
        y = noise([x * 0.1, z * 0.1])
        y = math.floor(y * height_multiplier)
        block = Entity(
            model='cube',
            scale=(1, 1, 1),
            position=(x, y, z),
            texture='white_cube',
            color=color.green,
            collider='box'
        )
        terrain.append(block)

# ✈️ Carregar os modelos
f16_model = load_model('f16CleanWings.obj')
f22_model = load_model('f22.obj')

# 🎯 Criar Targets (outros alvos)
targets = [
    Target(model_name='sphere', position=(-5, 1, 0), color=color.red, scale=1, collider='box', material_type="metal"),
    Target(model_name='cube', position=(5, 1, 0), color=color.blue, scale=1, collider='box', material_type="plastic"),
    Target(model_name='sphere', position=(-5, 10, 70), color=color.red, scale=1, collider='box', material_type="composite"),
    Target(model_name='cube', position=(5, 25, 35), color=color.blue, scale=1, collider='box', material_type="metal")
]

# 🎯 Criar o target do F-16 que se moverá continuamente ao longo do eixo X.
f16_target = Target(
    model=f16_model,
    position=(0, 3, 50),
    color=color.pink,
    scale=1,                 # Mantemos o F-16 com scale=1
    collider='box',
    material_type="metal"
)
targets.append(f16_target)

# 🎯 Criar o target do F-22, com escala ~1.35 para aproximar melhor a proporção
f22_target = Target(
    model=f22_model,
    position=(0, 5, 50),
    color=color.orange,
    scale=0.87,              # Aumentamos a escala para ~1.35
    collider='box',
    material_type="stealth"
)
targets.append(f22_target)

# Parâmetros de movimento
speed = 5
direction = 1
x_max = 20
x_min = -20

def update():
    global direction
    # Atualiza a posição de ambos os targets (F-16 e F-22) no eixo X
    f16_target.x += direction * speed * time.dt
    f22_target.x += direction * speed * time.dt

    # Se qualquer um dos targets atingir os limites, inverte a direção e ajusta a posição
    if f16_target.x >= x_max or f22_target.x >= x_max:
        f16_target.x = x_max
        f22_target.x = x_max
        direction = -1
    elif f16_target.x <= x_min or f22_target.x <= x_min:
        f16_target.x = x_min
        f22_target.x = x_min
        direction = 1

def input(key):
    if key == 'scroll up':
        camera.fov = clamp(camera.fov - 2, 5, 100)
    elif key == 'scroll down':
        camera.fov = clamp(camera.fov + 2, 10, 100)   

# 🎯 Criar o Radar e passar os targets
radar = Radar(position=(0, 0, -20), targets=targets)

app.run()
