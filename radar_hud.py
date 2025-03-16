from ursina import *
import math
from panda3d.core import Point3
import time

class RadarHUD(Entity):
    """
    Gerir o HUD do radar, incluindo o contador de mísseis, a barra de recarga,
    o minimapa e os indicadores do painel FOV.
    """
    def __init__(self, radar, targets, input_controller, **kwargs):
        # Permite definir o elemento pai; se não for especificado, utiliza camera.ui
        parent_entity = kwargs.pop('parent', camera.ui)
        super().__init__(parent=parent_entity, **kwargs)
        self.radar = radar
        self.targets = targets
        self.input_controller = input_controller  
        self._update_timer = 0  # Temporizador para limitar a frequência de atualizações pesadas

        # Contador de mísseis (filho deste HUD).
        self.missile_text = Text(
            text="Mísseis: 4/4",
            scale=2,
            position=(0, -0.45),
            origin=(0, 0),
            color=color.black,
            parent=self
        )

        # Elementos da barra de recarga.
        self.reload_background = Entity(
            model='quad',
            parent=self,
            color=color.dark_gray,
            position=(window.bottom),
            scale=(0.5, 0.05)
        )
        self.reload_bar = Entity(
            model='quad',
            parent=self,
            color=color.orange,
            position=(-0.25, -0.5),
            origin=(-0.5, 0),
            scale=(0, 0.05)
        )
        
        # Elementos do minimapa.
        self.minimap_border = Entity(
            parent=self,
            model='circle',
            color=color.black,
            scale=0.31,
            position=(0.7, -0.33)
        )
        verde_escuro = Vec4(0, 0.5, 0, 1)
        self.minimap = Entity(
            parent=self,
            model='circle',
            color=verde_escuro,
            scale=0.3,
            position=(0.7, -0.33)
        )
        self.minimap_radius = 0.5

        # Indicador de direção do radar no minimapa.
        cone = load_model('cone.obj')
        verde_transparente = Vec4(0.2, 0.8, 0.2, 0.5)
        self.thickness = 0.001 * (camera.fov / 60.0)
        self.radar_direction_container = Entity(parent=self.minimap, position=(0, 0))
        self.radar_direction_indicator = Entity(
            parent=self.radar_direction_container,
            model=cone,
            color=verde_transparente,
            scale=(self.thickness, -self.minimap_radius * 0.5, 0.1),
            position=(0, 0)
        )

        # Indicadores para cada alvo no minimapa.
        self.minimap_indicators = {}
        for target in targets:
            indicator = Entity(
                parent=self.minimap,
                model='circle',
                color=color.red,
                scale=0.03
            )
            self.minimap_indicators[target] = indicator

        # Elementos do painel FOV.
        self.fov_border = Entity(
            parent=self,
            model='quad',
            color=color.black,
            scale=(0.31, 0.31),
            position=(-0.70, -0.30)
        )
        self.fov_view = Entity(
            parent=self,
            model='quad',
            color=Vec4(0.2, 0.8, 0.2, 0.5),
            scale=(0.3, 0.3),
            position=(-0.70, -0.30)
        )
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
        """Converte uma posição no mundo para coordenadas de ecrã."""
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
        # Atualiza o contador de mísseis e a barra de recarga a cada ciclo.
        available = self.input_controller.missile_capacity - self.input_controller.missile_count
        self.missile_text.text = f"Mísseis: {available}/{self.input_controller.missile_capacity}"
        if self.input_controller.reloading and self.input_controller.reload_start_time:
            elapsed = time.time() - self.input_controller.reload_start_time
            progress = min(elapsed / self.input_controller.reload_delay, 1)
            self.reload_bar.scale_x = progress * self.reload_background.scale_x
        else:
            self.reload_bar.scale_x = 0

        # Atualizações pesadas para o minimapa e FOV, executadas a cada 0.01 segundos.
        self._update_timer += time.dt
        if self._update_timer >= 0.01:
            self._update_timer = 0

            # Atualiza os indicadores do minimapa.
            for target, indicator in list(self.minimap_indicators.items()):
                if not target or not target.enabled:
                    indicator.enabled = False
                    del self.minimap_indicators[target]
                    continue
                try:
                    rel = target.world_position - self.radar.world_position
                except Exception as e:
                    print("Erro ao aceder a world_position no RadarHUD:", e)
                    continue
                x, y = rel.x, rel.z
                dist = math.sqrt(x * x + y * y)
                if dist > 500:
                    factor = 500 / dist
                    x *= factor
                    y *= factor
                ui_x = (x / 500) * self.minimap_radius
                ui_y = (y / 500) * self.minimap_radius
                indicator.position = (ui_x, ui_y)

            # Atualiza o indicador de direção.
            self.thickness = 0.3 * (camera.fov / 60.0)
            self.radar_direction_indicator.scale = (self.thickness, -self.minimap_radius * 0.5, 0.1)
            forward = camera.forward
            fwd = Vec2(forward.x, forward.z)
            if fwd.length() > 0:
                angle = math.degrees(math.atan2(fwd.x, fwd.y))
                self.radar_direction_indicator.rotation_z = angle

            # Atualiza os indicadores do painel FOV com uma tolerância de 1 grau para evitar a cintilação.
            for target, indicator in list(self.fov_indicators.items()):
                if not target or not target.enabled:
                    indicator.enabled = False
                    del self.fov_indicators[target]
                    continue
                rel = target.world_position - self.radar.world_position
                angle = math.degrees(math.atan2(rel.x, rel.z))
                relative_angle = (angle - camera.rotation_y + 180) % 360 - 180
                half_hfov = camera.fov / 2.0
                if abs(relative_angle) > half_hfov + 1:
                    indicator.enabled = False
                    continue
                else:
                    indicator.enabled = True
                ui_x = ((relative_angle + half_hfov) / (2 * half_hfov))
                horiz_dist = math.sqrt(rel.x ** 2 + rel.z ** 2)
                vertical_angle = math.degrees(math.atan2(rel.y, horiz_dist))
                relative_v_angle = (camera.rotation_x + vertical_angle)
                half_vfov = camera.fov / 2.0
                if abs(relative_v_angle) > half_vfov + 1:
                    indicator.enabled = False
                    continue
                ui_y = ((relative_v_angle + half_vfov) / (2 * half_vfov))
                indicator.position = (ui_x - 0.5, ui_y - 0.5)
