import os
import json
from datetime import datetime


class RunLogger:
    def __init__(self, logs_dir="logs"):
        self.logs_dir = logs_dir
        os.makedirs(self.logs_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
        self.log_file_path = os.path.join(self.logs_dir, f"log_{timestamp}.json")

        self.events = []  # Accumulate structured logs in memory first

    def log_event(self, event_type: str, payload: dict):
        event = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "payload": payload
        }
        self.events.append(event)
        self._flush()

    def _flush(self):
        with open(self.log_file_path, "w") as f:
            json.dump(self.events, f, indent=2)
