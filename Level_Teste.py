from ursina import *
import math, random
from perlin_noise import PerlinNoise
from target import Target

# Variável global para controle do movimento dos targets.
direction = [1]  # Usamos uma lista para permitir alteração dentro do update

def load_level_teste():
    """
    Cria o terreno, spawna os targets e retorna:
      - uma lista com as entidades do terreno,
      - uma lista com os targets,
      - a função de update do nível (para o movimento dos targets)
    """
    # Criar o terreno proceduralmente usando Perlin Noise.
    noise = PerlinNoise(octaves=3, seed=random.randint(1, 1000000))
    terrain_size = 50
    height_multiplier = 5
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
    
    # Carregar os modelos
    f16_model = load_model('f16CleanWings.obj')
    f22_model = load_model('f22.obj')
    
    # Criar alguns targets estáticos (exemplo)
    targets = []
    targets.append(Target(model_name='sphere', position=(-5, 1, 0), color=color.red, scale=1, collider='box', material_type="metal"))
    targets.append(Target(model_name='cube', position=(5, 1, 0), color=color.blue, scale=1, collider='box', material_type="plastic"))
    targets.append(Target(model_name='sphere', position=(-5, 10, 70), color=color.red, scale=1, collider='box', material_type="composite"))
    targets.append(Target(model_name='cube', position=(5, 25, 35), color=color.blue, scale=1, collider='box', material_type="metal"))
    
    # Criar os targets que se movem (F-16 e F-22)
    f16_target = Target(
        model=f16_model,
        position=(0, 3, 50),
        color=color.pink,
        scale=1,
        collider='box',
        material_type="metal"
    )
    targets.append(f16_target)
    
    f22_target = Target(
        model=f22_model,
        position=(0, 5, 50),
        color=color.orange,
        scale=0.87,  # F-16 em scale=1 equivale aproximadamente a F-22 em scale=0.87
        collider='box',
        material_type="stealth"
    )
    targets.append(f22_target)
    
    # Função update do nível: move os targets F-16 e F-22 no eixo X.
    def level_update():
        if f16_target.x >= 20 or f22_target.x >= 20:
            direction[0] = -1
        elif f16_target.x <= -20 or f22_target.x <= -20:
            direction[0] = 1
        f16_target.x += direction[0] * 5 * time.dt
        f22_target.x += direction[0] * 5 * time.dt
    
    return terrain, targets, level_update
