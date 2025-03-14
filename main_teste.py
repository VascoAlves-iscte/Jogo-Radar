from ursina import *
from radar import Radar
from input_controller import InputController
from Level_TestingRange import load_level_testingrange
from Level_Teste import load_level_teste
from Level_Arena import load_level_arena
from Level_Tutorial import load_level_tutorial
from radar_hud import RadarHUD

# Configure the window size and aspect ratio (16:9)
#window.size = (1920, 1080)  # Set the window size to 1280x720 (16:9 aspect ratio)
#window.position = (0, 0)  # Center the window on the screen

app = Ursina()

# GameController class to manage game state and scene transitions
class GameController(Entity):
    def __init__(self):
        super().__init__()
        self.current_level = None
        self.radar = None
        self.input_controller = None
        self.radar_hud = None
        self.game_running = False  # Flag to track if the game is running
        self.menu_entities = []  # List to store menu entities
        self.create_main_menu()

    def start_game(self, level_loader):
        # Clear the current scene
        self.stop_game()

        # Load the selected level
        terrain, targets, level_update = level_loader()

        # Create the Radar with the targets
        self.radar = Radar(position=(0, 0, 0), targets=targets)

        # Instantiate the InputController, passing the Radar instance
        self.input_controller = InputController(radar=self.radar, targets=targets, sensibilidade=100)

        # Instantiate the Radar HUD
        self.radar_hud = RadarHUD(radar=self.radar, targets=targets, input_controller=self.input_controller)

        # Skybox
        sky = Sky()

        # Create a Level entity to encapsulate the level update function
        class Level(Entity):
            def __init__(self, update_func, game_running_flag, **kwargs):
                super().__init__(**kwargs)
                self.update_func = update_func
                self.game_running_flag = game_running_flag  # Reference to the game_running flag

            def update(self):
                if self.game_running_flag:  # Only update if the game is running
                    self.update_func()

        # Set the game state to running before creating the Level
        self.game_running = True

        # Create and add the Level to the scene
        self.current_level = Level(update_func=level_update, game_running_flag=self.game_running)

    def stop_game(self):
        # Stop all game-related entities and reset the game state
        if self.current_level:
            destroy(self.current_level)
        if self.radar:
            destroy(self.radar)
        if self.input_controller:
            destroy(self.input_controller)
        if self.radar_hud:
            destroy(self.radar_hud)

        # Destroy all menu entities
        for entity in self.menu_entities:
            destroy(entity)
        self.menu_entities.clear()

        self.current_level = None
        self.radar = None
        self.input_controller = None
        self.radar_hud = None
        self.game_running = False  # Set the game state to stopped

    def create_main_menu(self):
        # Clear the current scene
        self.stop_game()

        # Load the custom background image
        background_texture = load_texture("assets/Radar Na Colina.png")

        # Calculate the aspect ratio of the image (1920x1080)
        image_width = 1920
        image_height = 1080
        aspect_ratio = image_width / image_height

        # Define the height of the background (adjust as needed)
        background_height = 1
        background_width = background_height * aspect_ratio

        # Create the main menu background using the custom texture
        background = Entity(
            model='quad', 
            scale=(background_width, background_height),  # Maintain aspect ratio
            texture=background_texture,  # Use the loaded texture
            parent=camera.ui,  # Ensure it's rendered in the UI layer
            position=(0, 0)  # Center the background
        )
        self.menu_entities.append(background)

        # Create the buttons
        tutorial_button = Button(text='Tutorial', color=color.blue, scale=(0.3, 0.1), position=(-0.5, -0.2))
        arena_button = Button(text='Arena', color=color.red, scale=(0.3, 0.1), position=(0, -0.2))
        quit_button = Button(text='Quit', color=color.green, scale=(0.3, 0.1), position=(0.5, -0.2))

        # Assign actions to the buttons
        tutorial_button.on_click = lambda: self.start_game(load_level_tutorial)
        arena_button.on_click = lambda: self.start_game(load_level_arena)
        quit_button.on_click = lambda: application.quit()

        # Add buttons to the menu entities list
        self.menu_entities.extend([tutorial_button, arena_button, quit_button])

# Create the GameController instance
game_controller = GameController()

# Run the app
app.run()