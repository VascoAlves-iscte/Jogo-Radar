import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class ElectromagneticWave:
    def __init__(self, amplitude=1.0, wavelength=10.0, period=5.0, space_range=50, resolution=500):
        self.amplitude = amplitude
        self.wavelength = wavelength
        self.k = 2 * np.pi / wavelength  # Número de onda
        self.period = period
        self.omega = 2 * np.pi / period  # Frequência angular
        self.x = np.linspace(0, space_range, resolution)

    def wave_function(self, t):
        return self.amplitude * np.sin(self.k * self.x - self.omega * t)

    def animate(self):
        fig, ax = plt.subplots()
        line, = ax.plot(self.x, self.wave_function(0), color='blue', lw=2)

        ax.set_xlabel("Posição (x)")
        ax.set_ylabel("Campo Elétrico (E)")
        ax.set_title("Simulação de Onda Eletromagnética")
        ax.set_ylim(-1.5 * self.amplitude, 1.5 * self.amplitude)

        def update(frame):
            t = frame * 0.1
            line.set_ydata(self.wave_function(t))
            return line,

        ani = animation.FuncAnimation(fig, update, frames=200, interval=50, blit=True)
        plt.show()

# Testar a simulação
if __name__ == "__main__":
    wave = ElectromagneticWave()
    wave.animate()
