# radar.py
from ursina import held_keys

class Radar:
    """
    Classe que representa o 'radar', responsável por controlar a câmera.
    """
    def __init__(self, camera):
        self.camera = camera

    def update(self):
        # Movimenta a câmera (radar) com as teclas 'a' e 'd'
        if held_keys['a']:
            self.camera.x -= 0.05
        if held_keys['d']:
            self.camera.x += 0.05
        if held_keys['w']:
            self.camera.z += 0.05
        if held_keys['s']:
            self.camera.z -= 0.05