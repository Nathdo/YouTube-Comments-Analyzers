import json
from datetime import datetime
import os

HISTORY_FILE = "history.json"

def load_history():
    if not os.path.exists(HISTORY_FILE):
        return []
    with open(HISTORY_FILE, "r") as f:
        return json.load(f)

def save_to_history(url, summary, title, thumbnail):
    history = load_history()
    entry = {
        "url": url,
        "summary": summary,
        "title": title,
        "thumbnail": thumbnail,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    history.insert(0, entry)
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)

def clear_history_file():
    if os.path.exists(HISTORY_FILE):
        os.remove(HISTORY_FILE)


