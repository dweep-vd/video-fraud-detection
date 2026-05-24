import time
import json
import os


# Project root is two levels up from this file
# (services/ -> app/ -> project root)

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

DEFAULT_LOG_PATH = os.path.join(
    PROJECT_ROOT, "log", "fraud_log.json"
)


class FraudLogger:

    def __init__(self):

        self.events = []

        self.session_start_time = time.time()

        self.logged_events = set()

        print("Fraud logger initialized.")

    def log_event(self, event_type):

        current_time = time.time()

        elapsed = round(
            current_time - self.session_start_time,
            2
        )

        event_entry = {
            "timestamp": elapsed,
            "event": event_type,
        }

        self.events.append(event_entry)

        print(
            f"[FRAUD LOG] {elapsed}s - {event_type}"
        )

    def get_events(self):

        return self.events

    def get_summary(self):

        session_duration = round(
            time.time() - self.session_start_time,
            2
        )

        event_counts = {}

        for event in self.events:

            event_type = event["event"]

            if event_type in event_counts:

                event_counts[event_type] += 1

            else:

                event_counts[event_type] = 1

        summary = {
            "session_duration_seconds": session_duration,
            "total_events": len(self.events),
            "event_counts": event_counts,
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

        with open(filepath, "w") as file:

            json.dump(data, file, indent=4)

        print(
            f"Fraud log saved to {filepath}"
        )
