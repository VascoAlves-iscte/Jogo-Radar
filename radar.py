from ursina import *
import time
import random  

class Radar(Entity):
    def __init__(self, position=(20, 1, -20), targets=None, **kwargs):
        super().__init__(position=position, **kwargs)
        
        # UI Elements (os elementos de UI estão aninhados à câmera para não interferirem nos inputs 3D)
        self.crosshair = Text('+', scale=2, position=(0, 0), origin=(0, 0), color=color.yellow, parent=camera.ui)
        self.radar_text = Text(text="RADAR LIGADO", scale=2, origin=(0, 0), position=(0, 0.4), color=color.orange, enabled=False)
        self.radar_lock_text = Text(text="LOCK", scale=2, origin=(0, 0), position=(0, 0.35), color=color.red, enabled=False)
        self.crosshair.ignore = True
        self.radar_text.ignore = True
        self.radar_lock_text.ignore = True

        # Radar State Variables
        self.radar_ligado = False
        self.target_locked = False  
        self.sensibilidade = 100  
        self.last_lock_check = time.time()  
        self.last_status_check = time.time()
        self.lock_on_timer = None  
        self.lock_on_delay = random.uniform(3, 5) 
        self.locked_target= None 

        # Variáveis para o blink do texto "LOCK"
        self.blink_interval = 0.3
        self.last_blink_time = time.time()

        # Sound Configuration
        self.som_radar = Audio('radar_beep.mp3', autoplay=False, loop=True)  
        self.som_radar_fast = Audio('radar_beep_fast.mp3', autoplay=False, loop=True)  
        self.som_radar_lock = Audio('radar_lock.mp3', autoplay=False, loop=True)  

        # Mouse & Window Configuration
        mouse.visible = False  
        mouse.locked = True  
        window.exit_button.enabled = False  
        window.fullscreen = False  
        window.focused = True  

        self.targets = targets if targets else []

    # Métodos de controle do radar
    def ligar_radar(self):
        self.radar_ligado = True
        self.radar_text.enabled = True  
        self.som_radar.play()  
        self.target_locked = False  
        self.lock_on_timer = None  
        print("Radar ligado - Som ativado")
        # A verificação de status será feita no update()

    def desligar_radar(self):
        self.radar_ligado = False
        self.radar_text.enabled = False  
        self.target_locked = False  
        self.som_radar.stop()
        self.som_radar_fast.stop()
        self.som_radar_lock.stop()  
        self.lock_on_timer = None  
        self.radar_lock_text.enabled = False
        print("Radar desligado - Som desativado")

    def is_target_in_view(self):
        max_distance = 1000  
        hit_info = raycast(
            origin=camera.world_position, 
            direction=camera.forward,  
            distance=max_distance, 
            ignore=[camera],  
            debug=True  
        )
        if hit_info.hit and hit_info.entity in self.targets:
            rcs = hit_info.entity.get_rcs(self.world_position)
            self.locked_target=hit_info.entity
            print(f"📡 RCS captado: {rcs:.2f}")
            print(f"🎯 Target detected: {hit_info.entity} at {hit_info.distance:.2f} units")
            return True  
        return False  

    def start_fast_beep_timer(self):
        if self.radar_ligado and not self.target_locked:
            self.lock_on_timer = time.time()
            self.som_radar.stop()
            self.som_radar_fast.play()
            print(f"🔄 Fast beep active! Lock-on in {self.lock_on_delay:.2f}s")
            # O lock_target será chamado via verificação de tempo no update()

    def lock_target(self):
        if self.radar_ligado and self.is_target_in_view():
            self.som_radar_fast.stop()
            self.som_radar_lock.play()
            self.target_locked = True
            self.radar_lock_text.enabled = True
            print("🔒 Lock-On Achieved!")

    def reset_to_normal_beep(self):
        self.som_radar_fast.stop()
        self.som_radar_lock.stop()
        self.som_radar.play()
        self.target_locked = False
        self.radar_lock_text.enabled = False
        self.lock_on_timer = None
        print("🔄 Lock lost! Back to normal beep.")

    def check_target_status(self):
        if not self.radar_ligado:
            return
        if self.is_target_in_view():
            if not self.target_locked and self.lock_on_timer is None:
                self.start_fast_beep_timer()
        else:
            if self.target_locked or self.lock_on_timer:
                self.reset_to_normal_beep()

    def update(self):
        current_time = time.time()
        # Verifica o status dos targets periodicamente.
        if current_time - self.last_status_check > 0.5:
            self.last_status_check = current_time
            self.check_target_status()

        # Se o radar está ligado, vamos atualizar a visibilidade do texto "LOCK":
        if self.radar_ligado:
            if self.target_locked:
                # Quando locked, o texto permanece ativo de forma permanente.
                self.radar_lock_text.enabled = True
            else:
                # Se não estiver locked e houver target na mira, efetua o blink.
                if self.is_target_in_view():
                    if current_time - self.last_blink_time > self.blink_interval:
                        self.radar_lock_text.enabled = not self.radar_lock_text.enabled
                        self.last_blink_time = current_time
                else:
                    self.radar_lock_text.enabled = False

        # Se um lock_on_timer foi iniciado e o tempo decorrido for maior que lock_on_delay, dispara o lock.
        if self.lock_on_timer is not None and not self.target_locked:
            if current_time - self.lock_on_timer >= self.lock_on_delay:
                self.lock_target()
                self.lock_on_timer = None

        # Atualiza o last_lock_check (se necessário para outros usos)
        if self.radar_ligado and (current_time - self.last_lock_check > 0.5):
            self.last_lock_check = current_time
