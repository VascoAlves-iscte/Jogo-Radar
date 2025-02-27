from ursina import *
import math
from ursina import Vec2,Vec4, camera, application
from panda3d.core import Point3

class RadarHUD(Entity):
    def __init__(self, radar,targets, **kwargs):
        super().__init__(parent=camera.ui, **kwargs)
        self.radar = radar
        self.targets = targets

        verde_escuro= Vec4(0, 0.5, 0, 1)
        # --- Minimapa Circular no lado direito ---
        # Fundo do minimapa: posicionado à direita, com tamanho ajustável.
        self.minimap = Entity(
            parent=self,
            model='circle',      # ou use um quad com textura circular
            color=verde_escuro,
            scale=0.3,           # ajuste conforme necessário
            position=(0.7, -0.33)
        )
        # Definindo o "raio" interno do minimapa (em unidades de UI)
        self.minimap_radius = 0.15

        lens = application.base.cam.node().getLens()

        # Cria um indicador para cada target no minimapa.
        self.minimap_indicators = {}
        for target in targets:
            indicator = Entity(
                parent=self.minimap,
                model='circle',
                color=color.red,
                scale=0.03
            )
            self.minimap_indicators[target] = indicator

        # --- Indicador da direção do radar no minimapa ---.
        cone = load_model('cone.obj')
        verde_transparente= Vec4(0.2, 0.8, 0.2, 0.5)
        # Cria um container centralizado no minimapa para o indicador de direção.
        self.radar_direction_container = Entity(parent=self.minimap, position=(0,0))
        self.radar_direction_indicator = Entity(
            parent=self.radar_direction_container,
            model=cone,
            color=verde_transparente,
            scale=(0.05, -self.minimap_radius, 0.05),
            position=(0, 0)
        )


        # --- Visão Vertical do FOV no lado esquerdo ---
        # Fundo do painel FOV: posicionado à esquerda
        self.fov_view = Entity(
            parent=self,
            model='quad',
            color=color.black33,  # semi-transparente para efeito de HUD
            scale=(0.3, 0.3),
            position=(-0.70, -0.30)
        )
        # Cria um indicador para cada target na visão FOV.
        self.fov_indicators = {}
        for target in targets:
            indicator = Entity(
                parent=self.fov_view,
                model='circle',
                color=color.red,
                scale=0.03
            )
            self.fov_indicators[target] = indicator

    

    def world_to_screen_point(self, world_position):
        p3 = Point3(world_position.x, world_position.y, world_position.z)
        p2 = Point3()
        lens = application.base.cam.node().getLens()  
        if lens.project(p3, p2):
            screen_x = (p2.x + 1) / 2
            screen_y = (p2.y + 1) / 2
            return Vec2(screen_x, screen_y)
        else:
            return Vec2(-100, -100)

    def update(self):
        # --- Atualiza o Minimapa ---
        for target, indicator in list(self.minimap_indicators.items()):
            # Verifica se o target ainda existe e está habilitado.
            if not target or not target.enabled:
                indicator.enabled = False  # ou destroy(indicator)
                del self.minimap_indicators[target]
                continue

            # Calcula a posição relativa (apenas X e Z) entre o target e o radar.
            rel = target.world_position - self.radar.world_position
            x, y = rel.x, rel.z  # Y do minimapa corresponde a Z do mundo.
            # Calcula a distância e, se necessário, faz clamp para 500 metros.
            dist = math.sqrt(x*x + y*y)
            if dist > 500:
                factor = 500 / dist
                x *= factor
                y *= factor
            # Mapeia 500 m para o raio definido no minimapa.
            ui_x = (x / 500) * self.minimap_radius
            ui_y = (y / 500) * self.minimap_radius
            indicator.position = (ui_x, ui_y)

        # --- Atualiza a Visão Vertical do FOV ---
        for target, indicator in list(self.fov_indicators.items()):
            if not target or not target.enabled:
                indicator.enabled = False
                del self.fov_indicators[target]
                continue

            screen_pos = self.world_to_screen_point(target.world_position)
            # Converter para coordenadas locais do painel, se necessário:
            local_x = screen_pos.x - 0.5
            local_y = screen_pos.y - 0.5
            indicator.position = (local_x, local_y)
        
        # --- Atualiza o indicador de direção do radar ---
        forward = camera.forward  # vetor 3D que representa a direção da câmera
        fwd = Vec2(forward.x, forward.z)
        if fwd.length() > 0:
            angle = math.degrees(math.atan2(fwd.x, fwd.y))
            self.radar_direction_indicator.rotation_z = angle

