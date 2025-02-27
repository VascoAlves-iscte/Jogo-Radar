from ursina import *
import math, time

class Missile(Entity):
    def __init__(self, target, target_list, start_pos, speed=50, **kwargs):
        # Cria o míssil (modelo simples, ex: uma esfera)
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
            # Calcula a direção do míssil para o target
            direction = (self.target.world_position - self.world_position).normalized()
            # Move o míssil
            self.world_position += direction * self.speed * time.dt

            # Se o míssil se aproximou do target, "explode"
            if distance(self.world_position, self.target.world_position) < self.explosion_distance:
                self.explode()
        else:
            # Se o target não existe mais, destrói o míssil
            destroy(self)

    def explode(self):
        print("Míssil explodiu!")
        # Remover o alvo da lista de targets, se estiver presente.
        if self.target in self.target_list:
            self.target_list.remove(self.target)
        # Agendar a destruição do target e do míssil no próximo frame
        invoke(destroy, self.target, delay=0)
        invoke(destroy, self, delay=0)
