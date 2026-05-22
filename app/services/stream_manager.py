import cv2
import time
from utils.fps import FPSCounter
from utils.drawings import draw_fps, draw_resolution, draw_face_detections, draw_face_count, draw_absence_timer
from utils.preprocessing import resize_frame,convert_to_grayscale,apply_gaussian_blur
from detectors.face_detector import FaceDetector

class StreamManager:

    def __init__(self, source_handler):

        self.source_handler= source_handler
        self.fps_counter= FPSCounter()
        self.face_detector= FaceDetector()
        self.no_face_start_time= None
        self.absence_threshold_seconds=2.5

    def start_stream(self):

        print("Starting video stream...")

        while True:

            success, frame= self.source_handler.read_frame()

            if not success:
                print("Unable to retrieve frame.")
                break

            frame= resize_frame(frame)
            gray_frame= convert_to_grayscale(frame)

            blurred_gray_frame= apply_gaussian_blur(gray_frame) 

            fps= self.fps_counter.get_fps()

            draw_fps(frame, fps)
            draw_resolution(frame)

            detection_results= self.face_detector.detect_faces(gray_frame)
            draw_face_detections(frame, detection_results)
            face_count= len(detection_results)
            draw_face_count(frame, face_count)

            if face_count > 1:
                cv2.putText(frame,"ALERT: MULTIPLE FACES DETECTED",(20,170),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),3,)
            
            current_time = time.time()

            if face_count == 0:

                if self.no_face_start_time is None:

                    self.no_face_start_time = current_time
                
                absence_duration = (current_time - self.no_face_start_time)
                draw_absence_timer(frame, absence_duration)

                if absence_duration >= self.absence_threshold_seconds:
                    cv2.putText(
                        frame,
                        "ALERT: CANDIDATE ABSENT",
                        (20, 220),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0, 0, 255),
                        3,
                    )

            else:

                self.no_face_start_time = None
            
            if face_count > 0:
                self.no_face_start_time = None

            cv2.imshow("AI Fraud Detection System", frame)

            if cv2.waitKey(1) == ord('q'):
                print("Exit requested by user.")
                break

        self.shutdown()

    def shutdown(self):
        self.source_handler.cleanup()