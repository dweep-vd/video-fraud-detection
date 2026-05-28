import time
import json
import os
from datetime import datetime


# go up two levels: services/ -> app/ -> project root
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DEFAULT_LOG_PATH = os.path.join(PROJECT_ROOT, "log", "fraud_log.json")


def format_seconds(sec):
    """turn elapsed seconds into a MM:SS string"""
    mins = int(sec) // 60
    secs = int(sec) % 60
    return f"{mins:02d}:{secs:02d}"


class FraudLogger:
    def __init__(self):
        self.events = []
        self.session_start_time = time.time()
        self.session_start_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print("Fraud logger initialized.")

    def log_event(self, event_type, start_time, end_time):
        """log a completed fraud event with its time range (in elapsed seconds)"""
        duration = round(end_time - start_time, 2)
        entry = {
            "event": event_type,
            "start_time": start_time,
            "end_time": end_time,
            "duration": duration,
            "start_time_fmt": format_seconds(start_time),
            "end_time_fmt": format_seconds(end_time),
            "duration_fmt": format_seconds(duration),
        }
        self.events.append(entry)
        print(f"[FRAUD LOG] {event_type} {start_time}s - {end_time}s (duration: {duration}s)")

    def get_events(self):
        return self.events

    def get_summary(self):
        session_duration = round(time.time() - self.session_start_time, 2)
        session_end_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        event_counts = {}
        total_durations = {}
        for ev in self.events:
            t = ev["event"]
            if t in event_counts:
                event_counts[t] += 1
                total_durations[t] += ev["duration"]
            else:
                event_counts[t] = 1
                total_durations[t] = ev["duration"]

        # round the duration totals
        for k in total_durations:
            total_durations[k] = round(total_durations[k], 2)

        summary = {
            "session_start": self.session_start_str,
            "session_end": session_end_str,
            "session_duration_seconds": session_duration,
            "session_duration_fmt": format_seconds(session_duration),
            "total_events": len(self.events),
            "event_counts": event_counts,
            "total_durations": total_durations,
        }
        return summary

    def save_to_file(self, filepath=DEFAULT_LOG_PATH):
        directory = os.path.dirname(filepath)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)

        data = {
            "summary": self.get_summary(),
            "events": self.events,
        }
        with open(filepath, "w") as f:
            json.dump(data, f, indent=4)
        print(f"Fraud log saved to {filepath}")
