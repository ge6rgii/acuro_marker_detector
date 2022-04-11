import cv2 as cv


class VideoStream:

    def __init__(self, video_path) -> None:
        self.video = cv.VideoCapture(video_path)
        self.width = self.video.get(cv.CAP_PROP_FRAME_WIDTH)
        self.height = self.video.get(cv.CAP_PROP_FRAME_HEIGHT)

    def stream_generator(self):
        while self.video.isOpened():
            _, frame = self.video.read()
            ret, frame = self.video.read()
            if not ret: break
            yield frame

        self.video.release()
        cv.destroyAllWindows()
