import cv2

from utils.fps import FPSCounter
from utils.drawings import draw_fps, draw_resolution
from utils.preprocessing import resize_frame,convert_to_grayscale,apply_gaussian_blur
from detectors.face_detector import FaceDetector

class StreamManager:

    def __init__(self, source_handler):

        self.source_handler = source_handler
        self.fps_counter = FPSCounter()
        self.face_detector = FaceDetector()

    def start_stream(self):

        print("Starting video stream...")

        while True:

            success, frame = self.source_handler.read_frame()

            if not success:
                print("Unable to retrieve frame.")
                break

            frame = resize_frame(frame)
            gray_frame = convert_to_grayscale(frame)

            blurred_gray_frame = apply_gaussian_blur(gray_frame) #would be useful for haar cascades but I am using mediapipe which expects RGB

            fps = self.fps_counter.get_fps()

            draw_fps(frame, fps)
            draw_resolution(frame)

            cv2.imshow("AI Fraud Detection System",frame)
            # cv2.imshow("Blurred gray Frame", blurred_gray_frame)
            
            detection_results = self.face_detector.detect_faces(blurred_gray_frame)
            print(detection_results)

            if cv2.waitKey(1) == ord('q'):
                print("Exit requested by user.")
                break

        self.shutdown()

    def shutdown(self):

        self.source_handler.cleanup()