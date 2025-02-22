from ursina import *
import time
import random  

class Radar(Entity):
    def __init__(self, position=(20, 1, -20), targets=None, **kwargs):
        super().__init__(position=position, **kwargs)
        
        # Removemos a configuração da câmera deste módulo.
        
        # 🎯 UI Elements
        # Note que agora o crosshair é aninhado à UI da câmera para não interferir nos inputs 3D.
        self.crosshair = Text('+', scale=2, position=(0,0), origin=(0,0), color=color.yellow, parent=camera.ui)
        self.crosshair.ignore = True

        self.radar_text = Text(text="RADAR LIGADO", scale=2, origin=(0,0), position=(0,0.4), color=color.orange, enabled=False)
        self.radar_lock_text = Text(text="LOCK", scale=2, origin=(0,0), position=(0,0.35), color=color.red, enabled=False)

        # 🎯 Radar State Variables
        self.radar_ligado = False
        self.target_locked = False  
        self.sensibilidade = 100  
        self.last_lock_check = time.time()  
        self.lock_on_timer = None  
        self.lock_on_delay = random.uniform(3, 5)  

        # 🎯 Sound Configuration
        self.som_radar = Audio('radar_beep.mp3', autoplay=False, loop=True)  
        self.som_radar_fast = Audio('radar_beep_fast.mp3', autoplay=False, loop=True)  
        self.som_radar_lock = Audio('radar_lock.mp3', autoplay=False, loop=True)  

        # 🎯 Mouse & Window Configuration
        mouse.visible = False  
        mouse.locked = True  
        window.exit_button.enabled = False  
        window.fullscreen = False  
        window.focused = True  

        self.targets = targets if targets else []

    # 🔥 ======================= RADAR CONTROLS ======================= 🔥 #

    def ligar_radar(self):
        self.radar_ligado = True
        self.radar_text.enabled = True  
        self.som_radar.play()  
        self.target_locked = False  
        self.lock_on_timer = None  
        print("Radar ligado - Som ativado")
        invoke(self.check_target_status, delay=0.2)  

    def desligar_radar(self):
        self.radar_ligado = False
        self.radar_text.enabled = False  
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
            print(f"📡 RCS captado: {rcs:.2f}")
            print(f"🎯 Target detected: {hit_info.entity} at {hit_info.distance:.2f} units")
            return True  
        return False  

    def start_fast_beep_timer(self):
        if self.radar_ligado and not self.target_locked:
            self.lock_on_timer = time.time()  
            self.som_radar.stop()
            self.som_radar_fast.play()  
            self.blink_lock_text()
            print(f"🔄 Fast beep active! Lock-on in {self.lock_on_delay:.2f}s")
            invoke(self.lock_target, delay=self.lock_on_delay)  

    def blink_lock_text(self):
        if self.radar_ligado and not self.target_locked:
            self.radar_lock_text.enabled = not self.radar_lock_text.enabled  
            invoke(self.blink_lock_text, delay=0.3)  

    def lock_target(self):
        if self.radar_ligado and self.is_target_in_view():
            self.som_radar_fast.stop()  
            self.som_radar_lock.play()  
            self.target_locked = True
            self.radar_lock_text.enabled = True  
            print("🔒 Lock-On Achieved!")

    def check_target_status(self):
        if not self.radar_ligado:
            return  
        if self.is_target_in_view():
            if not self.target_locked and self.lock_on_timer is None:
                self.start_fast_beep_timer()  
        else:
            if self.target_locked or self.lock_on_timer:
                self.reset_to_normal_beep()  
        invoke(self.check_target_status, delay=0.2)  

    def reset_to_normal_beep(self):
        self.som_radar_fast.stop()
        self.som_radar_lock.stop()
        self.som_radar.play()  
        self.target_locked = False
        self.radar_lock_text.enabled = False  
        self.lock_on_timer = None  
        print("🔄 Lock lost! Back to normal beep.")

    def input(self, key):
        if key == 'r':  
            if not self.radar_ligado:
                self.ligar_radar()
            else:
                self.desligar_radar()

    # Removemos as definições de movimento da câmera deste update,
    # pois elas agora estão centralizadas na classe CameraController.
    def update(self):
        if self.radar_ligado and (time.time() - self.last_lock_check > 0.2):
            self.last_lock_check = time.time()
