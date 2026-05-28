import cv2
import time


class VideoFileHandler:
    def __init__(self, video_path):
        self.video_path = video_path
        self.cap = None
        self.retry_limit = 3
        self.retry_delay = 0.2

    def initialize_video(self):
        self.cap = cv2.VideoCapture(self.video_path)
        if not self.cap.isOpened():
            raise Exception(f"Unable to open video file: {self.video_path}")
        print("Video file initialized successfully.")

    def read_frame(self):
        retries = 0
        while retries < self.retry_limit:
            success, frame = self.cap.read()
            if success:
                return success, frame
            retries += 1
            print(f"Failed to read frame ({retries}/{self.retry_limit})")
            time.sleep(self.retry_delay)
        return False, None

    def cleanup(self):
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()
        print("Video resources released.")