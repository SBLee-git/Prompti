# backend/storage/interview_store.py
import os
import json
from datetime import datetime

SAVE_DIR = "saved_interviews"
os.makedirs(SAVE_DIR, exist_ok=True)

def save_interview_result(user_email: str, position: str, experience: str, history: list, feedback: dict):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"{user_email}_{position}_{timestamp}.json"
    full_path = os.path.join(SAVE_DIR, file_name)

    with open(full_path, "w", encoding="utf-8") as f:
        json.dump({
            "email": user_email,
            "position": position,
            "experience": experience,
            "timestamp": timestamp,
            "history": history,
            "feedback": feedback
        }, f, ensure_ascii=False, indent=2)


def load_interview_list(user_email: str):
    files = [f for f in os.listdir(SAVE_DIR) if f.startswith(user_email)]
    return sorted(files, reverse=True)


def load_interview_file(filename: str):
    with open(os.path.join(SAVE_DIR, filename), encoding="utf-8") as f:
        return json.load(f)
