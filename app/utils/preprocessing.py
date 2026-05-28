import cv2


def resize_frame(frame, width=640, height=480):
    return cv2.resize(frame, (width, height))


def convert_to_grayscale(frame):
    return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


def apply_gaussian_blur(frame):
    return cv2.GaussianBlur(frame, (5, 5), 0)