from ursina import *
from radar import Radar
from target import Target

app = Ursina()

# Criando o ambiente
sky = Sky()

floor = Entity(
    model='plane',
    scale=(50, 1, 50),
    texture='white_cube',
    texture_scale=(50, 50),
    color=color.green,
    collider='box'
)
floor.position = (0, 0, 0)

editor_camera = EditorCamera()
editor_camera.position = (0, 5, -15)
editor_camera.rotation_x = 10

radar = Radar(camera)

f16_model = load_model('f16CleanWings.obj')

# Criando os outros alvos
targets = [
    Target(model_name='sphere', position=(-5, 1, 0), color=color.red, scale=1),
    Target(model_name='cube', position=(5, 1, 0), color=color.blue, scale=1),
    Target(model=f16_model, position=(0, 1, 5),color =color.pink, scale=1)
  
]

def update():
    radar.update()
   

app.run()
