from aruco_detection.marker_detector import MarkerDetector
from aruco_detection.plot_builder import PlotBuilder
from aruco_detection import config as cfg


if __name__ == "__main__":
    detector = MarkerDetector(cfg.VIDEO_PATH)
    plot_builder = PlotBuilder(detector.width, detector.height, detector.marker_center_coordinates_generator)
    plot_builder.build_anumated_2d_plot()
