from ursina import *
import math, random
from target import Target

# Variável global para controlar o movimento horizontal dos alvos não-incoming.
direction = [1]  # Usamos uma lista para permitir alteração mutável

def load_level_arena():
    """
    Cria o terreno (shooting range) e spawna os targets para o nível "Arena".
    Retorna:
      - floor: a entidade que representa o chão,
      - targets: uma lista com todos os targets criados (originais e incoming),
      - level_update: função que atualiza a posição dos targets móveis.
    """
    # Cria o chão : um plano de 20 m de largura x 1000 m de comprimento.
    floor = Entity(
        model='plane',
        scale=(20, 1, 1000),
        texture='white_cube',
        texture_scale=(20, 1000),
        color=color.green,
        collider=None,
        position=(0, 0, 1000/2)  # O range se estende de z = 0 a z = 1000.
    )
    
    # Carrega os modelos.
    f16_1 = load_model('f16CleanWings.obj')
    f16_2 = load_model('f16CleanWings.obj')
    f16_3 = load_model('f16CleanWings.obj')
    f16_4 = load_model('f16CleanWings.obj')
    f16_5 = load_model('f16CleanWings.obj')
    f22_model = load_model('f22.obj')
      
    targets = []
    
    # Alvos originais:
    composite_f16 = Target(
        model=f16_1,
        position=(-30, 3, 200),
        color=color.red,
        scale=1,
        collider='box',
        material_type="composite"
    )
    targets.append(composite_f16)

    metal_f16 = Target(
        model=f16_2,
        position=(0, 3, 300),
        color=color.pink,
        scale=1,
        collider='box',
        material_type="metal"
    )
    targets.append(metal_f16)

    stealth_f22 = Target(
        model=f22_model,
        position=(30, 5, 100),
        color=color.orange,
        scale=0.7,
        collider='box',
        material_type="stealth"
    )
    targets.append(stealth_f22)

    # Alvos adicionais: 3 F-16 posicionados num círculo a 400 m do radar (origem)
    # Em vez de manter duas listas, marcamos os alvos adicionais com um atributo 'incoming'
    modelos_incoming = [f16_3, f16_4, f16_5]
    for angle_deg, modelo in zip([0, 120, 240], modelos_incoming):
        angle_rad = math.radians(angle_deg)
        x = 400 * math.cos(angle_rad)
        z = 400 * math.sin(angle_rad)
        incoming_f16 = Target(
            model=modelo,
            position=(x, 3, z),
            color=color.blue,
            scale=1,
            collider='box',
            material_type="metal"
        )
        incoming_f16.incoming = True  # Marca este target como incoming
        targets.append(incoming_f16)
    
    def update_incoming_target(target, radar_position, inbound_speed, dt):
        # Atualiza o alvo "incoming" para que se aproxime do radar
        dir_vector = (radar_position - target.position).normalized()
        target.position += dir_vector * inbound_speed * dt
        # Se o alvo estiver muito próximo (distância < 10), reinicia a sua posição
        if (target.position - radar_position).length() < 10:
            new_distance = random.uniform(400, 500)
            angle = random.uniform(0, 2 * math.pi)
            new_x = new_distance * math.cos(angle)
            new_z = new_distance * math.sin(angle)
            new_y = random.uniform(0, 500)
            target.position = Vec3(new_x, new_y, new_z)

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
            if hasattr(target, 'incoming') and target.incoming:
                update_incoming_target(target, radar_position, inbound_speed, dt)
            elif target in (composite_f16, stealth_f22):
                update_horizontal_target(target, direction, x_speed, dt)
            elif target == metal_f16:
                update_metal_target(target, z_speed, dt)
        
        # Atualiza a orientação de cada target para que fiquem virados para o radar
        for target in targets:
            target.look_at(radar_position)

    
    return floor, targets, level_update
