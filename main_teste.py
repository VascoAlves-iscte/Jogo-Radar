from ursina import *
from radar import Radar
from input_controller import InputController
from Level_TestingRange import load_level_testingrange
from Level_Teste import load_level_teste
from Level_Arena import load_level_arena
from Level_Tutorial import load_level_tutorial
from radar_hud import RadarHUD
from ui_manager import UIManager, destroy_entities
from Level_Manager import LevelManager

app = Ursina()
window.fullscreen = True

class GameController(Entity):
    """
    Gestão global do jogo: orquestra a transição entre níveis, a interface (menus e HUD)
    e a pausa/retoma do jogo.
    """
    def __init__(self):
        super().__init__()
        self.level_manager = LevelManager()
        self.ui_manager = UIManager(ui_root=camera.ui)
        self.radar = None
        self.input_controller = None
        self.radar_hud = None
        self.game_running = False

        # Exibe o menu inicial e define os callbacks
        self.ui_manager.create_main_menu(self.start_game, application.quit, load_level_tutorial, load_level_arena)

    def start_game(self, level_loader):
        """Carrega e inicia um nível de jogo."""
        self.stop_game()
        self.level_manager.start_level(level_loader, parent=self)
        # Para obter os alvos, recarregamos o nível (poder-se-ia integrar para evitar chamadas duplicadas)
        terrain, targets, level_update = level_loader()
        self.radar = Radar(position=(0, 0, 0), targets=targets, parent=self.level_manager.game_root)
        self.input_controller = InputController(radar=self.radar, targets=targets, game_controller=self, sensibilidade=100, parent=self.level_manager.game_root)
        self.radar_hud = RadarHUD(radar=self.radar, targets=targets, input_controller=self.input_controller, parent=camera.ui)
        self.game_running = True
        mouse.locked = True
        mouse.visible = False

    def stop_game(self):
        """Descarrega completamente o jogo."""
        self.level_manager.stop_level()
        if self.radar_hud:
            destroy(self.radar_hud)
            self.radar_hud = None
        self.game_running = False

    def create_pause_menu(self):
        """Cria o menu de pausa e para o jogo."""
        self.ui_manager.create_pause_menu(self.resume_game, self.restart_game, lambda: self.ui_manager.create_main_menu(self.start_game, application.quit, load_level_tutorial, load_level_arena))
        self.game_running = False
        mouse.locked = False
        mouse.visible = True

    def resume_game(self):
        """Retoma o jogo, escondendo o menu de pausa."""
        destroy_entities(self.ui_manager.pause_menu_entities)
        self.game_running = True
        mouse.locked = True
        mouse.visible = False

    def restart_game(self):
        """Reinicia o nível atual, desligando o radar se estiver activo e reinicializando toda a interface."""
        destroy_entities(self.ui_manager.pause_menu_entities)
        if self.radar and getattr(self.radar, 'radar_ligado', False):
            self.radar.desligar_radar()
        self.game_running = True
        if self.level_manager.current_level_loader:
            self.start_game(self.level_manager.current_level_loader)

game_controller = GameController()
app.run()
