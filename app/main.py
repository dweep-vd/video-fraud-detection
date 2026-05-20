from services.webcam_handling import WebcamHandler
from services.video_file_handler import VideoFileHandler
from services.stream_manager import StreamManager


USE_WEBCAM = True


def main():

    if USE_WEBCAM:

        source_handler = WebcamHandler()

        source_handler.initialize_camera()

    else:

        source_handler = VideoFileHandler(
            "data/test_video.mp4"
        )

        source_handler.initialize_video()

    stream_manager = StreamManager(source_handler)

    stream_manager.start_stream()


if __name__ == "__main__":
    main()