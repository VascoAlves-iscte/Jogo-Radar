from ursina import *

class Radar(Entity):
    """
    Classe que representa o radar fixo no mapa.
    A câmera rotaciona conforme o movimento do mouse sem limite e de forma suave.
    """
    def __init__(self, position=(20, 1, -20), **kwargs):
        super().__init__(position=position, **kwargs)

        # Ajusta a posição inicial da câmera no radar
        camera.parent = self
        camera.position = (0, 2, 0)  # Ajusta a altura da câmera para a visão do radar

        # Crosshair (mira no centro da tela)
        self.crosshair = Text('+', scale=2, position=(0, 0), origin=(0, 0), color=color.yellow)

        # 🔥 **Efeito de radar ativado (overlay cobrindo toda a tela)**
        self.overlay = Entity(
            parent=camera.ui, model='quad',
            scale=(10, 10),  
            color=color.green,  # 🔥 Começa com verde sólido
            z=-0.1,  
            enabled=False
        )

        # Estado do radar
        self.radar_ligado = False
        self.cor_atual = color.green  # 🔥 Começa com verde

        # Sensibilidade do mouse
        self.sensibilidade = 100 

        # Suavização de movimento
        self.smooth_x = 0  
        self.smooth_y = 0

        # Esconder o cursor para melhor controle
        mouse.visible = False  

        # 🔊 **Carrega o som do radar**
        self.som_radar = Audio('radar_beep.mp3', autoplay=False, loop=True)  
        self.som_duracao = 1  

    def ligar_radar(self):
        """Ativa o radar, toca o som e sincroniza o efeito visual."""
        self.radar_ligado = True
        self.overlay.enabled = True  
        self.som_radar.play()  
        print("Radar ligado - Efeito ativado")

        if self.som_radar.length > 0:
            self.som_duracao = self.som_radar.length
        else:
            self.som_duracao = 1  

        self.sincronizar_efeito()

    def desligar_radar(self):
        """Desativa o radar, para o som e remove o efeito visual."""
        self.radar_ligado = False
        self.overlay.enabled = False  
        self.som_radar.stop()  
        print("Radar desligado - Efeito desativado")

    def sincronizar_efeito(self):
        """Alterna a cor entre verde e branco no ritmo do som."""
        if self.radar_ligado:
            # 🔄 Alterna entre verde e branco
            self.cor_atual = color.white if self.cor_atual == color.green else color.green  
            self.overlay.color = self.cor_atual  # 🔥 Aplica a nova cor
            
            print(f"🔄 Pulso do radar - Nova cor: {'Branco' if self.cor_atual == color.white else 'Verde'}")  

            # 🔥 Chama a função novamente na mesma frequência do som
            invoke(self.sincronizar_efeito, delay=self.som_duracao)  

    def input(self, key):
        """Alterna o radar ao pressionar 'R' apenas uma vez"""
        if key == 'r':  
            if not self.radar_ligado:
                self.ligar_radar()
            else:
                self.desligar_radar()

    def update(self):
        """Controla a rotação da câmera conforme o movimento do mouse, suavizando a transição."""
        self.smooth_x = lerp(self.smooth_x, mouse.velocity[0] * self.sensibilidade, time.dt * 10)
        self.smooth_y = lerp(self.smooth_y, mouse.velocity[1] * self.sensibilidade, time.dt * 10)

        camera.rotation_y += self.smooth_x
        camera.rotation_x -= self.smooth_y

        camera.rotation_x = clamp(camera.rotation_x, -45, 45)
