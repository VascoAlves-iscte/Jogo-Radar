# chatbox.py
from ursina import *
from collections import deque

class ChatBox(Entity):
    def __init__(self, max_messages=10, position=(-0.8, -0.4), scale=2, **kwargs):
        """
        Cria uma chatbox para exibir até max_messages na tela.
        :param max_messages: Número máximo de mensagens armazenadas.
        :param position: Posição da chatbox na UI (em coordenadas relativas).
        :param scale: Escala do texto (ajuste conforme necessário).
        """
        super().__init__(**kwargs)
        self.max_messages = max_messages
        self.messages = deque(maxlen=max_messages)
        # Cria o componente Text e o anexa à UI da câmera
        self.text_entity = Text(
            text="",
            origin=(0, 0),
            position=position,
            scale=scale,
            parent=camera.ui,
            color=color.white,
            background=True,
            background_color=color.black33,
            word_wrap=True
        )
    
    def add_message(self, message):
        """
        Adiciona uma mensagem à chatbox e atualiza o componente Text.
        """
        message = message.strip()
        if message:
            self.messages.append(message)
            self.text_entity.text = "\n".join(self.messages)

# Variável global que armazenará a instância da chatbox
chatbox_instance = None

def initialize_chatbox(max_messages=10, position=(-0.8, -0.4), scale=2):
    """
    Inicializa a chatbox e armazena a instância global.
    """
    global chatbox_instance
    chatbox_instance = ChatBox(max_messages=max_messages, position=position, scale=scale)
    return chatbox_instance

def println(*args, **kwargs):
    """
    Função customizada para imprimir mensagens no terminal e na chatbox.
    Apenas as mensagens enviadas por esta função serão exibidas na interface.
    """
    message = " ".join(map(str, args))
    # Imprime normalmente no terminal.
    print(message, **kwargs)
    # Se a chatbox estiver inicializada, adiciona a mensagem.
    if chatbox_instance is not None:
        chatbox_instance.add_message(message)
