import time


class FraudEngine:

    def __init__(self):

        self.absence_threshold_seconds = 2.5
        self.multi_face_threshold_seconds = 2.5
        self.phone_threshold_seconds = 2.5

        # Start times for each condition (None = not active)
        self.no_face_start_time = None
        self.multi_face_start_time = None
        self.phone_start_time = None

        # Whether each fraud type is currently "confirmed"
        # (past the threshold)
        self.absence_active = False
        self.multi_face_active = False
        self.phone_active = False

        # Session start for elapsed time calculation
        self.session_start_time = time.time()

    def get_elapsed(self):
        return round(
            time.time() - self.session_start_time, 2
        )

    def analyze(self, face_count, phone_detected=False):
        """Returns a dict of fraud states that just started
        or just ended this frame.

        Returns:
            dict with keys:
                'started': list of event types that just
                           crossed the threshold
                'ended': list of (event_type, start_elapsed,
                         end_elapsed) tuples
                'active': list of currently active fraud types
        """

        started = []
        ended = []
        active = []

        current_time = time.time()

        # --- NO FACE / ABSENCE ---

        if face_count == 0:

            if self.no_face_start_time is None:
                self.no_face_start_time = current_time

            absence_duration = (
                current_time - self.no_face_start_time
            )

            if (
                absence_duration
                >= self.absence_threshold_seconds
            ):
                if not self.absence_active:
                    self.absence_active = True
                    started.append("CANDIDATE ABSENT")

                active.append("CANDIDATE ABSENT")

        else:

            if self.absence_active:
                elapsed_start = round(
                    self.no_face_start_time
                    - self.session_start_time,
                    2,
                )
                elapsed_end = self.get_elapsed()
                ended.append(
                    (
                        "CANDIDATE ABSENT",
                        elapsed_start,
                        elapsed_end,
                    )
                )

            self.no_face_start_time = None
            self.absence_active = False

        # --- MULTIPLE FACES ---

        if face_count > 1:

            if self.multi_face_start_time is None:
                self.multi_face_start_time = current_time

            multi_duration = (
                current_time - self.multi_face_start_time
            )

            if (
                multi_duration
                >= self.multi_face_threshold_seconds
            ):
                if not self.multi_face_active:
                    self.multi_face_active = True
                    started.append(
                        "MULTIPLE FACES DETECTED"
                    )

                active.append(
                    "MULTIPLE FACES DETECTED"
                )

        else:

            if self.multi_face_active:
                elapsed_start = round(
                    self.multi_face_start_time
                    - self.session_start_time,
                    2,
                )
                elapsed_end = self.get_elapsed()
                ended.append(
                    (
                        "MULTIPLE FACES DETECTED",
                        elapsed_start,
                        elapsed_end,
                    )
                )

            self.multi_face_start_time = None
            self.multi_face_active = False

        # --- PHONE DETECTION ---

        if phone_detected:

            if self.phone_start_time is None:
                self.phone_start_time = current_time

            phone_duration = (
                current_time - self.phone_start_time
            )

            if (
                phone_duration
                >= self.phone_threshold_seconds
            ):
                if not self.phone_active:
                    self.phone_active = True
                    started.append("PHONE DETECTED")

                active.append("PHONE DETECTED")

        else:

            if self.phone_active:
                elapsed_start = round(
                    self.phone_start_time
                    - self.session_start_time,
                    2,
                )
                elapsed_end = self.get_elapsed()
                ended.append(
                    (
                        "PHONE DETECTED",
                        elapsed_start,
                        elapsed_end,
                    )
                )

            self.phone_start_time = None
            self.phone_active = False

        return {
            "started": started,
            "ended": ended,
            "active": active,
        }

    def finalize(self):
        """Called at shutdown to close any still-active
        fraud events. Returns list of
        (event_type, start_elapsed, end_elapsed) tuples."""

        ended = []
        elapsed_now = self.get_elapsed()

        if self.absence_active and self.no_face_start_time:
            elapsed_start = round(
                self.no_face_start_time
                - self.session_start_time,
                2,
            )
            ended.append(
                ("CANDIDATE ABSENT", elapsed_start, elapsed_now)
            )
            self.absence_active = False

        if self.multi_face_active and self.multi_face_start_time:
            elapsed_start = round(
                self.multi_face_start_time
                - self.session_start_time,
                2,
            )
            ended.append(
                (
                    "MULTIPLE FACES DETECTED",
                    elapsed_start,
                    elapsed_now,
                )
            )
            self.multi_face_active = False

        if self.phone_active and self.phone_start_time:
            elapsed_start = round(
                self.phone_start_time
                - self.session_start_time,
                2,
            )
            ended.append(
                ("PHONE DETECTED", elapsed_start, elapsed_now)
            )
            self.phone_active = False

        return ended