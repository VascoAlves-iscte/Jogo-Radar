from ursina import *
import time  # Needed for performance fixes

class Radar(Entity):
    """
    Classe que representa o radar fixo no mapa.
    A câmera rotaciona conforme o movimento do mouse sem limite e de forma suave.
    """

    def __init__(self, position=(20, 1, -20), targets=None, **kwargs):
        super().__init__(position=position, **kwargs)

        # 🎯 Camera Configuration
        camera.parent = self
        camera.position = (0, 2, 0)  # Ajusta a altura da câmera para a visão do radar

        # 🎯 UI Elements
        self.crosshair = Text('+', scale=2, position=(0, 0), origin=(0, 0), color=color.yellow)
        self.radar_text = Text(
            text="RADAR LIGADO", scale=2, origin=(0, 0),
            position=(0, 0.4), color=color.red, enabled=False
        )

        # 🎯 Radar State Variables
        self.radar_ligado = False
        self.target_locked = False  # Keeps track if radar is locked onto a target
        self.sensibilidade = 100  # Sensibilidade do mouse
        self.smooth_x, self.smooth_y = 0, 0  # Variáveis para suavização do movimento
        self.last_lock_check = time.time()  # ✅ FIXED: Properly initialize the last lock check

        # 🎯 Sound Configuration
        self.som_radar = Audio('radar_beep.mp3', autoplay=False, loop=True)
        self.som_radar_lock = Audio('radar_lock.mp3', autoplay=False, loop=True)
        self.som_duracao = 0.5  # Frequência do beep

        # 🎯 Mouse & Window Configuration
        mouse.visible = False  # 🔥 Hide cursor
        mouse.locked = True  # 🔥 Lock mouse to window
        window.exit_button.enabled = False  # 🔥 Prevent accidental window closing
        window.fullscreen = False  # 🔥 Keep focus on the game
        window.focused = True  # 🔥 Ensure keyboard inputs always work

        # 🎯 Lista de Targets
        self.targets = targets if targets else []

    # 🔥 ======================= PREVENT MOUSE ESCAPE & FORCE INPUT ======================= 🔥 #

    def check_mouse_bounds(self):
        """Prevents the mouse from leaving the game window & ensures input works."""
        if not mouse.locked:
            mouse.locked = True  # 🔥 Ensures the mouse stays locked inside
        if not window.focused:
            window.focused = True  # 🔥 Ensure window stays active
            held_keys.clear()  # 🔥 Fixes keyboard input not working

    # 🔥 ======================= RADAR CONTROLS ======================= 🔥 #

    def ligar_radar(self):
        """Ativa o radar e exibe o letreiro na tela."""
        self.radar_ligado = True
        self.radar_text.enabled = True  # ✅ Show "Radar Ligado"
        self.som_radar.play()  # ✅ Start normal beep immediately
        self.target_locked = False  # ✅ Reset lock state
        print("Radar ligado - Som ativado")
        invoke(self.sincronizar_som, delay=self.som_duracao)  # ✅ Ensures sound switching starts

    def desligar_radar(self):
        """Desativa o radar e remove o letreiro."""
        self.radar_ligado = False
        self.radar_text.enabled = False  # ✅ Hide "Radar Ligado"
        self.som_radar.stop()
        self.som_radar_lock.stop()  # ✅ Stop lock sound if playing
        print("Radar desligado - Som desativado")

    def sincronizar_som(self):
        """Muda o som do radar se estiver travado em um alvo."""
        if not self.radar_ligado:
            return  # 🔥 Exit early if radar is off

        locked = self.is_target_locked()  # ✅ Call raycast less frequently

        if locked and not self.target_locked:
            self.som_radar.stop()  # ✅ Stop normal beep
            self.som_radar_lock.play()  # ✅ Play lock sound
            self.target_locked = True
            print("🔒 Lock-on! Radar travado em um alvo.")

        elif not locked and self.target_locked:
            self.som_radar_lock.stop()  # ✅ Stop lock sound
            self.som_radar.play()  # ✅ Resume normal radar beep
            self.target_locked = False
            print("🔄 Lock perdido! Voltando ao beep normal.")

        # 🔥 Instead of calling every frame, reduce frequency to 0.2s
        invoke(self.sincronizar_som, delay=0.2)

    # 🔥 ======================= TARGET LOCK DETECTION ======================= 🔥 #

    def is_target_locked(self):
        """Usa raycasting para detectar se há um alvo na mira."""
        max_distance = 50  # 🔥 Distância máxima do lock-on

        hit_info = raycast(
            origin=camera.world_position, 
            direction=camera.forward,  
            distance=max_distance, 
            ignore=[camera],  
            debug=True  # 🔍 Debug mode (will draw a ray so you can see it!)
        )

        if hit_info.hit and hit_info.entity in self.targets:
            print(f"🎯 Target locked: {hit_info.entity} at {hit_info.distance:.2f} units")
            return True  # ✅ Target is locked

        return False  # ❌ No target detected

    # 🔥 ======================= INPUT HANDLING ======================= 🔥 #

    def input(self, key):
        """Alterna o radar ao pressionar 'R' apenas uma vez."""
        print(f"🔘 Key Pressed: {key}")  # ✅ Debugging Key Presses

        if key == 'r':  
            if not self.radar_ligado:
                self.ligar_radar()
            else:
                self.desligar_radar()

    # 🔥 ======================= CAMERA MOVEMENT ======================= 🔥 #

    def update(self):
        """Controla a rotação da câmera conforme o movimento do mouse, suavizando a transição."""
        self.check_mouse_bounds()  # ✅ Prevents mouse escape & ensures input works

        self.smooth_x = lerp(self.smooth_x, mouse.velocity[0] * self.sensibilidade, time.dt * 10)
        self.smooth_y = lerp(self.smooth_y, mouse.velocity[1] * self.sensibilidade, time.dt * 10)

        camera.rotation_y += self.smooth_x
        camera.rotation_x -= self.smooth_y
        camera.rotation_x = clamp(camera.rotation_x, -45, 45)

        # 🔥 Reduce raycasting calls for performance
        if self.radar_ligado and (time.time() - self.last_lock_check > 0.2):
            self.last_lock_check = time.time()  # ✅ Only update every 0.2s
            self.sincronizar_som()
