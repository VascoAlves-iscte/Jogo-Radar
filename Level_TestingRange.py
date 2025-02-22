# level1.py
from ursina import *
import math, random
from perlin_noise import PerlinNoise
from target import Target

# Variável global para controlar o movimento do target móvel.
direction = [1]  # Usamos uma lista para permitir alteração mutável

def load_level_testingrange():
    """
    Cria o terreno (shooting range) e spawna os targets para este nível.
    Retorna:
      - targets: uma lista com todos os targets criados,
      - floor: a entidade que representa o chão,
      - level_update: função que atualiza a posição do único target móvel.
    """
    # Criar o chão (shooting range): um plano de 100 m de largura x 1000 m de comprimento.
    floor = Entity(
        model='plane',
        scale=(100, 2, 1000),
        texture='white_cube',
        texture_scale=(50, 50),
        color=color.green,
        collider='box',
        position=(0, 0, 500)  # O range se estende de z = 0 a z = 1000.
    )
    
    # Carregar os modelos.
    f16_model = load_model('f16CleanWings.obj')
    f22_model = load_model('f22.obj')
    
    
    targets = []
  
    metal_f16 = Target(
        model=f16_model,
        position=(-30, 3, 300),
        color=color.pink,
        scale=1,
        collider='box',
        material_type="metal"
    )
    targets.append(metal_f16)

    composite_f16 = Target(
        model=f16_model,
        position=(0, 3, 200),
        color=color.red,
        scale=1,
        collider='box',
        material_type="composite"
    )
    targets.append(composite_f16)

    stealth_f22 = Target(
        model=f22_model,
        position=(30, 5, 100),
        color=color.orange,
        scale=0.7,  # F-16 em scale=1 equivale a F-22 em scale=0.7
        collider='box',
        material_type="stealth"
    )
    targets.append(stealth_f22)

    
    # Função update do nível: move apenas o target móvel (F-16 metal) no eixo X.
    def level_update():
        if composite_f16.x >= 20 or stealth_f22.x >= 20:
            direction[0] = -1
        elif composite_f16.x <= -20 or stealth_f22.x <= -20:
            direction[0] = 1
        composite_f16.x += direction[0] * 5 * time.dt
        stealth_f22.x += direction[0] * 5 * time.dt
    
    return floor, targets, level_update
