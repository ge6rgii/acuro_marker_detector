from os import getenv
from dotenv import load_dotenv


load_dotenv()

ARUCO_MARKER_TYPE = getenv("ARUCO_MARKER_TYPE", "APRILTAG_16H5")
VIDEO_PATH = getenv("VIDEO_PATH", "/Users/georgii/Documents/ArucoVideo.mp4")
