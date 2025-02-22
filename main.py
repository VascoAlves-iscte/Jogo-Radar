from ursina import *
from radar import Radar
from camera_controller import CameraController  # Nosso módulo de câmera
from Level_Teste import load_level_teste
from Level_TestingRange import load_level_testingrange
import random

app = Ursina()

# Skybox
sky = Sky()

# Instancia o controlador de câmera (movimento e zoom ficam centralizados nele)
camera_controller = CameraController(sensibilidade=100)

# Carrega o nível: terreno, targets e função de update do nível
terrain, targets, level_update = load_level_testingrange()

# Criamos uma entidade Level que encapsula o update do nível
class Level(Entity):
    def __init__(self, update_func, **kwargs):
        super().__init__(**kwargs)
        self.update_func = update_func
    def update(self):
        self.update_func()

# Instancia a entidade Level para garantir que o level_update seja chamado a cada frame.
level_entity = Level(update_func=level_update)

# Cria o Radar e passa os targets; posiciona-o para visualizar a cena (por exemplo, (0,10,0))
radar = Radar(position=(0, 0, 0), targets=targets)

app.run()
