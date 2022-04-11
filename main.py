from aruco_detection.marker_detector import MarkerDetector
from aruco_detection.plot_builder import PlotBuilder3D


if __name__ == "__main__":
    detector = MarkerDetector()
    plot_builder = PlotBuilder3D(detector.center_coordinates_generator)
    plot_builder.draw_animated_3d_plot()
