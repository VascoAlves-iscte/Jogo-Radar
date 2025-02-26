
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
      - floor: a entidade que representa o chão,
      - targets: uma lista com todos os targets criados,
      - level_update: função que atualiza a posição do único target móvel.
    """
    # Define as dimensões do terreno
    width = 20    # Largura (em unidades)
    length = 1000 # Comprimento (em unidades)

    # Cria o terreno como um plano
    floor = Entity(
        model='plane',
        scale=(width, 1, length),
        texture='white_cube',
        texture_scale=(width, length),
        color=color.green,
        collider=None,
        position=(0, 0, length / 2)
    )

    # Carrega os modelos
    f16_1 = load_model('f16CleanWings.obj')
    f16_2 = load_model('f16CleanWings.obj')
    f22 = load_model('f22.obj')
      
    targets = []
    
    # Alteramos para carregar explicitamente o modelo da esfera
    
    bola = Target(model='sphere', position=(0, 1, 10), color=color.red, scale=1, collider='box', material_type="metal")
    targets.append(bola)
    print("Bola criada em:", bola.position)

    stealth_f22 = Target(model=f22, position=(30, 5, 100), color=color.orange, scale=0.80, collider='box', material_type="stealth")
    targets.append(stealth_f22)

    metal_f16 = Target(model=f16_1, position=(0, 3, 300), color=color.pink, scale=1, collider='box', material_type="metal")
    targets.append(metal_f16)

    composite_f16 = Target(model=f16_2, position=(-30, 3, 200), color=color.red, scale=1, collider='box', material_type="composite")
    targets.append(composite_f16)


    

    # Velocidade de movimento horizontal (para composite_f16 e stealth_f22)
    x_speed = 5
    # Velocidade do F-16 metal no eixo Z (aproximando-se do radar)
    z_speed = 50

    def level_update():
        # Atualiza a posição horizontal dos alvos, se existirem e estiverem ativos.
        if composite_f16 and composite_f16.enabled:
            composite_f16.x += direction[0] * x_speed * time.dt
        if stealth_f22 and stealth_f22.enabled:
            stealth_f22.x += direction[0] * x_speed * time.dt

        # Verifica se algum dos alvos horizontais ultrapassou os limites e inverte a direção.
        # Aqui, usamos as verificações individualmente para cada target.
        if (composite_f16 and composite_f16.x > 40) or (stealth_f22 and stealth_f22.x > 40):
            if composite_f16:
                composite_f16.x = min(composite_f16.x, 40)
            if stealth_f22:
                stealth_f22.x = min(stealth_f22.x, 40)
            direction[0] = -1
        elif (composite_f16 and composite_f16.x < -40) or (stealth_f22 and stealth_f22.x < -40):
            if composite_f16:
                composite_f16.x = max(composite_f16.x, -40)
            if stealth_f22:
                stealth_f22.x = max(stealth_f22.x, -40)
            direction[0] = 1

        # Atualiza a posição do F-16 metal no eixo Z, se existir e estiver ativo.
        if metal_f16 and metal_f16.enabled:
            metal_f16.z -= z_speed * time.dt
            # Se o F-16 metal estiver muito próximo (por exemplo, z < 10), reinicia-o para uma posição distante (por exemplo, z = 300)
            if metal_f16.z < 10:
                metal_f16.z = 300


    return floor, targets, level_update

