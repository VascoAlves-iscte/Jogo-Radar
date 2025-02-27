
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


    def update_horizontal_target(target, direction, x_speed, dt):
        # Atualiza a posição horizontal (eixo X) dos alvos que se movem horizontalmente
        if target.x >= 40:
            direction[0] = -1
        elif target.x <= -40:
            direction[0] = 1
        target.x += direction[0] * x_speed * dt

    def update_metal_target(target, z_speed, dt):
        # Atualiza o alvo metal_f16 para que se aproxime do radar no eixo Z
        target.z -= z_speed * dt
        if target.z < 10:
            target.z = 300  # Reinicia para uma posição distante

    def level_update():
        # Parâmetros de velocidade (ajustáveis conforme necessário)
        x_speed = 5         # Velocidade horizontal para os alvos composite e stealth
        z_speed = 50        # Velocidade do F-16 metal no eixo Z
        inbound_speed = 30  # Velocidade para os alvos incoming
        
        radar_position = Vec3(0, 0, 0)
        dt = time.dt  # Delta time
        
        # Atualiza cada target de acordo com o seu tipo
        for target in targets:
            # Se o target for um dos que se movem horizontalmente (composite_f16 ou stealth_f22)
            if target in (composite_f16, stealth_f22):
                update_horizontal_target(target, direction, x_speed, dt)
            # Se o target for o metal_f16 (que se move no eixo Z)
            elif target == metal_f16:
                update_metal_target(target, z_speed, dt)



    return floor, targets, level_update

