import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
# Para projeções 3D no Matplotlib
from mpl_toolkits.mplot3d import Axes3D

class ElectromagneticWave3D:
    def __init__(self, amplitude=1.0, wavelength=10.0, period=5.0, grid_size=50, space_range=20):
        """
        amplitude: amplitude da onda (A)
        wavelength: comprimento de onda (λ)
        period: período (T)
        grid_size: número de pontos em cada dimensão (x, y, z)
        space_range: extensão do espaço (será de -space_range/2 a +space_range/2 em cada eixo)
        """
        self.amplitude = amplitude
        self.wavelength = wavelength
        self.period = period

        # Frequência angular ω e número de onda k
        self.omega = 2 * np.pi / period     # ω = 2π / T
        self.k = 2 * np.pi / wavelength    # k = 2π / λ

        # Cria o espaço 3D: de -space_range/2 até +space_range/2
        self.x = np.linspace(-space_range/2, space_range/2, grid_size)
        self.y = np.linspace(-space_range/2, space_range/2, grid_size)
        self.z = np.linspace(-space_range/2, space_range/2, grid_size)

        # Cria uma malha 3D (X, Y, Z) - cada um é um array 3D
        self.X, self.Y, self.Z = np.meshgrid(self.x, self.y, self.z, indexing='ij')

    def wave_function(self, t):
        """
        Retorna E(x,y,z,t) para todos os pontos (X, Y, Z).
        A onda é esférica, com r = sqrt(x^2 + y^2 + z^2).
        """
        R = np.sqrt(self.X**2 + self.Y**2 + self.Z**2)
        return self.amplitude * np.sin(self.k * R - self.omega * t)

    def animate(self):
        """
        Anima a onda 3D, mas mostrando apenas um corte no plano z=0.
        Nesse corte, interpretamos a "altura" da onda como valor no eixo Z.
        """
        # Índice aproximado para z=0 (meio do array)
        z_index = self.z.size // 2

        # Configura a figura e o eixo 3D
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        # Para simplificar, criamos uma malha 2D (X2D, Y2D) só no plano z=0
        X2D, Y2D = np.meshgrid(self.x, self.y, indexing='ij')

        # Calcula a onda no instante t=0
        initial_data = self.wave_function(0)[:, :, z_index]

        # Cria a superfície inicial: interpretamos "initial_data" como altura (Z)
        surf = ax.plot_surface(X2D, Y2D, initial_data, cmap='viridis')

        # Ajusta os eixos
        ax.set_title("Simulação de Onda Eletromagnética 3D (Corte z=0)")
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_zlabel("Amplitude")
        ax.set_zlim(-self.amplitude, self.amplitude)

        # Função de atualização a cada frame
        def update(frame):
            t = frame * 0.1  # Define o passo de tempo
            # Recalcula a onda no corte z=0
            data = self.wave_function(t)[:, :, z_index]

            # Limpa o eixo antes de redesenhar
            ax.clear()
            ax.set_title(f"Onda 3D no tempo t={t:.1f}")
            ax.set_xlabel("x")
            ax.set_ylabel("y")
            ax.set_zlabel("Amplitude")
            ax.set_zlim(-self.amplitude, self.amplitude)

            # Desenha a nova superfície
            surf = ax.plot_surface(X2D, Y2D, data, cmap='viridis')
            return surf,

        # Cria a animação
        ani = animation.FuncAnimation(
            fig, update, frames=100, interval=100, blit=False
        )

        plt.show()

# Se quiser testar diretamente
if __name__ == '__main__':
    wave3d = ElectromagneticWave3D(
        amplitude=1.0,
        wavelength=10.0,
        period=5.0,
        grid_size=50,
        space_range=20
    )
    wave3d.animate()
