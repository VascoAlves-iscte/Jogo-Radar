from ursina import *
import math
from ursina import Vec2, Vec4, camera, application
from panda3d.core import Point3

class RadarHUD(Entity):
    def __init__(self, radar, targets, **kwargs):
        super().__init__(parent=camera.ui, **kwargs)
        self.radar = radar
        self.targets = targets

        # --- Minimapa ---
        # Borda do minimapa (um círculo preto um pouco maior que o fundo)
        self.minimap_border = Entity(
            parent=self,
            model='circle',
            color=color.black,
            scale=0.31,
            position=(0.7, -0.33)
        )
        # Fundo do minimapa: um círculo com um tom de verde escuro
        verde_escuro = Vec4(0, 0.5, 0, 1)
        self.minimap = Entity(
            parent=self,
            model='circle',
            color=verde_escuro,
            scale=0.3,
            position=(0.7, -0.33)
        )
        # Define o "raio" interno do minimapa (em unidades de UI)
        self.minimap_radius = 0.5

        # --- Indicador da direção do radar no minimapa ---
        # Carrega o modelo do cone
        cone = load_model('cone.obj')
        # Define uma cor verde com transparência (valor alfa de 0.5)
        verde_transparente = Vec4(0.2, 0.8, 0.2, 0.5)
        # Inicializa thickness com base no FOV atual (referência de 60°)
        self.thickness = 0.001 * (camera.fov / 60.0)
        # Cria um container centralizado no minimapa para o indicador de direção
        self.radar_direction_container = Entity(parent=self.minimap, position=(0, 0))
        self.radar_direction_indicator = Entity(
            parent=self.radar_direction_container,
            model=cone,
            color=verde_transparente,
            scale=(self.thickness, -self.minimap_radius * 0.5, 0.1),
            position=(0, 0)
        )

        # Cria um indicador para cada target no minimapa
        self.minimap_indicators = {}
        for target in targets:
            indicator = Entity(
                parent=self.minimap,
                model='circle',
                color=color.red,
                scale=0.03
            )
            self.minimap_indicators[target] = indicator

        # --- Painel FOV (Visão Vertical do FOV) ---
        # Cria uma borda preta para o painel FOV
        self.fov_border = Entity(
            parent=self,
            model='quad',
            color=color.black,
            scale=(0.31, 0.31),
            position=(-0.70, -0.30)
        )
        # Fundo do painel FOV: um quad semi-transparente com tom de verde
        self.fov_view = Entity(
            parent=self,
            model='quad',
            color=verde_transparente,
            scale=(0.3, 0.3),
            position=(-0.70, -0.30)
        )
        # Opcional: linhas de mira horizontais e verticais no painel FOV
        self.fov_line_horizontal = Entity(
            parent=self,
            model='quad',
            color=color.black33,
            scale=(0.05, 0.005),
            position=(-0.70, -0.30)
        )
        self.fov_line_vertical = Entity(
            parent=self,
            model='quad',
            color=color.black33,
            scale=(0.005, 0.05),
            position=(-0.70, -0.30)
        )
        # Cria um indicador para cada target na visão FOV
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
            if not target or not target.enabled:
                indicator.enabled = False
                del self.minimap_indicators[target]
                continue
            rel = target.world_position - self.radar.world_position
            x, y = rel.x, rel.z  # X e Z para a vista "de cima"
            dist = math.sqrt(x * x + y * y)
            if dist > 500:
                factor = 500 / dist
                x *= factor
                y *= factor
            ui_x = (x / 500) * self.minimap_radius
            ui_y = (y / 500) * self.minimap_radius
            indicator.position = (ui_x, ui_y)

        # Atualiza a thickness de acordo com o zoom
        base_fov = 60.0
        self.thickness = 0.3 * (camera.fov / base_fov)
        self.radar_direction_indicator.scale = (self.thickness, -self.minimap_radius * 0.5, 0.1)

        # --- Atualiza o indicador de direção do radar (minimapa) ---
        forward = camera.forward
        fwd = Vec2(forward.x, forward.z)
        if fwd.length() > 0:
            angle = math.degrees(math.atan2(fwd.x, fwd.y))
            self.radar_direction_indicator.rotation_z = angle

        # --- Atualiza o Painel FOV (apenas targets dentro do FOV atual da câmera) ---
        for target, indicator in list(self.fov_indicators.items()):
            if not target or not target.enabled:
                indicator.enabled = False
                del self.fov_indicators[target]
                continue

            # Calcula o vetor do target em relação ao radar
            rel = target.world_position - self.radar.world_position
            # Calcula o ângulo do target em relação ao eixo Z (frente do radar)
            angle = math.degrees(math.atan2(rel.x, rel.z))
            # Normaliza a diferença entre o ângulo do target e a rotação horizontal da câmera para o intervalo [-180, 180]
            relative_angle = (angle - camera.rotation_y + 180) % 360 - 180
            # Define o FOV atual com base no zoom (por exemplo, ±(camera.fov/2))
            half_fov = camera.fov / 2.0
            if abs(relative_angle) > half_fov:
                indicator.enabled = False
                continue
            else:
                indicator.enabled = True

            # Mapeia o ângulo relativo (de -half_fov a half_fov) para uma coordenada horizontal normalizada de 0 a 1
            ui_x = (relative_angle + half_fov) / (2 * half_fov)

            # Para a coordenada vertical, usa a projeção da posição (ou um fallback baseado na altitude)
            screen_pos = self.world_to_screen_point(target.world_position)
            if screen_pos.x == -100 and screen_pos.y == -100:
                vertical_range = 100.0  # ajuste conforme necessário
                dy = target.world_position.y - self.radar.world_position.y
                ui_y = 0.5 + (dy / vertical_range)
            else:
                ui_y = screen_pos.y

            indicator.position = (ui_x - 0.5, ui_y - 0.5)
