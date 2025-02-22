from ursina import *

class InputController(Entity):
    def __init__(self, radar, sensibilidade=100, base_fov=60, **kwargs):
        super().__init__(**kwargs)
        self.radar = radar  # Guarda a instância do radar
        self.sensibilidade = sensibilidade
        self.base_fov = base_fov
        self.smooth_x = 0
        self.smooth_y = 0
        camera.parent = self
        camera.position = (0, 2, 0)
        self._r_pressed = False  # Flag para a tecla 'r'
    
    def update(self):
        sens_factor = camera.fov / self.base_fov
        self.smooth_x = lerp(self.smooth_x, mouse.velocity[0] * self.sensibilidade * sens_factor, time.dt * 10)
        self.smooth_y = lerp(self.smooth_y, mouse.velocity[1] * self.sensibilidade * sens_factor, time.dt * 10)
        
        camera.rotation_y += self.smooth_x
        camera.rotation_x -= self.smooth_y
        camera.rotation_x = clamp(camera.rotation_x, -45, 45)
    
    def input(self, key):
        # Zoom via scroll
        if key == 'scroll up':
            camera.fov = clamp(camera.fov - 2, 5, 100)
        elif key == 'scroll down':
            camera.fov = clamp(camera.fov + 2, 5, 100)
            
        # Toggle radar usando a tecla "r", garantindo que só ocorra uma vez por pressionamento.
        if key == 'r' and not self._r_pressed:
            self._r_pressed = True
            if not self.radar.radar_ligado:
                self.radar.ligar_radar()
            else:
                self.radar.desligar_radar()
        elif key == 'r up':
            self._r_pressed = False
