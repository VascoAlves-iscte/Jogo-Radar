from ursina import *
from missile import Missile

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
        self.target_fov = camera.fov
    
    def update(self):

        if self.radar.target_locked and self.radar.locked_target:
            # Calcula a direção desejada para a câmera olhar
            direction = self.radar.locked_target.world_position - camera.world_position
            desired_y = math.degrees(math.atan2(direction.x, direction.z))
            horizontal_dist = math.sqrt(direction.x**2 + direction.z**2)
            desired_x = math.degrees(math.atan2(direction.y, horizontal_dist))
            # Suaviza a transição: use lerp para os ângulos atuais da câmera
            camera.rotation_y = desired_y
            camera.rotation_x = -desired_x

        else:
            sens_factor = camera.fov / self.base_fov
            self.smooth_x = lerp(self.smooth_x, mouse.velocity[0] * self.sensibilidade * sens_factor, time.dt * 10)
            self.smooth_y = lerp(self.smooth_y, mouse.velocity[1] * self.sensibilidade * sens_factor, time.dt * 10)
            
            camera.rotation_y += self.smooth_x
            camera.rotation_x -= self.smooth_y
            camera.rotation_x = clamp(camera.rotation_x, -45, 45)
        
            
        # Atualiza o FOV da câmara suavemente em direção ao target_fov:
        camera.fov = lerp(camera.fov, self.target_fov, time.dt * 5)

    
    def input(self, key):
        # Zoom via scroll: atualiza target_fov em vez de alterar camera.fov diretamente
        if key == 'scroll up':
            self.target_fov = clamp(self.target_fov - 5, 5, 100)
        elif key == 'scroll down':
            self.target_fov = clamp(self.target_fov + 5, 5, 100)
            
        # Toggle radar usando a tecla "r", garantindo que só ocorra uma vez por pressionamento.
        if key == 'r' and not self._r_pressed:
            self._r_pressed = True
            if not self.radar.radar_ligado:
                self.radar.ligar_radar()
            else:
                self.radar.desligar_radar()
        elif key == 'r up':
            self._r_pressed = False

        # Lançar míssil com a barra de espaço se houver um lock
        if key == 'space':
            if self.radar.target_locked and self.radar.locked_target:
                # Cria um míssil a partir da posição do radar (ou outra posição definida)
                Missile(target=self.radar.locked_target, start_pos=self.radar.world_position)
