import cv2
import time


class WebcamHandler:
    def __init__(self):
        self.cap = None
        self.retry_limit = 3
        self.retry_delay = 0.2

    def initialize_camera(self):
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            raise Exception("Unable to access webcam")
        print("Webcam initialized successfully.")

    def read_frame(self):
        retries = 0
        while retries < self.retry_limit:
            success, frame = self.cap.read()
            if success:
                frame = cv2.flip(frame, 1)
                return success, frame
            retries += 1
            print(f"Failed to read frame ({retries}/{self.retry_limit})")
            time.sleep(self.retry_delay)
        return False, None

    def cleanup(self):
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()
        print("Webcam resources released.")