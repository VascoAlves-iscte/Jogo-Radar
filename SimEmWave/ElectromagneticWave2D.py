import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class ElectromagneticWave2D:
    def __init__(self, amplitude=1.0, wavelength=10.0, period=5.0, grid_size=200, space_range=50):
        """
        amplitude: amplitude da onda (v/m)
        wavelength: comprimento de onda (m)
        period: período da onda (s)
        grid_size: número de pontos em cada dimensão da grade
        space_range: tamanho total do espaço em cada dimensão (será de -space_range/2 a space_range/2)
        """
        self.amplitude = amplitude
        self.wavelength = wavelength
        self.period = period
        self.freqAng = 2 * np.pi / period  # Calcula a frequência angular (ω = 2π/T) (rad/s)
        self.k = 2 * np.pi / wavelength    # Calcula o número de onda (k = 2π/λ) (rad/m)
        
        # Definindo os limites do espaço (centralizado na origem)
        self.x = np.linspace(-space_range/2, space_range/2, grid_size) # Gera um array de valores igualmente espaçados para os eixos x e y, cobrindo o intervalo desejado.
        self.y = np.linspace(-space_range/2, space_range/2, grid_size) 
        self.X, self.Y = np.meshgrid(self.x, self.y) #Cria duas matrizes que contêm as coordenadas x e y de cada ponto da grade. São usadas para calcular a distância de cada ponto em relação à origem.

    def wave_function(self, t):
        """
         Calcular o valor do campo elétrico E(x,y,t) para cada ponto da grade no instante 𝑡.
        """
        # Distância radial de cada ponto em relação à origem (fonte da onda)
        R = np.sqrt(self.X**2 + self.Y**2)
        return self.amplitude * np.sin(self.k * R - self.freqAng * t) #representa a função seno que descreve a oscilação da onda multiplicada pela amplitude para ajustar a altura máxima da onda.

    def animate(self):
        """
        Anima a propagação da onda eletromagnética 2D.
        """
        fig, ax = plt.subplots() #cria uma figura e um conjunto de eixos onde a animação será exibida.
        
        # Cálculo inicial para t = 0
        initial_data = self.wave_function(0)
        
        # Exibe a imagem usando imshow; definindo extent para mapear os eixos x e y
        im = ax.imshow(
            initial_data, 
            extent=(self.x[0], self.x[-1], self.y[0], self.y[-1]),
            cmap='RdBu', 
            vmin=-self.amplitude,  
            vmax=self.amplitude,
            animated=True
        )
        
        ax.set_title("Simulação de Onda Eletromagnética 2D")
        ax.set_xlabel("x")
        ax.set_ylabel("y")

        def update(frame): #Função chamada para cada frame
            t = frame * 0.1  # O tempo pode ser escalonado conforme desejado
            data = self.wave_function(t)
            im.set_data(data)
            return im,

        # Cria a animação com 200 frames e um intervalo de 50ms entre cada frame
        ani = animation.FuncAnimation(fig, update, frames=200, interval=50, blit=True)
        plt.show()

if __name__ == '__main__':
    wave2d = ElectromagneticWave2D(amplitude=1.0, wavelength=10.0, period=5.0, grid_size=200, space_range=50)
    wave2d.animate()
