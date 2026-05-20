import cv2
import logging
import time


logger = logging.getLogger(__name__)


class WebcamHandler:

    def __init__(self):
        self.cap = None
        self.retry_limit = 3
        self.retry_delay_seconds = 0.2

    def initialize_camera(self):
        self.cap = cv2.VideoCapture(0)

        if not self.cap.isOpened():
            raise Exception("Unable to access webcam")

    def start_stream(self):
        retry_count = 0

        while True:
            ret, frame = self.cap.read()

            if not ret:
                retry_count += 1
                logger.warning(
                    "Failed to read frame from webcam (attempt %d/%d).",
                    retry_count,
                    self.retry_limit,
                )

                if retry_count >= self.retry_limit:
                    logger.warning(
                        "Frame read failed after %d attempts. Shutting down safely.",
                        self.retry_limit,
                    )
                    break

                time.sleep(self.retry_delay_seconds)
                continue

            retry_count = 0
            cv2.imshow("Fraud Detection Webcam Feed", frame)

            if cv2.waitKey(1) == ord('q'):
                break

        self.shutdown()

    def cleanup(self):
        if self.cap:
            self.cap.release()

        cv2.destroyAllWindows()

    def shutdown(self):
        logger.info("Shutting down webcam stream safely.")
        self.cleanup()