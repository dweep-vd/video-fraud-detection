# AI-Powered Fraud Detection System

A computer vision-based fraud detection application that monitors video feeds (webcam or recorded) to identify suspicious activity in real-time. Built for online exam proctoring, identity verification, and monitoring systems.

---

## Features

| Detection Module | Description |
|---|---|
| **Multiple Faces** | Flags when more than one person appears in frame |
| **Candidate Absence** | Alerts when no face is detected for 2.5+ seconds |
| **Mobile Phone Usage** | Detects cell phones using YOLOv8 object detection |

Additional features:
- Real-time FPS and resolution overlay
- Timestamped fraud event logging (saved as JSON)
- Flask-based dashboard for reviewing session results

---

## Project Structure

```
video-fraud-detection/
├── app/
│   ├── main.py                     # Entry point
│   ├── detectors/
│   │   ├── face_detector.py        # Haar cascade face detection
│   │   └── phone_detector.py       # Phone detection (YOLOv8)
│   ├── services/
│   │   ├── stream_manager.py       # Main video loop and orchestration
│   │   ├── fraud_engine.py         # Fraud event analysis logic
│   │   ├── fraud_logger.py         # Event logging and JSON export
│   │   ├── video_file_handler.py   # Video file input handler
│   │   └── webcam_handling.py      # Webcam input handler
│   └── utils/
│       ├── drawings.py             # All HUD/overlay drawing functions
│       ├── fps.py                  # FPS counter utility
│       └── preprocessing.py        # Frame resize, grayscale, blur
├── dashboard/
│   ├── app.py                      # Flask dashboard server
│   └── templates/
│       └── index.html              # Dashboard HTML template
├── log/
│   └── fraud_log.json              # Auto-generated session log
├── outputs/
├── tests/
├── requirements.txt
└── README.md
```

---

## Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Webcam (for live detection) OR a test video file

### Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd video-fraud-detection
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS/Linux
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

> **Note:** On the first run, YOLOv8 will auto-download the `yolov8n.pt` model (~6 MB). This requires an internet connection.

---

## How to Run

### Detection System

```bash
cd app
python main.py
```

- Press **q** to quit. The fraud log is saved automatically on exit.
- To use a video file instead of webcam, edit `main.py` and set `USE_WEBCAM = False`.

### Dashboard

After running a detection session:

```bash
python dashboard/app.py
```

Open `http://localhost:5000` in your browser to view the fraud event summary and log.

---

## Architecture

```
┌─────────────┐    ┌──────────────────┐    ┌──────────────┐
│ Source       │───>│ Stream Manager   │───>│ Display      │
│ (Webcam/    │    │ (orchestrator)   │    │ (cv2 window) │
│  Video)     │    └────────┬─────────┘    └──────────────┘
└─────────────┘             │
                   ┌────────┴─────────┐
                   │                  │
          ┌────────▼────────┐  ┌──────▼───────┐
          │ Detectors       │  │ Services     │
          │ - FaceDetector  │  │ - FraudEngine│
          │ - PhoneDetector │  │ - FraudLogger│
          └─────────────────┘  └──────────────┘
```

**Data flow per frame:**

1. Source handler reads a frame
2. Preprocessing: resize → grayscale → Gaussian blur
3. Face detection (Haar cascade on blurred grayscale)
4. Phone detection (YOLOv8 on color frame)
5. Fraud engine analyzes all results → returns fraud events
6. Fraud logger records any events with timestamps
7. Drawing utilities render overlays on the frame
8. Frame displayed via OpenCV window

---

## Datasets and Resources Used

| Resource | Usage |
|---|---|
| OpenCV Haar Cascades | Face detection (`haarcascade_frontalface_default.xml`) |
| YOLOv8n (Ultralytics) | Phone detection — pretrained on COCO dataset (class: "cell phone") |
| COCO Dataset | YOLOv8 was pretrained on 80-class COCO; we filter for class 67 (cell phone) |

---

## Model Comparison

| Task | Model Used | Alternative Considered | Why This Choice |
|---|---|---|---|
| Face Detection | Haar Cascade | MediaPipe, dlib HOG | Simplest to understand, no extra dependencies, fast |
| Phone Detection | YOLOv8n | Haar cascade for phones | YOLOv8n is accurate, fast, and pre-trained on COCO |

---

## Challenges Faced

1. **Haar cascade sensitivity** — The cascade can be noisy with certain lighting. Gaussian blur on the grayscale frame helps reduce false positives.

2. **YOLO confidence tuning** — The default confidence for phone detection needed to be set at 0.5 to balance between false positives and missed detections.

3. **Event flooding** — Without deduplication, the logger records the same event every frame. In production, a cooldown timer per event type would reduce log noise.

---

## Future Improvements

- **Identity verification** — Compare live face with a registered photo using face_recognition
- **Head pose estimation** — Detect if the candidate is looking away using MediaPipe face mesh landmarks
- **Face spoofing detection** — Use liveness checks (eye blink detection, texture analysis) to detect photo/video attacks
- **Fraud scoring** — Assign Low/Medium/High risk based on event frequency and severity
- **Event deduplication** — Add cooldown timers to avoid logging the same event every frame
- **GPU acceleration** — Use CUDA-enabled builds for faster inference
- **Multi-camera support** — Monitor multiple video feeds simultaneously
- **Database storage** — Replace JSON logging with SQLite or PostgreSQL for multi-session history
- **Notification system** — Send email/SMS alerts for high-severity fraud events

---

## Tech Stack

- **Python 3.8+**
- **OpenCV** — Video capture, frame processing, display
- **Ultralytics YOLOv8** — Object detection (phone)
- **Flask** — Dashboard web server
- **NumPy** — Array operations