from ursina import *
from target import Target
from tutorial_slides import TutorialSlides  # Importa o módulo dos slides

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
    
    # Define os slides educativos com os textos desejados
    slides = [
        {
            'text': (
                "1. Introdução:\n\n"
                "Bem-vindo ao tutorial! Aqui, vais aprender como funciona um sistema de radar,\n" 
                "o conceito de RCS (Radar Cross-Section), a influência dos materiais na deteção,\n" 
                "e como a tecnologia stealth e as contramedidas de chaff/flare são usadas para evitar a deteção\n"
                " e destruição. Vamos começar com uma explicação básica sobre o funcionamento do radar."
            ),
           
        },
        {
            'text': (
                "2. Como Funciona um Radar? \n\n"
                "Um radar é um sistema que usa ondas de rádio para detetar e localizar objetos à distância.\n"
                "Funciona enviando um sinal de rádio (onda eletromagnética) na direção de um alvo.\n "
                "Quando esse sinal atinge o alvo, parte da energia é refletida de volta para o radar.\n"
                " O sistema analisa o sinal refletido e determina a distância, a velocidade e a direção do alvo."  
            ),
            'image': 'assets/radarops.gif',
            'image_scale': (1, 0.5),
            'image_position': (0, -0.1)
        },
        {
            'text': (
                "3. O q é a Radar Cross Section (RCS)? \n"
                "A RCS é uma medida de quão detetável um objeto é pelo radar. Quanto maior mais energia reflete \n"
                "de volta para o radar, tornando-o mais fácil de detetar. O RCS depende de vários fatores:\n "
                "Material do Alvo: Diferentes materiais refletem a energia do radar de forma diferente. \n"
                "Tamanho do Alvo: Objetos maiores tendem a refletir mais energia.\n"  
                "Geometria do Alvo: Superfícies planas e angulares refletem o sinal para longe do radar.\n"
                "Esta imagem mostra os diferentes RCS de vários objetos. \n"
                "Nota que aviões fabricados com tecnologia stealth,como o F-35 'Lightning II', o F-117 'NightHawk' \n"
                "e o B-2 'Spirit', têm um RCS muito menor do que aviões convencionais."
            ),
            'image': 'assets/RCS_example.jpeg',
            'image_scale': (0.069, 0.05),
            'image_position': (0, -0.1)
        },
        {
            'text': (
                "4. Controlos do Jogo \n"
                "Aqui estão os controlos que vais usar para operar o radar e destruir os alvos:\n"
                "R: Ligar/desligar o radar. Mantém o radar apontado ao alvo até se realizar o 'lock'.\n"
                "Quando isto acontece, o radar segue automaticamente o movimento do alvo.\n"
                "Barra de Espaço: Lançar um míssil que irá seguir o alvo 'locked'.\n"
                "Scroll Up/Down: Zoom.\n"
                "A bateria de mísseis do radar só pode conter 4 mísseis de cada vez.\n"
                "A bateria suporta 4 mísseis de cada vez e demora 3 segundos a recarregar.\n"
                " Planeia os teus disparos!"
            ),
        },
        {
            'text': (
                "5. Alvos para praticar\n\n"
                "Para demonstrar como o RCS e os materiais afetam a deteção, vais enfrentar dois alvos de teste:\n"
                "Cubo Metálico: Altamente refletivo, fácil de detetar. \n"
                "Serve para mostrar como materiais metálicos e formas simples refletem muita energia.\n"
                "Bola de Madeira: Menos refletiva, mais difícil de detetar. \n"
                "Demonstra como materiais não metálicos e formas arredondadas reduzem a reflexão do radar."
            ),
        },
        {
            'text': (
                "6. Tecnologia Stealth \n\n"
                "Agora que já entendes o básico do radar e do RCS, vamos introduzir a tecnologia stealth.\n"
                "Como já foi mencionado anteriormente esta tecnologia é usada para reduzir\n"
                "a detetabilidade dos objetos. Isto é feito principalmente de duas maneiras:\n"
                "Geometria do objeto e Materiais Absorventes de Radar (RAM)\n"
                "Estes materiais são projetados para absorver a energia do radar, em vez de a refletir de volta.\n"
                "Aqui está uma das primeiras aeronaves stealth fabricadas, o F-117 'NightHawk'.\n"
                "Nota a geometria particular e complexa, desenhada para dissipar o máximo de energia possível."
            
            ),
            'image': 'assets/f117nighthawk.jpg',
            'image_scale': (0.033, 0.025),
            'image:position': (0, -0.2)
        },
        {
            'text': (
                "Neste jogo, vais enfrentar dois alvos em particular:\n\n"
                "F-16 'Fighting Falcon': Um alvo feito de materiais compósitos. \n"
                "Relativamente fácil de detetar e abater, pois não foi projetado para ser stealth.\n\n"
                "F-22 'Raptor': Um alvo feito com materiais RAM e com uma forma projetada para evitar deteção.\n"
                "Muito mais difícil de detetar e abater."
                
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
                "7.Contramedidas de Chaff & Flare: O que São e Como Funcionam no Jogo\n\n"
                "O chaff é um sistema de contramedida antirradar que dispersa pequenos pedaços de alumínio,\n"
                "fibra de vidro metalizada no ar.Forma uma 'nuvem de partículas' que cria um grande \n"
                "radar cross-section (RCS),confundindo ou cegando os sistemas de radar. \n"
                "No jogo, depois de disparares um míssil contra um alvo, este pode lançar chaff para tentar\n"
                "evitar ser atingido. \n"
                "Boa Sorte!\n"
             
            ),
            'image': 'assets/chaff flare.jpg',
            'image_scale': (0.2, 0.1),
            'image_position': (0, -0.2)
        }
    ]
    
    # Instancia os slides educativos automaticamente ao carregar o nível
    TutorialSlides(slides)
    
    return floor, targets, level_update
