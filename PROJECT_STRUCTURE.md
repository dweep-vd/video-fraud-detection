# Project Structure

```
video-fraud-detection/
├── .git/
├── .gitignore
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
│   └── utils/
│       ├── drawings.py
│       ├── fps.py
│       └── preprocessing.py
├── dashboard/
│   ├── app.py
│   └── templates/
│       └── index.html
├── log/
│   └── fraud_log.json
├── outputs/
├── README.md
├── requirements.txt
├── tests/
└── venv/
```
