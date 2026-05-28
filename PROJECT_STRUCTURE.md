# Project Structure

```
video-fraud-detection/
├── app/
│   ├── detectors/
│   │   ├── face_detector.py
│   │   └── phone_detector.py
│   ├── main.py
│   ├── services/
│   │   ├── fraud_engine.py
│   │   ├── fraud_logger.py
│   │   ├── stream_manager.py
│   │   ├── video_file_handler.py
│   │   └── webcam_handling.py
│   ├── utils/
│   │   ├── drawings.py
│   │   ├── fps.py
│   │   └── preprocessing.py
│   └── yolov8n.pt
├── dashboard/
│   ├── app.py
│   └── templates/
│       ├── index.html
│       ├── results.html
│       └── running.html
├── log/
│   └── fraud_log.json
├── requirements.txt
├── README.md
└── PROJECT_STRUCTURE.md
```
