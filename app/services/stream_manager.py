import cv2
import time
from utils.fps import FPSCounter
from utils.drawings import draw_fps, draw_resolution, draw_face_detections, draw_face_count, draw_absence_timer
from utils.preprocessing import resize_frame, convert_to_grayscale, apply_gaussian_blur
from detectors.face_detector import FaceDetector
from services.fraud_engine import FraudEngine

class StreamManager:

    def __init__(self, source_handler):

        self.source_handler = source_handler
        self.fps_counter = FPSCounter()
        self.face_detector = FaceDetector()
        self.fraud_engine = FraudEngine()

    def start_stream(self):

        print("Starting video stream...")

        while True:

            success, frame = self.source_handler.read_frame()

            if not success:
                print("Unable to retrieve frame.")
                break

            frame = resize_frame(frame)
            gray_frame = convert_to_grayscale(frame)
            blurred_gray_frame = apply_gaussian_blur(gray_frame)

            fps = self.fps_counter.get_fps()
            draw_fps(frame, fps)
            draw_resolution(frame)

            detection_results = self.face_detector.detect_faces(blurred_gray_frame)
            draw_face_detections(frame, detection_results)
            face_count = len(detection_results)
            draw_face_count(frame, face_count)

            fraud_events = self.fraud_engine.analyze(face_count)

            # Draw absence timer when no face is present
            if face_count == 0 and self.fraud_engine.no_face_start_time is not None:
                absence_duration = time.time() - self.fraud_engine.no_face_start_time
                draw_absence_timer(frame, absence_duration)

            # Overlay alerts for each fraud event
            alert_y = 170
            for event in fraud_events:
                cv2.putText(
                    frame,
                    f"ALERT: {event}",
                    (20, alert_y),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 0, 255),
                    3,
                )
                alert_y += 50

            cv2.imshow("AI Fraud Detection System", frame)

            if cv2.waitKey(1) == ord('q'):
                print("Exit requested by user.")
                break

        self.shutdown()

    def shutdown(self):
        self.source_handler.cleanup()