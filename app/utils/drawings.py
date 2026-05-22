import cv2


def draw_fps(frame, fps):

    cv2.putText(
        frame,
        f"FPS: {fps}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2,
    )


def draw_resolution(frame):

    height, width, _ = frame.shape

    text = f"Resolution: {width}x{height}"

    cv2.putText(
        frame,
        text,
        (20, 80),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 0),
        2,
    )

def draw_face_detections(frame, detections):

    for (x, y, w, h) in detections:

        cv2.rectangle(
            frame,
            (x, y),
            (x + w, y + h),
            (0, 255, 0),
            2,
        )

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

def draw_absence_timer(frame, duration):

    cv2.putText(
        frame,
        f"Absence Time: {duration:.1f}s",
        (20, 260),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 255),
        2,
    )