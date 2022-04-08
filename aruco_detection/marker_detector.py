import cv2 as cv
import numpy as np

import aruco_detection.config as cfg


class MarkerDetector:

    def __init__(self, video_path):
        self.video = cv.VideoCapture(video_path)
        self.width = self.video.get(cv.CAP_PROP_FRAME_WIDTH)
        self.height = self.video.get(cv.CAP_PROP_FRAME_HEIGHT)
        self.aruco_detector_parametrs = cv.aruco.DetectorParameters_create()

    @property
    def aruco_dictionary(self):
        aruko_markers_mapper = {
            "APRILTAG_16H5": cv.aruco.DICT_APRILTAG_16H5
        }
        return cv.aruco.Dictionary_get(aruko_markers_mapper.get(cfg.ARUCO_MARKER_TYPE))

    @staticmethod
    def extract_marker_corners(corners):
        corners = corners[0].reshape((4, 2))
        (topLeft, topRight, bottomRight, bottomLeft) = corners
        topRight = (int(topRight[0]), int(topRight[1]))
        bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
        bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
        topLeft = (int(topLeft[0]), int(topLeft[1]))
        return topRight, bottomRight, bottomLeft, topLeft

    def get_marker_center_coordinates(self, parsed_corners):
        _, bottomRight, _, topLeft = parsed_corners
        x_center = int((topLeft[0] + bottomRight[0]) / 2.0)
        y_center = int((topLeft[1] + bottomRight[1]) / 2.0)
        return x_center, y_center

    def marker_center_coordinates_generator(self):
        while self.video.isOpened():
            ret, frame = self.video.read()
            if not ret: break

            corners, _, _ = cv.aruco.detectMarkers(
                frame, self.aruco_dictionary, parameters=self.aruco_detector_parametrs
            )
            # TODO: remove me.
            # just for testing.
            yaml_data = cv.FileStorage("/Users/georgii/Code/tws_italy/cam_calib.yml", cv.FILE_STORAGE_READ)
            matrix_coefficients = np.asarray(yaml_data.getNode("K").mat())
            distortion_coefficients = np.asarray(yaml_data.getNode("D").mat())
            rvec, tvec, markerPoints = cv.aruco.estimatePoseSingleMarkers(
                corners[0], 0.01, matrix_coefficients, distortion_coefficients
            )
            a = rvec[0]
            b = tvec[0]
            cv.aruco.drawAxis(frame, matrix_coefficients, distortion_coefficients, rvec[0], tvec[0], 0.03)
            marker_corners = self.extract_marker_corners(corners)
            x_center, y_center = self.get_marker_center_coordinates(marker_corners)
            yield x_center, self.height - y_center

            cv.circle(frame, (x_center, y_center), 4, (0, 0, 255), -1)
            cv.putText(frame, f"{x_center}, {y_center}",
                (x_center, y_center - 15),
                cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2
            )

            cv.imshow('frame', frame)
            if cv.waitKey(1) == ord('q'):
                break

        self.video.release()
        cv.destroyAllWindows()


# detector = MarkerDetector("/Users/georgii/Code/tws_italy/test_videos/ArucoVideo.mp4")
# detector.marker_center_coordinates_generator()
