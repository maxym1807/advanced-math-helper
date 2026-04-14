import json
from datetime import datetime
import os

class HistoryManager:
    def __init__(self, filename="data/history.json"):
        self.filename = filename
        self.ensure_data_folder()
        self.history = self.load_history()

    def ensure_data_folder(self):
        if not os.path.exists("data"):
            os.makedirs("data")

    def load_history(self):
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []

    def save_to_history(self, solution: str):
        entry = {
            "date": datetime.now().strftime("%d.%m.%Y %H:%M"),
            "solution": solution
        }
        self.history.append(entry)

        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(self.history, f, ensure_ascii=False, indent=2)

    def get_last_entries(self, count=15):
        return list(reversed(self.history[-count:]))

    def clear_history(self):
        self.history = []
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump([], f)
