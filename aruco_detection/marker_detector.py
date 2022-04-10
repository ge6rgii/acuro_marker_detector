import cv2 as cv
import numpy as np

import aruco_detection.config as cfg
import numpy as np


class MarkerDetector:

    def __init__(self, video_path):
        self.video = cv.VideoCapture(video_path)
        self.width = self.video.get(cv.CAP_PROP_FRAME_WIDTH)
        self.height = self.video.get(cv.CAP_PROP_FRAME_HEIGHT)
        self.aruco_detector_parametrs = cv.aruco.DetectorParameters_create()
        self.cam_calibration = cv.FileStorage(cfg.CAM_CALIBRATION_PATH, cv.FILE_STORAGE_READ)
        self.matrix_coefficients = np.asarray(self.cam_calibration.getNode("K").mat())
        self.distortion_coefficients = np.asarray(self.cam_calibration.getNode("D").mat())
        self.rvec = np.array([])
        self.tvec = np.array([])

    @property
    def aruco_dictionary(self):
        aruko_markers_mapper = {
            "APRILTAG_16H5": cv.aruco.DICT_APRILTAG_16H5
        }
        return cv.aruco.Dictionary_get(aruko_markers_mapper.get(cfg.ARUCO_MARKER_TYPE))

    @property
    def use_extraction_guess(self):
        return bool(self.tvec.size and self.rvec.size)

    @staticmethod
    def extract_marker_corners(corners):
        corners = corners[0].reshape((4, 2))
        (topLeft, topRight, bottomRight, bottomLeft) = corners
        topRight = (int(topRight[0]), int(topRight[1]))
        bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
        bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
        topLeft = (int(topLeft[0]), int(topLeft[1]))
        return topRight, bottomRight, bottomLeft, topLeft

    @staticmethod
    def inversePerspective(rvec, tvec):
        R, _ = cv.Rodrigues(rvec)
        R = np.matrix(R).T
        invTvec = np.dot(R, np.matrix(-tvec))
        invRvec, _ = cv.Rodrigues(R)
        return invRvec, invTvec

    @staticmethod
    def get_marker_center_coordinates(parsed_corners):
        _, bottomRight, _, topLeft = parsed_corners
        x_center = int((topLeft[0] + bottomRight[0]) / 2.0)
        y_center = int((topLeft[1] + bottomRight[1]) / 2.0)
        return x_center, y_center

    def draw_axis(self, frame, imgpts):
        axis = np.float32([[0,0,0], [3,0,0], [0,3,0], [0,0,3]])
        imgpts, _ = cv.projectPoints(
            axis, self.rvec, self.tvec, self.matrix_coefficients, self.distortion_coefficients
        )
        imgpts = imgpts.astype(int).reshape(4, 2)

        frame = cv.line(frame, imgpts[0], imgpts[1], (0,0,255), 5)
        frame = cv.line(frame, imgpts[0], imgpts[2], (0,255,0), 5)
        frame = cv.line(frame, imgpts[0], imgpts[3], (255,0,0), 5)

        return frame

    def marker_center_coordinates_generator(self):
        # TODO: split this madness into separate methods.
        # TODO: a lot of staticmethods means that something goes wrong.
        while self.video.isOpened():
            ret, frame = self.video.read()
            if not ret: break

            corners, _, _ = cv.aruco.detectMarkers(
                frame, self.aruco_dictionary, parameters=self.aruco_detector_parametrs
            )
            marker_corners = self.extract_marker_corners(corners)
            x_center, y_center = self.get_marker_center_coordinates(marker_corners)

            object_points = np.array([(-1, 1, 0.0),(1, 1, 0.0), (1, -1, 0.0),(-1, -1, 0.0)])
            _, self.rvec, self.tvec = cv.solvePnP(
                objectPoints=object_points,
                imagePoints=corners[0],
                cameraMatrix=self.matrix_coefficients,
                distCoeffs=self.distortion_coefficients,
                flags=cv.SOLVEPNP_ITERATIVE,
                useExtrinsicGuess=self.use_extraction_guess,
                rvec=self.rvec,
                tvec=self.tvec,
            )

            axis = np.float32([[0,0,0], [3,0,0], [0,3,0], [0,0,3]])
            imgpts, _ = cv.projectPoints(axis, self.rvec, self.tvec, self.matrix_coefficients, self.distortion_coefficients)
            imgpts = imgpts.astype(int).reshape(4, 2)
            yield self.tvec[0][0], self.tvec[1][0] * -1, self.tvec[2][0]

            # TODO: move me somewhere else.
            frame = self.draw_axis(frame, imgpts)
            cv.circle(frame, (x_center, y_center), 4, (0, 0, 255), -1)
            cv.imshow('frame', frame)
            if cv.waitKey(1) == ord('q'):
                break

        self.video.release()
        cv.destroyAllWindows()
