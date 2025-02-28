from ursina import *
from radar import Radar
from input_controller import InputController
from Level_TestingRange import load_level_testingrange
from Level_Teste import load_level_teste
from Level_Arena import load_level_arena
from radar_hud import RadarHUD

app = Ursina()      

# Carrega o nível: floor, targets e função de update
terrain, targets, level_update = load_level_arena()

# Cria o Radar com os targets
radar = Radar(position=(0, 0, 0), targets=targets)

# Instancia a HUD do radar
radar_hud = RadarHUD(radar=radar, targets=targets)

# Skybox
sky = Sky()

# Instancia o CameraController, passando a instância do Radar
input_controller= InputController(radar=radar,targets=targets, sensibilidade=100)

# Cria uma entidade Level para encapsular a função de update do nível
class Level(Entity):
    def __init__(self, update_func, **kwargs):
        super().__init__(**kwargs)
        self.update_func = update_func
    def update(self):
        self.update_func()


level_entity = Level(update_func=level_update)

app.run()
