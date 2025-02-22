import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Rectangle, Polygon
from matplotlib.path import Path

# Escolha: True para figura complexa (estrela) ou False para quadrado simples
use_complex_figure = True

# Parâmetros da simulação
nx, ny = 200, 200           # tamanho da grade
dx = dy = 1.0               # passo espacial (unidades arbitrárias)
c = 300.0                   # velocidade da onda (para visualização)
dt = 0.9 * dx / (c * np.sqrt(2))  # passo temporal (condição CFL)

# Matrizes para o estado atual, anterior e futuro
u = np.zeros((nx, ny))
u_prev = np.zeros((nx, ny))
u_next = np.zeros((nx, ny))

if use_complex_figure:
    # --- Figura Complexa: Estrela ---
    # Definindo uma estrela com centro em (100,100)
    center = (100, 100)
    outer_radius = 15    # raio externo
    inner_radius = 7     # raio interno
    num_points = 5       # número de pontas
    # Calcula os ângulos para os vértices (alternando entre externo e interno)
    angles = np.linspace(0, 2*np.pi, num_points*2, endpoint=False)
    star_points = []
    for i, angle in enumerate(angles):
        r = outer_radius if i % 2 == 0 else inner_radius
        x = center[0] + r * np.cos(angle)
        y = center[1] + r * np.sin(angle)
        star_points.append((x, y))
    # Cria o patch para visualização
    obstacle_patch = Polygon(star_points, closed=True, edgecolor='red',
                             facecolor='none', linewidth=2, zorder=10)
    # Cria a máscara do obstáculo: para cada célula, verifica se o centro está dentro da estrela
    grid_x, grid_y = np.meshgrid(np.arange(nx), np.arange(ny), indexing='ij')
    points = np.vstack((grid_x.flatten(), grid_y.flatten())).T
    path = Path(star_points)
    inside = path.contains_points(points)
    obstacle_mask = inside.reshape((nx, ny))
else:
    # --- Figura Simples: Quadrado ---
    cube_x_start, cube_x_end = 90, 110
    cube_y_start, cube_y_end = 90, 110
    obstacle_mask = np.zeros((nx, ny), dtype=bool)
    obstacle_mask[cube_x_start:cube_x_end, cube_y_start:cube_y_end] = True
    obstacle_patch = Rectangle((cube_y_start, cube_x_start),
                               cube_y_end - cube_y_start,
                               cube_x_end - cube_x_start,
                               linewidth=2, edgecolor='red', facecolor='none', zorder=10)

# Parâmetros da fonte (ponto emissor) - próximo à borda esquerda
source_x, source_y = 20, 100

# Número total de iterações (passos de tempo)
num_steps = 300

# Cria a máscara de amortecimento para as fronteiras (absorção)
damp_width = 20  # largura da camada absorvente (em células)
damp = np.ones((nx, ny))
for i in range(nx):
    for j in range(ny):
        factor_i = 1.0
        factor_j = 1.0
        if i < damp_width:
            factor_i = i / damp_width
        elif i >= nx - damp_width:
            factor_i = (nx - 1 - i) / damp_width
        if j < damp_width:
            factor_j = j / damp_width
        elif j >= ny - damp_width:
            factor_j = (ny - 1 - j) / damp_width
        damp[i, j] = min(factor_i, factor_j)

# Configuração do plot
fig, ax = plt.subplots()
im = ax.imshow(u, cmap='viridis', interpolation='nearest', vmin=-1, vmax=1, zorder=1)
ax.set_title("Propagação e Reflexão 2D de Onda sobre um Obstáculo")
ax.add_patch(obstacle_patch)

def update(frame):
    global u, u_prev, u_next
    # Atualiza os pontos internos usando o esquema de diferenças finitas
    for i in range(1, nx - 1):
        for j in range(1, ny - 1):
            if obstacle_mask[i, j]:
                # Dentro do obstáculo, força a condição fixa (u = 0)
                u_next[i, j] = 0
            else:
                u_next[i, j] = (2 * u[i, j] - u_prev[i, j] +
                    (c * dt / dx)**2 * (u[i+1, j] + u[i-1, j] + u[i, j+1] + u[i, j-1] - 4 * u[i, j]))
                # Aplica o fator de amortecimento próximo às bordas
                u_next[i, j] *= damp[i, j]
    # Adiciona um pulso na fonte nos primeiros 20 quadros
    if frame < 20:
        u_next[source_x, source_y] += np.sin(2 * np.pi * frame / 20)
    # Atualiza as matrizes de tempo
    u_prev, u = u.copy(), u_next.copy()
    im.set_array(u)
    return [im, obstacle_patch]

ani = animation.FuncAnimation(fig, update, frames=num_steps, interval=30, blit=True)
plt.show()
