from ursina import *
from target import Target
from tutorial_slides import TutorialSlides


# Variável global para armazenar os inimigos de prática.
practice_targets = []

def load_level_tutorial():
    # Remove qualquer slide anterior, se existir.
    for child in list(camera.ui.children):
        if isinstance(child, TutorialSlides):
            destroy(child)

    # Cria o chão (shooting range)
    floor = Entity(
        model='plane',
        scale=(20, 1, 1000),
        texture='white_cube',
        texture_scale=(20, 1000),
        color=color.green,
        collider=None,
        position=(0, 0, 500)
    )
    
    # Cria os targets (exemplo)
    f16_model = load_model('f16CleanWings.obj')
    f22_model = load_model('f22.obj')
    
    targets = []
    composite_f16 = Target(
        model=f16_model,
        position=(-30, 3, 200),
        color=color.red,
        scale=1,
        collider='box',
        material_type="composite"
    )
    targets.append(composite_f16)
    
    stealth_f22 = Target(
        model=f22_model,
        position=(30, 5, 100),
        color=color.orange,
        scale=0.7,
        collider='box',
        material_type="stealth"
    )
    targets.append(stealth_f22)
    
    # Função de update do nível
    def level_update():
        radar_position = Vec3(0, 0, 0)
        for target in targets:
            target.look_at(radar_position)
    
    # Callback para spawnar inimigos de prática.
    # Os inimigos são adicionados à lista global 'practice_targets' e também à lista 'targets'.
    def spawn_enemies():
        nonlocal targets
        global practice_targets
        print("Spawning practice enemies...")
        # Remove inimigos antigos, se houver.
        remove_enemies()
        practice_targets = []
        enemy_positions = [(-10, 2, 100), (10, 2, 100)]
        for pos in enemy_positions:
            enemy = Target(
                model='sphere',
                position=pos,
                color=color.pink,
                scale=0.7,
                collider='box',
                material_type="metal"
            )
            practice_targets.append(enemy)
            targets.append(enemy)
        
        
    
    # Callback para remover os inimigos de prática da lista de targets e destruí-los.
    def remove_enemies():
        nonlocal targets
        global practice_targets
        print("Removing practice enemies...")
        if practice_targets:
            for enemy in practice_targets:
                if enemy in targets:
                    targets.remove(enemy)
                destroy(enemy)
            practice_targets = []

    # Define os slides educativos com os textos desejados.
    slides = [
        {
            'text': (
                "1. Introdução:\n\n"
                "Bem-vindo ao tutorial! Aqui, vais aprender como funciona um sistema de radar,\n" 
                "o conceito de RCS (Radar Cross-Section), a influência dos materiais na deteção,\n" 
                "e como a tecnologia stealth e as contramedidas de chaff/flare são usadas para evitar a deteção\n"
                "e destruição. Vamos começar com uma explicação básica sobre o funcionamento do radar.\n\n"
                "Page Up: Avançar | Page Down: Voltar"
            ),
        },
        {
            'text': (
                "2. Como Funciona um Radar? \n\n"
                "Um radar é um sistema que usa ondas de rádio para detetar e localizar objetos à distância.\n"
                "Funciona enviando um sinal de rádio (onda eletromagnética) na direção de um alvo.\n"
                "Quando esse sinal atinge o alvo, parte da energia é refletida de volta para o radar.\n"
                "O sistema analisa o sinal refletido e determina a distância, a velocidade e a direção do alvo."  
            ),
            'image': 'assets/radarops.gif',
            'image_scale': (1, 0.5),
            'image_position': (0, -0.1)
        },
        {
            'text': (
                "3. O que é a Radar Cross Section (RCS)? \n"
                "A RCS é uma medida de quão detetável um objeto é pelo radar. Quanto maior, mais energia reflete\n"
                "de volta para o radar, tornando-o mais fácil de detetar. O RCS depende de vários fatores:\n"
                "- Material do Alvo: Diferentes materiais refletem a energia de forma distinta.\n"
                "- Tamanho do Alvo: Objetos maiores tendem a refletir mais energia.\n"  
                "- Geometria do Alvo: Superfícies planas e angulares podem refletir o sinal para longe do radar.\n"
                "Esta imagem mostra os diferentes RCS de vários objetos.\n"
                "Nota: Aviões stealth, como o F-35, F-117 e B-2, têm um RCS significativamente menor."
            ),
            'image': 'assets/RCS_example.jpeg',
            'image_scale': (0.069, 0.05),
            'image_position': (0, -0.1)
        },
        {
            'text': (
                "4. Tecnologia Stealth \n\n"
                "Agora que já entendes o básico do radar e do RCS, vamos introduzir a tecnologia stealth.\n"
                "Esta tecnologia reduz a detetabilidade dos objetos por meio da geometria e dos Materiais Absorventes de Radar (RAM).\n"
                "Aqui está uma das primeiras aeronaves stealth, o F-117 'NightHawk'.\n"
                "Nota: A geometria complexa é desenhada para dissipar o máximo de energia possível."
            ),
            'image': 'assets/f117nighthawk.jpg',
            'image_scale': (0.033, 0.025),
            'image_position': (0, -0.2)
        },
        {
            'text': (
                "5. Neste jogo, vais enfrentar dois alvos em particular:\n\n"
                "F-16 'Fighting Falcon': Alvo feito de materiais compósitos. Fácil de detetar e abater, pois não é stealth.\n\n"
                "F-22 'Raptor': Alvo feito com materiais RAM e com geometria para evitar deteção. Mais difícil de detetar e abater."
            ),
            'image': 'assets/f16 Viper.jpg',
            'image_scale': (0.022, 0.022),
            'image_position': (-0.25, -0.2),
            'image2': 'assets/f22 raptor.jpg',
            'image2_scale': (0.05, 0.037),
            'image2_position': (0.25, -0.2)
        },
        {
            'text': (
                "6. Contramedidas de Chaff & Flare: O que São e Como Funcionam no Jogo\n\n"
                "O chaff é um sistema de contramedida antirradar que dispersa partículas de alumínio e fibra de vidro metalizada.\n"
                "Forma uma 'nuvem de partículas' que aumenta o RCS, confundindo ou cegando os radares.\n"
                "No jogo, após disparares um míssil, o alvo pode lançar chaff para evitar ser atingido.\n"
                "Boa Sorte!"
            ),
            'image': 'assets/chaff flare.jpg',
            'image_scale': (0.2, 0.1),
            'image_position': (0, -0.2)
        },
        {
            'text': (
                "7. Controlos do Jogo \n"
                "Aqui estão os controlos que vais usar para operar o radar e destruir os alvos:\n"
                "R: Ligar/desligar o radar. Mantém o radar apontado ao alvo até se realizar o 'lock'.\n"
                "Quando isto acontece, o radar segue automaticamente o movimento do alvo.\n"
                "Barra de Espaço: Lançar um míssil que seguirá o alvo 'locked'.\n"
                "Scroll Up/Down: Zoom.\n"
                "A bateria de mísseis do radar suporta 4 mísseis e demora 3 segundos para recarregar.\n"
                "Planeia os teus disparos!"
            ),
            
        },
        {
            'text': "Testa os controlos nestes alvos de prática\n\n",
            'on_enter': spawn_enemies,
            'on_exit': remove_enemies
        },
        {
            'text': "Tutorial Completo! Pressiona 'Esc' para repetir ou voltar ao menu principal \n"
            "Boa sorte!",
        },
    ]
    
    # Instancia os slides educativos automaticamente ao carregar o nível.
    TutorialSlides(slides)
    
    return floor, targets, level_update
