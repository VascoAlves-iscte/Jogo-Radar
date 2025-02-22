from ursina import *
from radar import Radar
from target import Target
import random

app = Ursina()

# Skybox para o ambiente
sky = Sky()

# Shooting Range: um plano de 100 m (largura, eixo X) x 1000 m (comprimento, eixo Z)
# O plano é posicionado de forma que se estenda de z = 0 a z = 1000.
floor = Entity(
    model='plane',
    scale=(100, 2, 1000),
    texture='white_cube',
    texture_scale=(50, 50),
    color=color.green,
    collider='box',
    position=(0, 0, 500)
)

# Carregar os modelos
f16_model = load_model('f16CleanWings.obj')
f22_model = load_model('f22.obj')

# Definir as distâncias (em metros) para os alvos ao longo do eixo Z.
distances = [200, 400, 600, 800, 1000]

# Criar os alvos para cada distância:
# - F-16 metal: x = -30, y = 3, cor rosa, material "metal", scale=1.
# - F-16 composite: x = 0, y = 3, cor vermelha, material "composite", scale=1.
# - F-22 stealth: x = 30, y = 5, cor laranja, material "stealth", scale=0.7.
targets = []
for d in distances:
    metal_f16 = Target(
        model=f16_model,
        position=(-30, 3, d),
        color=color.pink,
        scale=1,
        collider='box',
        material_type="metal"
    )
    composite_f16 = Target(
        model=f16_model,
        position=(0, 3, d),
        color=color.red,
        scale=1,
        collider='box',
        material_type="composite"
    )
    stealth_f22 = Target(
        model=f22_model,
        position=(30, 5, d),
        color=color.orange,
        scale=0.7,
        collider='box',
        material_type="stealth"
    )
    targets.extend([metal_f16, composite_f16, stealth_f22])

# Posicionar o Radar (e sua câmera) na ponta do shooting range.
# Aqui, posicionamos o radar em (0, 10, 0) para que a câmera fique próxima da entrada e visualize todo o range.
radar = Radar(position=(0, 10, 0), targets=targets)

# Função input para capturar o scroll do mouse e ajustar o zoom.
def input(key):
    if key == 'scroll up':
        camera.fov = clamp(camera.fov - 2, 5, 100)
    elif key == 'scroll down':
        camera.fov = clamp(camera.fov + 2, 10, 100)



app.run()
