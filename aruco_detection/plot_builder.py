import matplotlib.animation as animation
import matplotlib.pyplot as plt


class PlotBuilder:

    def __init__(self, width, height, coordinates_generator) -> None:
        self.figure, self.axes = plt.subplots()
        self.width, self.height = width, height
        self.x, self.y = [], []
        self.coordinates_generator = coordinates_generator()

    def plot_drawer(self, _):
        x, y = next(self.coordinates_generator)
        self.x.append(x)
        self.y.append(y)
        self.axes.clear()
        self.axes.plot(self.x, self.y)
        self.axes.set_xlim([0, self.width])
        self.axes.set_ylim([0, self.height])

    def build_anumated_2d_plot(self):
        _ = animation.FuncAnimation(self.figure, self.plot_drawer, repeat=False)
        plt.show()
