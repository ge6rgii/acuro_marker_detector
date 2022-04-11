from abc import ABC, abstractmethod
import matplotlib.animation as animation
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


class BasePlotBuilder(ABC):

    def __init__(self, coordinates_generator):
        self.figure, self.axis = plt.subplots()
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

    def __init__(self, coordinates_generator, plane_name):
        super().__init__(coordinates_generator)
        self.plane_name = plane_name
        self.plane_coordinates = self.get_plane_coordinates(plane_name)

    @staticmethod
    def get_plane_coordinates(plane):
        return {
            "FRONT": [0, 1],
            "SAGITTAL": [1, 2],
            "TRANSVERSE": [0, 2],
        }.get(plane)

    def plot_drawer(self, _):
        coordinates = next(self.coordinates_generator)
        self.x.append(coordinates[self.plane_coordinates[0]])
        self.y.append(coordinates[self.plane_coordinates[1]])
        self.axis.clear()
        self.axis.plot(self.x, self.y)


class PlotBuilder3D(BasePlotBuilder):

    def __init__(self, coordinates_generator):
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
