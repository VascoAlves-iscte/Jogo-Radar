# target.py
from ursina import Entity, color

class Target(Entity):
    """
    Classe base para os alvos.
    Cada alvo é uma entidade 3D.
    Agora aceita tanto o parâmetro 'model_name' quanto 'model'.
    """
    def __init__(self, model_name=None, model=None, position=(0,0,0), scale=1.5, color=color.white, **kwargs):
        # Se o parâmetro 'model' for fornecido, ele tem prioridade.
        if model is None:
            model = model_name
        super().__init__(model=model, position=position, scale=scale, color=color, **kwargs)
