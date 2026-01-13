import json
import os
from datetime import datetime, date

DATA_FILE = "user_data.json"

class DataManager:
    def __init__(self):
        self.data_file = DATA_FILE
        self.data = self.load_data()
        self.update_visit_stats()

    def load_data(self):
        if not os.path.exists(self.data_file):
            return self.create_default_data()
        
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return self.create_default_data()

    def create_default_data(self):
        default_data = {
            "last_visit": None,
            "learning_days": 0,
            "total_questions_answered": 0,
            "correct_answers": 0,
            "history_log": [] # 将来的な拡張用
        }
        self.save_data(default_data)
        return default_data

    def save_data(self, data=None):
        if data is None:
            data = self.data
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except IOError:
            pass # ログ出力などは省略

    def update_visit_stats(self):
        today_str = date.today().isoformat()
        last_visit = self.data.get("last_visit")

        if last_visit != today_str:
            self.data["learning_days"] += 1
            self.data["last_visit"] = today_str
            self.save_data()

    def add_quiz_result(self, is_correct):
        self.data["total_questions_answered"] += 1
        if is_correct:
            self.data["correct_answers"] += 1
        self.save_data()

    def get_stats(self):
        total = self.data["total_questions_answered"]
        correct = self.data["correct_answers"]
        accuracy = (correct / total * 100) if total > 0 else 0.0
        
        return {
            "learning_days": self.data["learning_days"],
            "total_questions": total,
            "correct_answers": correct,
            "accuracy": accuracy
        }
