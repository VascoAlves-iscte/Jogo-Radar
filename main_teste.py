from ursina import * 
from radar import Radar
from input_controller import InputController
from Level_TestingRange import load_level_testingrange
from Level_Teste import load_level_teste
from Level_Arena import load_level_arena
from Level_Tutorial import load_level_tutorial
from radar_hud import RadarHUD

app = Ursina()

def destroy_entities(entity_list):
    """Helper function to destroy all entities in a list."""
    for entity in entity_list:
        destroy(entity)
    entity_list.clear()

class GameController(Entity):
    """
    GameController manages the overall game state, including level loading,
    UI management, and transitions between menus and gameplay.
    """
    def __init__(self):
        super().__init__()
        self.current_level = None
        self.radar = None
        self.input_controller = None
        self.radar_hud = None
        self.game_running = False  # Flag indicating if the game is running
        self.menu_entities = []    # Entities for the main menu
        self.pause_menu_entities = []  # Entities for the pause menu
        self.current_level_loader = None
        self.game_root = None      # Container for all game elements
        # Create a container for UI elements (menus, HUD, etc.)
        self.ui_root = Entity(parent=camera.ui, name="ui_root")
        self.create_main_menu()

    def start_game(self, level_loader):
        """
        Loads and starts a game level provided by level_loader.
        """
        self.stop_game()

        # Create container for all game elements.
        self.game_root = Entity(name="game_root")

        # Load level: terrain, targets, and level_update function.
        terrain, targets, level_update = level_loader()
        terrain.parent = self.game_root
        for target in targets:
            target.parent = self.game_root

        # Create Radar with targets.
        self.radar = Radar(position=(0, 0, 0), targets=targets, parent=self.game_root)

        # Create InputController (passing self as game_controller).
        self.input_controller = InputController(radar=self.radar, targets=targets, game_controller=self, sensibilidade=100, parent=self.game_root)

        # Create RadarHUD and attach it to the UI container.
        self.radar_hud = RadarHUD(radar=self.radar, targets=targets, input_controller=self.input_controller, parent=self.ui_root)

        # Skybox as part of the game elements.
        sky = Sky()
        sky.parent = self.game_root

        # Create a Level entity to encapsulate the level's update function.
        class Level(Entity):
            def __init__(self, update_func, game_running_flag, **kwargs):
                super().__init__(**kwargs)
                self.update_func = update_func
                self.game_running_flag = game_running_flag

            def update(self):
                if self.game_running_flag:
                    self.update_func()

        self.game_running = True
        self.current_level = Level(update_func=level_update, game_running_flag=self.game_running, parent=self.game_root)
        self.current_level_loader = level_loader

        # Lock and hide the mouse for gameplay.
        mouse.locked = True
        mouse.visible = False

    def stop_game(self):
        """
        Stops the current game level, destroying all game and UI elements.
        """
        if self.game_root:
            destroy(self.game_root)
            self.game_root = None

        if self.radar_hud:
            destroy(self.radar_hud)
            self.radar_hud = None

        destroy_entities(self.menu_entities)
        destroy_entities(self.pause_menu_entities)

        self.current_level = None
        self.radar = None
        self.input_controller = None
        self.game_running = False

    def create_main_menu(self):
        """
        Creates the main menu UI.
        """
        self.stop_game()

        # Load custom background texture.
        background_texture = load_texture("assets/Radar Na Colina.png")
        image_width, image_height = 1920, 1080
        aspect_ratio = image_width / image_height
        background_height = 1
        background_width = background_height * aspect_ratio

        background = Entity(
            model='quad',
            scale=(background_width, background_height),
            texture=background_texture,
            parent=self.ui_root,
            position=(0, 0)
        )
        self.menu_entities.append(background)

        # Create menu buttons.
        tutorial_button = Button(text='Tutorial', color=color.blue, scale=(0.3, 0.1), position=(-0.5, -0.2), parent=self.ui_root)
        arena_button = Button(text='Arena', color=color.red, scale=(0.3, 0.1), position=(0, -0.2), parent=self.ui_root)
        quit_button = Button(text='Quit', color=color.green, scale=(0.3, 0.1), position=(0.5, -0.2), parent=self.ui_root)

        tutorial_button.on_click = lambda: self.start_game(load_level_tutorial)
        arena_button.on_click = lambda: self.start_game(load_level_arena)
        quit_button.on_click = lambda: application.quit()

        self.menu_entities.extend([tutorial_button, arena_button, quit_button])

        # Release mouse for menu interaction.
        mouse.locked = False
        mouse.visible = True

    def create_pause_menu(self):
        """
        Creates the pause menu.
        """
        destroy_entities(self.pause_menu_entities)

        # Cria o fundo do menu com z=-1 para que fique sobre a UI existente.
        background = Entity(
            parent=self.ui_root,
            model='quad',
            scale=(1.8, 1),
            color=color.rgba(0, 0, 0, 180),
            position=(0, 0),
            z=-1  # Valor menor garante que fique na frente.
        )
        self.pause_menu_entities.append(background)

        # Cria os botões do menu de pausa com z=-1 também.
        resume_button = Button(text='Resumir', scale=(0.3, 0.1), position=(0, 0.2), parent=self.ui_root, z=-1)
        restart_button = Button(text='Reiniciar', scale=(0.3, 0.1), position=(0, 0), parent=self.ui_root, z=-1)
        main_menu_button = Button(text='Menu Inicial', scale=(0.3, 0.1), position=(0, -0.2), parent=self.ui_root, z=-1)

        resume_button.on_click = self.resume_game
        restart_button.on_click = self.restart_game
        main_menu_button.on_click = self.create_main_menu

        self.pause_menu_entities.extend([resume_button, restart_button, main_menu_button])
        self.game_running = False

        # Liberta o cursor para interação no menu de pausa.
        mouse.locked = False
        mouse.visible = True


    def resume_game(self):
        """
        Resumes the game from pause.
        """
        destroy_entities(self.pause_menu_entities)
        self.game_running = True
        mouse.locked = True
        mouse.visible = False

    def restart_game(self):
        """
        Restarts the current level, ensuring the radar is turned off and UI elements are reset.
        """
        destroy_entities(self.pause_menu_entities)

        if self.radar and self.radar.radar_ligado:
            self.radar.desligar_radar()

        mouse.locked = True
        mouse.visible = False
        self.game_running = True

        if self.current_level_loader:
            self.start_game(self.current_level_loader)

# Create GameController instance.
game_controller = GameController()

app.run()
