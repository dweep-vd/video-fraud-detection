from ultralytics import YOLO


class PhoneDetector:
    def __init__(self):
        self.model = YOLO("yolov8n.pt")
        self.phone_class_name = "cell phone"
        self.confidence_threshold = 0.5
        print("Phone detector loaded.")

    def detect_phones(self, frame):
        results = self.model(frame, verbose=False)
        phone_detections = []

        for result in results:
            for box in result.boxes:
                class_id = int(box.cls[0])
                class_name = self.model.names[class_id]
                confidence = float(box.conf[0])

                if (class_name == self.phone_class_name
                        and confidence >= self.confidence_threshold):
                    x1, y1, x2, y2 = box.xyxy[0]
                    phone_detections.append((
                        int(x1), int(y1), int(x2), int(y2), confidence
                    ))

        return phone_detections
