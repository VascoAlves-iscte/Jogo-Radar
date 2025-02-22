from ursina import *
import time
import random  

class Radar(Entity):
    def __init__(self, position=(20, 1, -20), targets=None, **kwargs):
        super().__init__(position=position, **kwargs)

        # 🎯 Camera Configuration
        camera.parent = self
        camera.position = (0, 2, 0)  

        # 🎯 UI Elements
        self.crosshair = Text('+', scale=2, position=(0, 0), origin=(0, 0), color=color.yellow)

        self.radar_text = Text(text="RADAR LIGADO", scale=2, origin=(0, 0), position=(0, 0.4),  color=color.orange, enabled=False)
        self.crosshair.ignore = True

        self.radar_lock_text = Text(text="LOCK", scale=2, origin=(0, 0), position=(0, 0.35),  color=color.red, enabled=False)

        # 🎯 Radar State Variables
        self.radar_ligado = False
        self.target_locked = False  
        self.sensibilidade = 100  
        self.smooth_x, self.smooth_y = 0, 0  
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
        """Ativa o radar e exibe o letreiro na tela."""
        self.radar_ligado = True
        self.radar_text.enabled = True  
        self.som_radar.play()  
        self.target_locked = False  
        self.lock_on_timer = None  
        self.lock_on_delay  

        print("Radar ligado - Som ativado")
        invoke(self.check_target_status, delay=0.2)  

    def desligar_radar(self):
        """Desativa o radar e remove o letreiro."""
        self.radar_ligado = False
        self.radar_text.enabled = False  
        self.som_radar.stop()
        self.som_radar_fast.stop()
        self.som_radar_lock.stop()  
        self.lock_on_timer = None  
        self.radar_lock_text.enabled = False  # 🔥 Make sure LOCK text disappears
        print("Radar desligado - Som desativado")

    # 🔥 ======================= TARGET DETECTION ======================= 🔥 #

    def is_target_in_view(self):
        "Verifica se um alvo está na mira e retorna o RCS captado."
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
        "Starts the fast beep and waits 1-3s before locking the target."
        if self.radar_ligado and not self.target_locked:
            self.lock_on_timer = time.time()  
            self.som_radar.stop()
            self.som_radar_fast.play()  
            self.blink_lock_text()  # 🔥 Start blinking "LOCK"
            print(f"🔄 Fast beep active! Lock-on in {self.lock_on_delay:.2f}s")
            
            invoke(self.lock_target, delay=self.lock_on_delay)  

    def blink_lock_text(self):
        "Makes 'LOCK' text blink while fast beep is active."
        if self.radar_ligado and not self.target_locked:
            self.radar_lock_text.enabled = not self.radar_lock_text.enabled  
            invoke(self.blink_lock_text, delay=0.3)  # 🔥 Blinks every 0.3s

    def lock_target(self):
        "Locks the target and switches to lock sound."
        if self.radar_ligado and self.is_target_in_view():
            self.som_radar_fast.stop()  
            self.som_radar_lock.play()  
            self.target_locked = True
            self.radar_lock_text.enabled = True  # 🔥 Stop blinking and keep LOCK visible
            print("🔒 Lock-On Achieved!")

    # 🔥 ======================= TARGET STATUS CHECK ======================= 🔥 #

    def check_target_status(self):
        "Checks the target status and switches sounds accordingly."
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
        "Resets the radar to normal beep when the target is lost."
        self.som_radar_fast.stop()
        self.som_radar_lock.stop()
        self.som_radar.play()  
        self.target_locked = False
        self.radar_lock_text.enabled = False  
        self.lock_on_timer = None  
        print("🔄 Lock lost! Back to normal beep.")

    # 🔥 ======================= INPUT HANDLING ======================= 🔥 #

    def input(self, key):
        "Alterna o radar ao pressionar 'R' apenas uma vez."
        if key == 'r':  
            if not self.radar_ligado:
                self.ligar_radar()
            else:
                self.desligar_radar()

    # 🔥 ======================= CAMERA MOVEMENT ======================= 🔥 #

    def update(self):
        "Controla a rotação da câmera conforme o movimento do mouse, suavizando a transição."
        self.smooth_x = lerp(self.smooth_x, mouse.velocity[0] * self.sensibilidade, time.dt * 10)
        self.smooth_y = lerp(self.smooth_y, mouse.velocity[1] * self.sensibilidade, time.dt * 10)

        camera.rotation_y += self.smooth_x
        camera.rotation_x -= self.smooth_y
        camera.rotation_x = clamp(camera.rotation_x, -45, 45)

        if self.radar_ligado and (time.time() - self.last_lock_check > 0.2):
            self.last_lock_check = time.time()  
