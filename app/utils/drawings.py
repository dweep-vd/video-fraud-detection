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