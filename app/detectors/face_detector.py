import cv2


class FaceDetector:

    def __init__(self):

        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades
            + "haarcascade_frontalface_default.xml"
        )

    def detect_faces(self, frame):

        faces = self.face_cascade.detectMultiScale(
            frame,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
        )

        return faces

    def draw_face_count(frame, face_count):

        cv2.putText(
            frame,
            f"Faces: {face_count}",
            (20, 120),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
        (0, 0, 255),
        2,
    )
    