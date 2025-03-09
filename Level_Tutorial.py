from ursina import *
from target import Target

# Variável global para controlar o movimento horizontal dos alvos não-incoming.
direction = [1]  # Usamos uma lista para permitir alteração mutável

def load_level_tutorial():
   
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

    stealth_f22 = Target(
        model=f22_model,
        position=(30, 5, 100),
        color=color.orange,
        scale=0.7,
        collider='box',
        material_type="stealth"
    )
    targets.append(stealth_f22)

    def level_update():
        radar_position = Vec3(0, 0, 0)
        # Atualiza a orientação de cada target para que fiquem virados para o radar
        for target in targets:
            target.look_at(radar_position)
    
    return floor, targets, level_update
