from ursina import *
from radar import Radar
from input_controller import InputController
from radar_hud import RadarHUD
from Level_TestingRange import load_level_testingrange
from Level_Teste import load_level_teste
from Level_Arena import load_level_arena
from Level_Tutorial import load_level_tutorial
from Level_Manager import LevelManager  # Novo import do LevelManager

app = Ursina()

# Para criar o radar, precisamos carregar um nível inicial para obter os targets.
# Aqui, usamos como exemplo o primeiro nível da lista.
initial_floor, initial_targets, initial_level_update = load_level_tutorial()
radar = Radar(position=(0, 0, 0), targets=initial_targets)
input_controller = InputController(radar=radar, targets=initial_targets, sensibilidade=100)
radar_hud = RadarHUD(radar=radar, targets=initial_targets, input_controller=input_controller)
sky = Sky()

# Define a lista de funções que carregam os níveis (a ordem pode ser a que preferir)
levels = [load_level_tutorial, load_level_testingrange, load_level_arena]

# Cria o LevelManager, que vai gerenciar a transição dos níveis
level_manager = LevelManager(radar, levels)

app.run()
