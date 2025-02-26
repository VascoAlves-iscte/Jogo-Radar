from ursina import *
import math

class Missile(Entity):
    def __init__(self, target, start_pos, speed=50, **kwargs):
        # Cria o míssil; aqui pode usar um modelo simples (por exemplo, uma esfera ou cubo)
        super().__init__(
            model='sphere',
            color=color.yellow,
            scale=0.5,
            position=start_pos,
            **kwargs
        )
        self.target = target
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
        # Pode adicionar efeitos visuais e sonoros aqui
        print("Míssil explodiu!")
        # Destrói o target
        destroy(self.target)
        # Destrói o míssil
        destroy(self)