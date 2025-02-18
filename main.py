from ursina import *
from radar import Radar
from target import Target

app = Ursina()

# 🌌 Skybox for environment
sky = Sky()

# 🟩 Ground (Floor)
floor = Entity(
    model='plane',
    scale=(50, 1, 50),
    texture='white_cube',
    texture_scale=(50, 50),
    color=color.green,
    collider='box'
)
floor.position = (0, 0, 0)

# ✈️ Load F-16 Model
f16_model = load_model('f16CleanWings.obj')

# 🎯 Create Targets
targets = [
    Target(model_name='sphere', position=(-5, 1, 0), color=color.red, scale=1, collider='box'),
    Target(model_name='cube', position=(5, 1, 0), color=color.blue, scale=1, collider='box'),
    Target(model=f16_model, position=(0, 1, 5), color=color.pink, scale=1, collider='box')
]

# 🎯 Create Radar and Pass Targets (FIXED)
radar = Radar(position=(0, 0, -20), targets=targets)

app.run()
