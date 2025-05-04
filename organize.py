import os
import shutil

structure = {
    "backend/generator": [
        "chain.py", "interview_final.py", "retriever.py",
        "interview_retriever.py", "prompt.py", "interview_prompt.py",
        "skill_extract.py"
    ],
    "backend/api": [],
    "backend/db": [],
    "frontend/pages": [],
}

for folder, files in structure.items():
    os.makedirs(folder, exist_ok=True)
    for file in files:
        old_path = f"./{file}"
        new_path = f"./{folder}/{file}"
        if os.path.exists(old_path):
            shutil.move(old_path, new_path)
            print(f"✅ Moved {file} → {new_path}")
