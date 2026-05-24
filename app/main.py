import sys
import os
from services.webcam_handling import WebcamHandler
from services.video_file_handler import VideoFileHandler
from services.stream_manager import StreamManager


USE_WEBCAM = True


def main():

    source_type = "webcam"

    video_path = "data/test_video.mp4"

    # Check for command line arguments
    # Usage: python main.py webcam
    # Usage: python main.py file path/to/video.mp4

    if len(sys.argv) > 1:

        source_type = sys.argv[1]

    if len(sys.argv) > 2:

        video_path = sys.argv[2]

    if source_type == "webcam":

        source_handler = WebcamHandler()

        source_handler.initialize_camera()

    else:

        source_handler = VideoFileHandler(
            video_path
        )

        source_handler.initialize_video()

    stream_manager = StreamManager(source_handler)

    stream_manager.start_stream()


if __name__ == "__main__":
    main()
