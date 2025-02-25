import math
from ursina import Vec3
from panda3d.core import CollisionRay, CollisionNode, CollisionTraverser, CollisionHandlerQueue, BitMask32, NodePath

def fresnel_reflection(angle, refractive_index):
    """
    Calcula o coeficiente de reflexão usando a aproximação de Schlick.
    angle: ângulo de incidência em graus.
    refractive_index: índice de refração do material (assumindo n1=1 para o ar).
    """
    cos_theta = abs(math.cos(math.radians(angle)))
    R0 = ((1 - refractive_index) / (1 + refractive_index)) ** 2
    R = R0 + (1 - R0) * ((1 - cos_theta) ** 5)
    return max(0.01, min(R, 1.0))

def obter_normal_colisao(radar_position, target):
    """
    Dispara um CollisionRay do radar em direção ao target para obter a normal da superfície
    no ponto de colisão. Retorna um vetor (Vec3) ou None se não houver colisão.
    """
    ray = CollisionRay()
    ray.setOrigin(radar_position)
    ray.setDirection((target.world_position - radar_position).normalized())
    
    cn = CollisionNode('rcs_ray')
    cn.addSolid(ray)
    cn.setFromCollideMask(BitMask32.bit(1))
    cn.setIntoCollideMask(BitMask32.allOff())
    
    ray_np = NodePath(cn)
    ray_np.reparentTo(target)
    
    traverser = CollisionTraverser()
    handler = CollisionHandlerQueue()
    traverser.addCollider(ray_np, handler)
    
    traverser.traverse(target)
    
    if handler.getNumEntries() > 0:
        handler.sortEntries()
        entry = handler.getEntry(0)
        result = entry.getSurfaceNormal(target)
    else:
        result = None
    ray_np.removeNode()
    return result

def obter_normal_colisao_com_direcao(radar_position, target, direction):
    """
    Dispara um CollisionRay do radar na direção especificada para obter a normal da superfície
    no ponto de colisão. Retorna um vetor (Vec3) ou None se não houver colisão.
    """
    ray = CollisionRay()
    ray.setOrigin(radar_position)
    ray.setDirection(direction)
    
    cn = CollisionNode('rcs_ray')
    cn.addSolid(ray)
    cn.setFromCollideMask(BitMask32.bit(1))
    cn.setIntoCollideMask(BitMask32.allOff())
    
    ray_np = NodePath(cn)
    ray_np.reparentTo(target)
    
    traverser = CollisionTraverser()
    handler = CollisionHandlerQueue()
    traverser.addCollider(ray_np, handler)
    
    traverser.traverse(target)
    
    if handler.getNumEntries() > 0:
        handler.sortEntries()
        entry = handler.getEntry(0)
        result = entry.getSurfaceNormal(target)
    else:
        result = None
    ray_np.removeNode()
    return result

def calcular_rcs_com_colisao(target, radar_position, max_angle=180):
    """
    Calcula o RCS do target utilizando a normal obtida via colisão.
    Em vez de lançar um único raycast, lança múltiplos raios dentro de um pequeno cone
    em torno da direção central do feixe e retorna uma média ponderada dos valores.
    
    Se a colisão retornar uma normal válida, essa normal é usada para o cálculo.
    Caso contrário, utiliza-se target.up como fallback.
    O parâmetro max_angle agora é 180°, permitindo capturar raios até esse ângulo.
    
    Além disso, a função aplica um fator de atenuação baseado na distância entre o radar e o target,
    fazendo com que alvos distantes tenham um RCS efetivo menor.
    """
    # --- Debug: Imprime o nome do modelo do alvo usando get_model_name() ---
    print(f"[DEBUG] Target model: {target.get_model_name()}", flush=True)
    
    num_rays = 10            # Número de raios a lançar
    cone_angle = 5          # Ângulo total do cone (em graus)
    
    # Direção central: do radar até o target
    central_direction = (target.world_position - radar_position).normalized()
    
    rcs_sum = 0.0
    weight_sum = 0.0
    
    # Lança raios uniformemente distribuídos no cone horizontal
    for i in range(num_rays):
        # Calcula um desvio (delta) de -cone_angle/2 até +cone_angle/2
        delta = (i - (num_rays - 1) / 2.0) * (cone_angle / (num_rays - 1))
        angle_rad = math.radians(delta)
        new_x = central_direction.x * math.cos(angle_rad) + central_direction.z * math.sin(angle_rad)
        new_y = central_direction.y
        new_z = -central_direction.x * math.sin(angle_rad) + central_direction.z * math.cos(angle_rad)
        new_direction = Vec3(new_x, new_y, new_z).normalized()
        
        # Obtém a normal para esse raio
        normal_colisao = obter_normal_colisao_com_direcao(radar_position, target, new_direction)
        if normal_colisao is None:
            normal_colisao = target.up  # fallback
        
        incidence_angle = math.degrees(math.acos(max(-1.0, min(1.0, new_direction.dot(normal_colisao)))))
        reflection_coefficient = fresnel_reflection(incidence_angle, target.refractive_index)
        
        scalar = 2 * new_direction.dot(normal_colisao)
        reflected_wave = (new_direction - (normal_colisao * scalar)).normalized()
        
        radar_direction = (radar_position - target.world_position).normalized()
        reflection_angle = math.degrees(math.acos(max(-1.0, min(1.0, reflected_wave.dot(radar_direction)))))
        
        print(f"\n[DEBUG] Ray {i}:", flush=True)
        print(f"    Delta: {delta:.2f}°", flush=True)
        print(f"    Incidence Angle: {incidence_angle:.2f}°", flush=True)
        print(f"    Reflection Angle: {reflection_angle:.2f}°", flush=True)
        print(f"    Reflection Coefficient: {reflection_coefficient:.4f}", flush=True)
        print(f"[DEBUG] Target model: {target.get_model_name()}", flush=True)
        
        # Calcula o RCS para esse raio com max_angle = 180°
        rcs_value = reflection_coefficient * (1 - (reflection_angle / max_angle)) * 100
        print(f"    RCS (ray): {rcs_value:.2f}", flush=True)
        
        weight = new_direction.dot(central_direction)
        print(f"    Weight: {weight:.2f}", flush=True)
        rcs_sum += rcs_value * weight
        weight_sum += weight
    
    if weight_sum != 0:
        weighted_rcs = rcs_sum / weight_sum
    else:
        weighted_rcs = 0.1

    # Incorpora atenuação por distância: quanto mais longe, menor o RCS efetivo.
    distance = (target.world_position - radar_position).length()
    d0 = 100.0  # distância de referência
    attenuation = 1 / (1 + (distance / d0) ** 2)
    effective_rcs = weighted_rcs * attenuation

    print(f"\n[DEBUG] Weighted RCS: {weighted_rcs:.2f}", flush=True)
    print(f"[DEBUG] Distance: {distance:.2f}  Attenuation: {attenuation:.2f}  Effective RCS: {effective_rcs:.2f}", flush=True)
    return effective_rcs
