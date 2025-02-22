from ursina import Entity, color

class Target(Entity):
    """
    Classe base para os alvos.
    Agora aceita propriedades de material para o cálculo do RCS e incorpora a detecção via colisão.
    """
    MATERIALS = {
        "metal": 3.0,      # Geralmente alto, pois metais refletem muito
        "plastic": 1.4,    # Valor menor, pois plásticos costumam refletir menos
        "composite": 2.0,  # Compósitos têm refletividade intermediária
        "stealth": 0.8     # Stealth: projetado para refletir muito pouco
    }

    def __init__(self, model_name=None, model=None, position=(0,0,0), scale=1.5, color=color.white, material_type="metal", **kwargs):
        if model is None:
            model = model_name
        super().__init__(model=model, position=position, scale=scale, color=color, **kwargs)
        self.material_type = material_type  
        self.refractive_index = self.MATERIALS.get(material_type, 1.5)  

    def get_rcs(self, radar_position):
        """
        Retorna o RCS calculado para este alvo.
        Agora utiliza a função 'calcular_rcs_com_colisao', que emprega colisão para extrair a normal do ponto de impacto.
        """
        from rcs import calcular_rcs_com_colisao  # Importação interna para evitar import circular
        return calcular_rcs_com_colisao(self, radar_position)
    
    def get_model_name(self):
        if isinstance(self.model, str):
            return self.model
        elif hasattr(self, 'model_name') and self.model_name:
            return self.model_name
        else:
            return str(self.model)
