import sys
from services.webcam_handling import WebcamHandler
from services.video_file_handler import VideoFileHandler
from services.stream_manager import StreamManager


def main():
    source_type = "webcam"
    video_path = "data/test_video.mp4"

    # usage: python main.py webcam
    #        python main.py file path/to/video.mp4
    if len(sys.argv) > 1:
        source_type = sys.argv[1]
    if len(sys.argv) > 2:
        video_path = sys.argv[2]

    if source_type == "webcam":
        handler = WebcamHandler()
        handler.initialize_camera()
    else:
        handler = VideoFileHandler(video_path)
        handler.initialize_video()

    stream = StreamManager(handler)
    stream.start_stream()


if __name__ == "__main__":
    main()
