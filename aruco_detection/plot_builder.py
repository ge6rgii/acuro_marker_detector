from abc import ABC, abstractmethod
import matplotlib.animation as animation
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


class BasePlotBuilder(ABC):

    def __init__(self, coordinates_generator) -> None:
        self.figure, self.axes = plt.subplots()
        self.coordinates_generator = coordinates_generator()
        self.x, self.y, self.z = [], [], []

    @abstractmethod
    def plot_drawer(self):
        pass

    def draw_animated_plot(self):
        # This unused "anim" var is important to avoid unwanted garbage collection.
        anim = animation.FuncAnimation(self.figure, self.plot_drawer, repeat=False)
        plt.show()


class PlotBuilder2D(BasePlotBuilder):

    def __init__(self, coordinates_generator) -> None:
        super().__init__(coordinates_generator)

    def plot_drawer(self, _):
        x, y = next(self.coordinates_generator)
        self.x.append(x)
        self.y.append(y)
        self.axis.clear()
        self.axis.plot(self.x, self.y)


class PlotBuilder3D(BasePlotBuilder):

    def __init__(self, coordinates_generator) -> None:
        super().__init__(coordinates_generator)
        self.axis = self.figure.add_subplot(111, projection='3d')

    def plot_drawer(self, _):
        x, y, z = next(self.coordinates_generator)
        self.x.append(x)
        self.y.append(y)
        self.z.append(z)
        self.axis.clear()
        self.axis.plot(self.x, self.y, self.z)

    def draw_animated_3d_plot(self):
        self.draw_animated_plot()
        Axes3D.plot()
