from ursina import *
import math, time
from missile import Missile
from tutorial_slides import TutorialSlides 


class InputController(Entity):
    def __init__(self, radar, targets,game_controller, sensibilidade=100, base_fov=60, **kwargs):
        super().__init__(**kwargs)
        self.radar = radar            # Instância do radar
        self.target_list = targets    # Lista de targets
        self.sensibilidade = sensibilidade
        self.base_fov = base_fov
        self.game_controller = game_controller
        self.smooth_x = 0
        self.smooth_y = 0
        camera.parent = self
        camera.position = (0, 2, 0)
        self._r_pressed = False       # Flag para a tecla 'r'
        self.target_fov = camera.fov

        # Controle de lançamento de mísseis
        self.missile_capacity = 4     # Número máximo de mísseis por carregador
        self.missile_count = 0        # Mísseis já lançados no carregador atual
        self.reload_delay = 3         # Tempo de reload (em segundos)
        self.reloading = False        # Flag que indica se está a recarregar
        self.reload_start_time = None
        self.countermz_start_time=None
        self.countermz_delay=1.5

    def update(self):
        if self.radar.target_locked and self.radar.locked_target:
            direction = self.radar.locked_target.world_position - camera.world_position
            desired_y = math.degrees(math.atan2(direction.x, direction.z))
            horizontal_dist = math.sqrt(direction.x**2 + direction.z**2)
            desired_x = math.degrees(math.atan2(direction.y, horizontal_dist))
            camera.rotation_y = desired_y
            camera.rotation_x = -desired_x
        else:
            sens_factor = camera.fov / self.base_fov
            self.smooth_x = lerp(self.smooth_x, mouse.velocity[0] * self.sensibilidade * sens_factor, time.dt * 10)
            self.smooth_y = lerp(self.smooth_y, mouse.velocity[1] * self.sensibilidade * sens_factor, time.dt * 10)
            camera.rotation_y += self.smooth_x
            camera.rotation_x -= self.smooth_y
            camera.rotation_x = clamp(camera.rotation_x, -45, 45)
        
        camera.fov = lerp(camera.fov, self.target_fov, time.dt * 5)
    
    def input(self, key):

        if key == 'page up':
            try:
                for child in camera.ui.children:
                    if isinstance(child, TutorialSlides):
                        child.next_slide()
                        return
            except Exception as e:
                print("Erro ao avançar o slide:", e)
        
        if key == 'page down':
            try:
                for child in camera.ui.children:
                    if isinstance(child, TutorialSlides):
                        child.prev_slide()
                        return
            except Exception as e:
                print("Erro ao retroceder o slide:", e)

        # Zoom via scroll
        if key == 'scroll up':
            self.target_fov = clamp(self.target_fov - 5, 5, 100)
        elif key == 'scroll down':
            self.target_fov = clamp(self.target_fov + 5, 5, 100)
            
        # Toggle radar com a tecla "r"
        if key == 'r' and not self._r_pressed:
            self._r_pressed = True
            if not self.radar.radar_ligado:
                self.radar.ligar_radar()
            else:
                self.radar.desligar_radar()
        elif key == 'r up':
            self._r_pressed = False

        # Lançar míssil com a barra de espaço, respeitando o limite e o reload
        if key == 'space':
            if self.radar.target_locked and self.radar.locked_target:
                if not self.reloading:
                    if self.missile_count < self.missile_capacity:
                        Missile(target=self.radar.locked_target, target_list=self.target_list, start_pos=self.radar.world_position)
                        self.missile_count += 1
                        print(f"Míssil lançado! [{self.missile_count}/{self.missile_capacity}]")
                        self.countermz_start_time = time.time()
                        invoke(self.countermz, delay=self.reload_delay)                     
                        if self.missile_count == self.missile_capacity:
                            print("Limite de mísseis atingido. Recarregando em 3 segundos...")
                            self.reloading = True
                            self.reload_start_time = time.time()
                            invoke(self.reload_missiles, delay=self.reload_delay)
                    else:
                        print("Aguarde o reload...")
                else:
                    print("Recarregando, aguarde...")

        # Teste manual de ativar contramedidas com a tecla 'c'
        if key == 'c':
            if self.radar.target_locked and self.radar.locked_target:
                self.radar.locked_target.activate_countermeasures()
        
        if key == 'escape':
            if self.game_controller.game_running:
                self.game_controller.create_pause_menu()


    def reload_missiles(self):
        self.missile_count = 0
        self.reloading = False
        self.reload_start_time = None
        print("Recarregado! Pode lançar novos mísseis.")
    
    def countermz (self):
        self.radar.locked_target.activate_countermeasures()
        self.countermz_start_time = None