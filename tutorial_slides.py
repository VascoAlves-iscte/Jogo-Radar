from ursina import *

class TutorialSlides(Entity):
    def __init__(self, slides, auto_advance_time=60, default_image_scale=(0.5, 0.5), default_image_position=(0, -0.2), **kwargs):
        """
        slides: lista de dicionários com os dados de cada slide.
            Cada slide pode ter as seguintes chaves:
                'text': Texto do slide.
                'image': Caminho para uma imagem estática.
                'image_scale': Escala para a primeira imagem.
                'image_position': Posição para a primeira imagem.
                'image2': Caminho para uma segunda imagem estática (opcional).
                'image2_scale': Escala para a segunda imagem.
                'image2_position': Posição para a segunda imagem.
                'on_enter': Callback executado ao entrar neste slide.
                'on_exit': Callback executado ao sair deste slide.
        auto_advance_time: tempo (em segundos) para avançar automaticamente para o próximo slide.
        default_image_scale: escala padrão para a imagem, se não definida.
        default_image_position: posição padrão para a imagem, se não definida.
        """
        super().__init__(parent=camera.ui, **kwargs)
        self.slides = slides
        self.auto_advance_time = auto_advance_time
        self.default_image_scale = default_image_scale
        self.default_image_position = default_image_position
        self.current_index = 0
        self.slide_entity = Entity(parent=self)  # Container para o conteúdo do slide
        self.display_slide(self.current_index)

    def display_slide(self, index):
        # Se existir um slide anterior com on_exit, chama-o
        if self.current_index < len(self.slides):
            prev_slide = self.slides[self.current_index]
            if 'on_exit' in prev_slide and callable(prev_slide['on_exit']):
                try:
                    prev_slide['on_exit']()
                except Exception as e:
                    print("Erro no on_exit do slide anterior:", e)
        self.current_index = index

        # Remove o conteúdo do slide anterior.
        for child in self.slide_entity.children:
            destroy(child)
        
        slide = self.slides[index]
        
        # Cria o texto do slide.
        Text(
            text=slide.get('text', ''),
            parent=self.slide_entity,
            scale=1.5,
            position=(0, 0.3),
            origin=(0, 0),
            color=color.white,
            background=True
        )
        
        # Exibe a primeira imagem ou animação.
        if 'image' in slide:
            image_scale = slide.get('image_scale', self.default_image_scale)
            image_position = slide.get('image_position', self.default_image_position)
            if slide['image'].endswith('.gif'):
                Animation(
                    slide['image'],
                    parent=self.slide_entity,
                    position=image_position,
                    scale=image_scale
                )
            else:
                Sprite(
                    texture=slide['image'],
                    parent=self.slide_entity,
                    position=image_position,
                    scale=image_scale
                )
        
        # Exibe a segunda imagem ou animação, se definida.
        if 'image2' in slide:
            image2_scale = slide.get('image2_scale', self.default_image_scale)
            image2_position = slide.get('image2_position', self.default_image_position)
            if slide['image2'].endswith('.gif'):
                Animation(
                    slide['image2'],
                    parent=self.slide_entity,
                    position=image2_position,
                    scale=image2_scale
                )
            else:
                Sprite(
                    texture=slide['image2'],
                    parent=self.slide_entity,
                    position=image2_position,
                    scale=image2_scale
                )
        
        
        # Chama o callback on_enter se definido
        if 'on_enter' in slide and callable(slide['on_enter']):
            try:
                slide['on_enter']()
            except Exception as e:
                print("Erro no on_enter do slide:", e)
        
        # Avança automaticamente após o tempo definido.
        invoke(self.next_slide, delay=self.auto_advance_time)

    def next_slide(self):
        self.current_index += 1
        if self.current_index < len(self.slides):
            self.display_slide(self.current_index)
        else:
            self.end_slides()
    
    def prev_slide(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.display_slide(self.current_index)

    def end_slides(self):
        destroy(self)
