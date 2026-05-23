import time


class FraudEngine:

    def __init__(self):

        self.no_face_start_time = None

        self.absence_threshold_seconds = 2.5

    def analyze(self, face_count):

        fraud_events = []

        current_time = time.time()

        # MULTIPLE FACE DETECTION

        if face_count > 1:

            fraud_events.append(
                "MULTIPLE FACES DETECTED"
            )

        # NO FACE DETECTION

        if face_count == 0:

            if self.no_face_start_time is None:

                self.no_face_start_time = current_time

            absence_duration = (
                current_time -
                self.no_face_start_time
            )

            if (
                absence_duration >=
                self.absence_threshold_seconds
            ):

                fraud_events.append(
                    "CANDIDATE ABSENT"
                )

        else:

            self.no_face_start_time = None

        return fraud_events