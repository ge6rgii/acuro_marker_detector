import matplotlib.animation as animation
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


class PlotBuilder:

    def __init__(self, width, height, coordinates_generator) -> None:
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.width, self.height = width, height
        self.x, self.y, self.z = [], [], []
        self.coordinates_generator = coordinates_generator()

    def plot_drawer(self, _):
        x, y, z = next(self.coordinates_generator)
        self.x.append(x)
        self.y.append(y)
        self.z.append(z)
        self.ax.clear()
        self.ax.plot(self.x, self.y, self.z)

    def build_anumated_2d_plot(self):
        # This unused "anum" definition is necessary
        # to avoid garbage collection of FuncAnimation.
        anim = animation.FuncAnimation(self.fig, self.plot_drawer, repeat=False)
        plt.show()
        Axes3D.plot()
