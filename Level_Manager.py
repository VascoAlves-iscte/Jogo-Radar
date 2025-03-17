from ursina import *

class LevelManager:
    """
    Gerir o carregamento e a eliminação dos níveis.
    """
    def __init__(self):
        self.current_level = None
        self.current_level_loader = None
        self.game_root = None

    def start_level(self, level_loader, parent):
        """
        Carrega o nível através do 'level_loader' e define o elemento pai (parent)
        para os elementos do jogo.
        Retorna: (game_root, targets, level_update)
        """
        self.game_root = Entity(name="game_root", parent=parent)
        terrain, targets, level_update = level_loader()
        terrain.parent = self.game_root
        for target in targets:
            target.parent = self.game_root
        self.current_level_loader = level_loader

        # Cria a entidade que executa a função de update do nível.
        level_entity = Entity(parent=self.game_root)
        level_entity.update = level_update
        self.current_level = level_entity

        return self.game_root, targets, level_update

    def stop_level(self):
        """
        Descarrega o nível, destruindo o game_root e reinicializando as variáveis.
        """
        if self.game_root:
            destroy(self.game_root)
            self.game_root = None
            self.current_level = None
            self.current_level_loader = None
