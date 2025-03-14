from ursina import *

# Entidade para encapsular a função de update do nível.
class Level(Entity):
    def __init__(self, update_func, **kwargs):
        super().__init__(**kwargs)
        self.update_func = update_func
    def update(self):
        self.update_func()

# Classe que gere os níveis do jogo.
class LevelManager(Entity):
    def __init__(self, radar, level_loaders, **kwargs):
        super().__init__(**kwargs)
        self.radar = radar
        self.level_loaders = level_loaders  # Lista de funções para carregar cada nível.
        self.current_level_index = 0
        self.loading = False  # Flag para evitar múltiplas transições.
        self.load_current_level()

    def load_current_level(self):
        print(f"Carregando nível {self.current_level_index}")
        self.floor, self.targets, self.level_update = self.level_loaders[self.current_level_index]()
        # Atualiza a lista de targets no radar.
        self.radar.targets = self.targets
        self.level_entity = Level(update_func=self.level_update)
        self.loading = False  # Finalizou o carregamento do nível atual.

    def update(self):
        # Atualiza a lista de targets a partir do radar, caso ela seja alterada.
        self.targets = self.radar.targets
        print(f"LevelManager update() chamado - {len(self.targets)} targets")
        # Se não estiver em transição e a condição de término for satisfeita...
        if not self.loading and (self.all_targets_destroyed() or self.radar_inativo()):
            self.loading = True  # Impede chamadas repetidas.
            self.load_next_level()

    def all_targets_destroyed(self):
        # Considera como fim de nível se a lista de targets estiver vazia ou todos estiverem desabilitados.
        return len(self.targets) == 0 or all(not target.enabled for target in self.targets)

    def radar_inativo(self):
        # Se o radar já estiver marcado como inativo, retorna True.
        if not getattr(self.radar, 'active', True):
            return True
        for target in self.targets:
            try:
                # Se algum target estiver muito próximo do radar, marca-o como inativo.
                if (target.world_position - self.radar.world_position).length() < 20:  
                    print("Radar inativado por proximidade de alvo!")
                    self.radar.active = False
                    self.radar.enabled = False
                    self.radar.visible = False
                    return True
            except Exception as e:
                print("Erro ao acessar world_position do radar:", e)
                return True
        return False

    def load_next_level(self):
        print("Carregando próximo nível")
        destroy(self.level_entity)
        self.current_level_index += 1
        if self.current_level_index < len(self.level_loaders):
            self.load_current_level()
            # Ao carregar o novo nível, reativa o radar.
            self.radar.active = True
            self.radar.enabled = True
            self.radar.visible = True
        else:
            print("Todos os níveis foram completados!")
