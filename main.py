from aruco_detection.marker_detector import MarkerDetector
from aruco_detection.plot_builder import PlotBuilder2D
from aruco_detection import config as cfg


if __name__ == "__main__":
    detector = MarkerDetector()
    plot_builder = PlotBuilder2D(detector.center_coordinates_generator, cfg.MARKER_PLANE)
    plot_builder.draw_animated_plot()
