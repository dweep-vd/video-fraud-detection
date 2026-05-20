import cv2

from utils.fps import FPSCounter


class StreamManager:

    def __init__(self, source_handler):

        self.source_handler = source_handler
        self.fps_counter = FPSCounter()

    def start_stream(self):

        print("Starting video stream...")

        while True:

            success, frame = self.source_handler.read_frame()

            if not success:
                print("Unable to retrieve frame.")
                break

            frame = cv2.resize(frame, (640, 480))

            fps = self.fps_counter.get_fps()

            cv2.putText(
                frame,
                f"FPS: {fps}",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2,
            )

            cv2.imshow(
                "AI Fraud Detection System",
                frame,
            )

            if cv2.waitKey(1) == ord('q'):
                print("Exit requested by user.")
                break

        self.shutdown()

    def shutdown(self):

        self.source_handler.cleanup()