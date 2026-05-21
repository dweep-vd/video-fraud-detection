import cv2


def resize_frame(frame, width=640, height=480):

    resized_frame = cv2.resize(
        frame,
        (width, height)
    )

    return resized_frame


def convert_to_grayscale(frame):

    gray_frame = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2GRAY
    )

    return gray_frame


def apply_gaussian_blur(frame):

    blurred_frame = cv2.GaussianBlur(
        frame,
        (5, 5),
        0
    )

    return blurred_frame