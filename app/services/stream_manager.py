import cv2
import time
from utils.fps import FPSCounter
from utils.drawings import (draw_fps, draw_resolution, draw_face_detections,
                             draw_face_count, draw_absence_timer, draw_phone_detections)
from utils.preprocessing import resize_frame, convert_to_grayscale, apply_gaussian_blur
from detectors.face_detector import FaceDetector
from detectors.phone_detector import PhoneDetector
from services.fraud_engine import FraudEngine
from services.fraud_logger import FraudLogger


class StreamManager:
    def __init__(self, source_handler):
        self.source_handler = source_handler
        self.fps_counter = FPSCounter()
        self.face_detector = FaceDetector()
        self.phone_detector = PhoneDetector()
        self.fraud_engine = FraudEngine()
        self.fraud_logger = FraudLogger()

        # run YOLO phone detection every N frames to keep fps decent
        self.phone_detect_interval = 3
        self.frame_count = 0
        self.last_phone_detections = []

    def start_stream(self):
        print("Starting video stream...")

        while True:
            success, frame = self.source_handler.read_frame()
            if not success:
                print("Unable to retrieve frame.")
                break

            frame = resize_frame(frame)
            gray = convert_to_grayscale(frame)
            blurred = apply_gaussian_blur(gray)

            fps = self.fps_counter.get_fps()
            draw_fps(frame, fps)
            draw_resolution(frame)

            # face detection runs every frame (its fast enough)
            faces = self.face_detector.detect_faces(blurred)
            draw_face_detections(frame, faces)
            face_count = len(faces)
            draw_face_count(frame, face_count)

            # phone detection is heavy (YOLO) so skip some frames
            self.frame_count += 1
            if self.frame_count % self.phone_detect_interval == 0:
                self.last_phone_detections = self.phone_detector.detect_phones(frame)

            phone_detected = len(self.last_phone_detections) > 0
            draw_phone_detections(frame, self.last_phone_detections)

            # run fraud analysis
            result = self.fraud_engine.analyze(face_count, phone_detected=phone_detected)

            # log any fraud events that just ended
            for event_type, start_t, end_t in result["ended"]:
                self.fraud_logger.log_event(event_type, start_t, end_t)

            # show absence timer when no face visible
            if face_count == 0 and self.fraud_engine.no_face_start_time is not None:
                absence_dur = time.time() - self.fraud_engine.no_face_start_time
                draw_absence_timer(frame, absence_dur)

            # show alerts for active fraud
            alert_y = 170
            for event_type in result["active"]:
                cv2.putText(frame, f"ALERT: {event_type}", (20, alert_y),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                alert_y += 50

            cv2.imshow("AI Fraud Detection System", frame)

            if cv2.waitKey(1) == ord("q"):
                print("Exit requested by user.")
                break

        self.shutdown()

    def shutdown(self):
        # close out any fraud events that are still going
        remaining = self.fraud_engine.finalize()
        for event_type, start_t, end_t in remaining:
            self.fraud_logger.log_event(event_type, start_t, end_t)

        self.fraud_logger.save_to_file()
        self.source_handler.cleanup()