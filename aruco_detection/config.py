from os import getenv
from dotenv import load_dotenv


load_dotenv()

ARUCO_MARKER_TYPE = getenv("ARUCO_MARKER_TYPE", "APRILTAG_16H5")
CAM_CALIBRATION_PATH = getenv("CAM_CALIBRATION_PATH", "/Users/georgii/Code/tws_italy/cam_calib.yml")
VIDEO_PATH = getenv("VIDEO_PATH", "test_videos/ArucoVideo.mp4")
MARKER_PLANE = getenv("MARKER_PLANE", "FRONT")
