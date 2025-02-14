from vpython import *

# Cria o ambiente 3D (canvas) com um fundo claro (ex: ciano)
scene = canvas(title="Ambiente 3D - Simulação de Objetos Radar", background=color.cyan)

# Cria um "chão" para distinguir da "parte do céu"
ground = box(pos=vector(0, -1.5, 0), size=vector(50, 0.1, 50), color=color.green)

# Função para spawnar uma esfera
def spawn_esfera(pos, raio=1, cor=color.red):
    return sphere(pos=vector(*pos), radius=raio, color=cor)

# Função para spawnar um cubo (box em VPython)
def spawn_cubo(pos, tamanho=1, cor=color.blue):
    return box(pos=vector(*pos), size=vector(tamanho, tamanho, tamanho), color=cor)

# Função para spawnar uma pirâmide
def spawn_piramide(pos, tamanho=1, cor=color.green):
    return pyramid(pos=vector(*pos), size=vector(tamanho, tamanho, tamanho), color=cor)

# Função para spawnar uma "cunha" (alternativa usando pyramid rotacionada)
def spawn_cunha(pos, tamanho=1, cor=color.yellow):
    cunha = pyramid(pos=vector(*pos), size=vector(tamanho, tamanho, tamanho), color=cor)
    cunha.rotate(angle=0.5, axis=vector(0, 1, 0))
    return cunha

# Spawn dos objetos no ambiente 3D
esfera = spawn_esfera((0, 0, 0), raio=1, cor=color.red)
cubo = spawn_cubo((3, 0, 0), tamanho=1.5, cor=color.blue)
piramide = spawn_piramide((-3, 0, 0), tamanho=1.5, cor=color.green)
cunha = spawn_cunha((0, 3, 0), tamanho=2, cor=color.yellow)

# Mantém a janela aberta com um loop infinito
while True:
    rate(60)
