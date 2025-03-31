from ursina import * 
from radar import Radar
from input_controller import InputController
from Level_Arena import load_level_arena
from Level_Tutorial import load_level_tutorial
from radar_hud import RadarHUD
from tutorial_slides import TutorialSlides


app = Ursina()

def destroy_entities(lista_entidades):
    """Função auxiliar para destruir todas as entidades de uma lista."""
    for entidade in lista_entidades:
        destroy(entidade)
    lista_entidades.clear()

class GameController(Entity):
    """
    Gestão global do jogo, incluindo o carregamento dos níveis, a interface (menus e HUD) e
    a pausa/retoma do jogo.
    """
    def __init__(self):
        super().__init__()
        self.current_level = None
        self.radar = None
        self.input_controller = None
        self.radar_hud = None
        self.game_running = False  # Flag que indica se o jogo está a correr
        self.menu_entities = []    # Entidades do menu inicial
        self.pause_menu_entities = []  # Entidades do menu de pausa
        self.current_level_loader = None
        self.game_root = None      # Container para os elementos do jogo
        self.ui_root = Entity(parent=camera.ui, name="ui_root")  # Container para a interface (menus, HUD)
        self.create_main_menu()

    def start_game(self, level_loader):
        """Carrega e inicia um nível de jogo."""
        self.stop_game()  # Garante que nenhum elemento do nível anterior persista
        
        # Cria o container para todos os elementos do jogo.
        self.game_root = Entity(name="game_root")

        # Carrega o nível (chão, alvos e função de update).
        terrain, targets, level_update = level_loader()
        terrain.parent = self.game_root
        for target in targets:
            target.parent = self.game_root

        # Cria o Radar com os alvos e associa-o ao container.
        self.radar = Radar(position=(0, 0, 0), targets=targets, parent=self.game_root)

        # Cria o InputController (passando o GameController) e associa-o ao container.
        self.input_controller = InputController(radar=self.radar, targets=targets, game_controller=self, sensibilidade=100, parent=self.game_root)

        # Cria o RadarHUD e associa-o à interface (ui_root).
        self.radar_hud = RadarHUD(radar=self.radar, targets=targets, input_controller=self.input_controller, parent=self.ui_root)

        # Skybox – adiciona-o ao container do jogo.
        sky = Sky()
        sky.parent = self.game_root

        # Cria uma entidade Level que encapsula a função de update do nível.
        # A classe Level recebe o próprio GameController para consultar a flag game_running.
        class Level(Entity):
            def __init__(self, update_func, game_controller, **kwargs):
                super().__init__(**kwargs)
                self.update_func = update_func
                self.game_controller = game_controller  # Guarda a referência ao GameController

            def update(self):
                if self.game_controller.game_running:
                    self.update_func()

        self.game_running = True
        self.current_level = Level(update_func=level_update, game_controller=self, parent=self.game_root)
        self.current_level_loader = level_loader

        # Trava e esconde o cursor para o jogo.
        mouse.locked = True
        mouse.visible = False
        window.fullscreen = True

    def stop_game(self):
        """Descarrega completamente o jogo, destruindo os containers e a interface."""
        if self.game_root:
            destroy(self.game_root)
            self.game_root = None

        if self.radar_hud:
            destroy(self.radar_hud)
            self.radar_hud = None

        for child in list(camera.ui.children):
            if isinstance(child, TutorialSlides):
                destroy(child)

        destroy_entities(self.menu_entities)
        destroy_entities(self.pause_menu_entities)

        self.current_level = None
        self.radar = None
        self.input_controller = None
        self.game_running = False

    def create_main_menu(self):
        
        """Cria o menu inicial com fundo customizado e botões."""
        self.stop_game()

        # Carrega a imagem de fundo
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

        # Cria os botões do menu inicial.

        # Cria os botões do menu inicial.
        tutorial_button = Button(
            text='Tutorial',
            text_color=color.black,
            color=color.rgb32(255,248,233),
            scale=(0.3, 0.1),
            position=(0.5, -0.05),
            parent=self.ui_root,
            origin=(0, 0),
            text_origin=(0, 0),
            text_size=1.5,
            collider='box',
            highlight_scale=1.1,
            pressed_scale=0.9,
            highlight_sound='assets/hover button.mp3',   # Ficheiro de som para o efeito de highlight
            pressed_sound='assets/button sound.mp3',         # Ficheiro de som para o efeito de pressionar
            highlight_color=color.rgb32(255,248,233)
        )
        arena_button = Button(
            text='Arena',
            text_color=color.black,
            color=color.rgb32(255,248,233),
            scale=(0.3, 0.1),
            position=(0.5, -0.2),
            parent=self.ui_root,
            origin=(0, 0),
            text_origin=(0, 0),
            text_size=1.5,
            collider='box',
            highlight_scale=1.1,
            pressed_scale=0.9,
            highlight_sound='assets/hover button.mp3',   # Ficheiro de som para o efeito de highlight
            pressed_sound='assets/button sound.mp3',         # Ficheiro de som para o efeito de pressionar
            highlight_color=color.rgb32(255,248,233)
        )
        quit_button = Button(
            text='Exit',
            text_color=color.black,
            color=color.rgb32(255,248,233),
            scale=(0.3, 0.1),
            position=(0.5, -0.35),
            parent=self.ui_root,
            text_size=1.5,
            collider='box',
            highlight_scale=1.1,
            pressed_scale=0.9,
            highlight_sound='assets/hover button.mp3',   # Ficheiro de som para o efeito de highlight
            pressed_sound='assets/button sound.mp3',         # Ficheiro de som para o efeito de pressionar
            highlight_color=color.rgb32(255,248,233)
        )

        tutorial_button.on_click = lambda: self.start_game(load_level_tutorial)
        arena_button.on_click = lambda: self.start_game(load_level_arena)
        quit_button.on_click = lambda: application.quit()

        self.menu_entities.extend([tutorial_button, arena_button, quit_button])

        # Liberta o cursor para interação no menu.
        mouse.locked = False
        mouse.visible = True
        window.fullscreen = True



    def create_pause_menu(self):
        """Cria o menu de pausa e para o jogo."""
        destroy_entities(self.pause_menu_entities)

        # Carrega aimagem de fundo
        background_texture = load_texture("assets/Radar Na Colina 2.png")
        image_width, image_height = 1920, 1080
        aspect_ratio = image_width / image_height
        background_height = 1
        background_width = background_height * aspect_ratio

        # Cria o fundo do menu de pausa, definindo um valor de z menor para que fique por cima.
        background = Entity(
            model='quad',
            scale=(background_width, background_height),
            texture=background_texture,
            parent=self.ui_root,
            position=(0, 0),
            z=-1
        )
        self.pause_menu_entities.append(background)

        # Cria os botões do menu de pausa.
        resume_button = Button(
            text='Resumir',
            pressed_sound='assets/som pausa.mp3',
            highlight_sound='assets/hover pausa.mp3',
            scale=(0.3, 0.1), position=(0, 0.2), 
            parent=self.ui_root, 
            z=-2)
        
        restart_button = Button(
            text='Reiniciar',
            pressed_sound='assets/som pausa.mp3',
            highlight_sound='assets/hover pausa.mp3', 
            scale=(0.3, 0.1), position=(0, 0), 
            parent=self.ui_root, 
            z=-2)
        
        main_menu_button = Button(
            text='Menu Inicial',
            pressed_sound='assets/som pausa.mp3',
            highlight_sound='assets/hover pausa.mp3',   
            scale=(0.3, 0.1), 
            position=(0, -0.2), 
            parent=self.ui_root, 
            z=-2)

        resume_button.on_click = self.resume_game
        restart_button.on_click = self.restart_game
        main_menu_button.on_click = self.create_main_menu

        self.pause_menu_entities.extend([resume_button, restart_button, main_menu_button])
        self.game_running = False  # Pausa o jogo

        # Liberta o cursor para o menu de pausa.
        mouse.locked = False
        mouse.visible = True
        

    def resume_game(self):
        """Retoma o jogo, escondendo o menu de pausa."""
        destroy_entities(self.pause_menu_entities)
        self.game_running = True
        mouse.locked = True
        mouse.visible = False

    def restart_game(self):
        """Reinicia o nível atual, desligando o radar se estiver activo e reinicializando toda a interface."""
        destroy_entities(self.pause_menu_entities)

        if self.radar and self.radar.radar_ligado:
            self.radar.desligar_radar()

        mouse.locked = True
        mouse.visible = False
        self.game_running = True

        if self.current_level_loader:
            self.start_game(self.current_level_loader)

# Cria a instância do GameController.
game_controller = GameController()

app.run()
