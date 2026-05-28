import time


class FraudEngine:
    def __init__(self):
        # how long a condition must persist before we flag it
        self.absence_threshold_seconds = 2.5
        self.multi_face_threshold_seconds = 2.5
        self.phone_threshold_seconds = 2.5

        # when each condition started (None = not happening right now)
        self.no_face_start_time = None
        self.multi_face_start_time = None
        self.phone_start_time = None

        # whether each fraud type is currently confirmed (past threshold)
        self.absence_active = False
        self.multi_face_active = False
        self.phone_active = False

        self.session_start_time = time.time()

    def get_elapsed(self):
        return round(time.time() - self.session_start_time, 2)

    def analyze(self, face_count, phone_detected=False):
        """check current frame and return which fraud states just started/ended.
        returns dict with 'started', 'ended', and 'active' lists."""
        started = []
        ended = []
        active = []
        now = time.time()

        # --- no face / candidate absent ---
        if face_count == 0:
            if self.no_face_start_time is None:
                self.no_face_start_time = now
            duration = now - self.no_face_start_time
            if duration >= self.absence_threshold_seconds:
                if not self.absence_active:
                    self.absence_active = True
                    started.append("CANDIDATE ABSENT")
                active.append("CANDIDATE ABSENT")
        else:
            if self.absence_active:
                t_start = round(self.no_face_start_time - self.session_start_time, 2)
                t_end = self.get_elapsed()
                ended.append(("CANDIDATE ABSENT", t_start, t_end))
            self.no_face_start_time = None
            self.absence_active = False

        # --- multiple faces ---
        if face_count > 1:
            if self.multi_face_start_time is None:
                self.multi_face_start_time = now
            duration = now - self.multi_face_start_time
            if duration >= self.multi_face_threshold_seconds:
                if not self.multi_face_active:
                    self.multi_face_active = True
                    started.append("MULTIPLE FACES DETECTED")
                active.append("MULTIPLE FACES DETECTED")
        else:
            if self.multi_face_active:
                t_start = round(self.multi_face_start_time - self.session_start_time, 2)
                t_end = self.get_elapsed()
                ended.append(("MULTIPLE FACES DETECTED", t_start, t_end))
            self.multi_face_start_time = None
            self.multi_face_active = False

        # --- phone detection ---
        if phone_detected:
            if self.phone_start_time is None:
                self.phone_start_time = now
            duration = now - self.phone_start_time
            if duration >= self.phone_threshold_seconds:
                if not self.phone_active:
                    self.phone_active = True
                    started.append("PHONE DETECTED")
                active.append("PHONE DETECTED")
        else:
            if self.phone_active:
                t_start = round(self.phone_start_time - self.session_start_time, 2)
                t_end = self.get_elapsed()
                ended.append(("PHONE DETECTED", t_start, t_end))
            self.phone_start_time = None
            self.phone_active = False

        return {"started": started, "ended": ended, "active": active}

    def finalize(self):
        """called at shutdown to close any still-active fraud events"""
        ended = []
        now = self.get_elapsed()

        if self.absence_active and self.no_face_start_time:
            t_start = round(self.no_face_start_time - self.session_start_time, 2)
            ended.append(("CANDIDATE ABSENT", t_start, now))
            self.absence_active = False

        if self.multi_face_active and self.multi_face_start_time:
            t_start = round(self.multi_face_start_time - self.session_start_time, 2)
            ended.append(("MULTIPLE FACES DETECTED", t_start, now))
            self.multi_face_active = False

        if self.phone_active and self.phone_start_time:
            t_start = round(self.phone_start_time - self.session_start_time, 2)
            ended.append(("PHONE DETECTED", t_start, now))
            self.phone_active = False

        return ended