
from ursina import *

class CameraController(Entity):
    def __init__(self, sensibilidade=100, base_fov=60, **kwargs):
        super().__init__(**kwargs)
        self.sensibilidade = sensibilidade
        self.base_fov = base_fov
        self.smooth_x = 0
        self.smooth_y = 0
        camera.parent = self
        camera.position = (0, 2, 0)
    
    def update(self):
        # Ajusta a sensibilidade em função do fov: quanto menor o fov, menor a sensibilidade.
        # Por exemplo, podemos usar um fator igual a (camera.fov / base_fov).
        sens_factor = camera.fov / self.base_fov

        self.smooth_x = lerp(self.smooth_x, mouse.velocity[0] * self.sensibilidade * sens_factor, time.dt * 10)
        self.smooth_y = lerp(self.smooth_y, mouse.velocity[1] * self.sensibilidade * sens_factor, time.dt * 10)
        
        camera.rotation_y += self.smooth_x
        camera.rotation_x -= self.smooth_y
        camera.rotation_x = clamp(camera.rotation_x, -45, 45)

    
    def input(self, key):
        # Implementa o zoom via scroll do mouse.
        if key == 'scroll up':
            camera.fov = clamp(camera.fov - 2, 5, 100)
        elif key == 'scroll down':
            camera.fov = clamp(camera.fov + 2, 5, 100)
