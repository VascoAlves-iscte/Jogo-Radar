from ursina import *
import math, time, random  
from target import Target

class Missile(Entity):
    def __init__(self, target, target_list, start_pos, speed=50, **kwargs):
        super().__init__(
            model='sphere',
            color=color.yellow,
            scale=0.5,
            position=start_pos,
            **kwargs
        )
        self.target = target
        self.target_list = target_list  # Guarda a lista de targets
        self.speed = speed
        self.explosion_distance = 2  # Distância para considerar que o míssil atingiu o alvo

    def update(self):
        if self.target and self.target.enabled:
            # Se o target ativou contramedidas, verifica chance de desvio
            if hasattr(self.target, 'countermeasures_active') and self.target.countermeasures_active:
                radar_position = Vec3(0, 0, 0)
                effective_rcs = self.target.get_rcs(radar_position)
                distance_val = (self.target.world_position - radar_position).length()
                # Parâmetros ajustáveis para a fórmula
                base_chance = 0.1
                reference_distance = 100.0
                reference_rcs = 50.0
                # Cálculo da probabilidade
                prob_miss = base_chance * (distance_val / reference_distance) * (reference_rcs / (effective_rcs + 0.001))
                prob_miss = prob_miss*0.01
                if random.random() < prob_miss:
                    print("Míssil desviou devido às contramedidas!")
                    destroy(self)
                    return
                else:
                    self.target.deactivate_countermeasures()

            # Cálculo normal da direção e movimentação do míssil
            direction = (self.target.world_position - self.world_position).normalized()
            self.world_position += direction * self.speed * time.dt

            # Se o míssil se aproximou do target, "explode"
            if distance(self.world_position, self.target.world_position) < self.explosion_distance:
                self.explode()
        else:
            # Se o target não existe mais, destrói o míssil
            destroy(self)

    def explode(self):
        print("Míssil explodiu!")
        if self.target in self.target_list:
            self.target_list.remove(self.target)
        invoke(destroy, self.target, delay=0)
        invoke(destroy, self, delay=0)
