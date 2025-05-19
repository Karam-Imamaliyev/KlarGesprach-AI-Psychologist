import json
from pathlib import Path
from datetime import datetime
from typing import Literal

# Conversation log file path
LOG_FILE = Path("data/logs.json")
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

# if there is no doc mkdir
if not LOG_FILE.exists():
    LOG_FILE.write_text("[]", encoding="utf-8")

def log_conversation(user_message: str, bot_response: str, source: Literal["user"] = "user") -> None:
    """
    Saves a conversation entry to the logs.json file.
    Each entry contains timestamp, input, and response.
    """
    entry = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "source": source,
        "user_message": user_message.strip(),
        "bot_response": bot_response.strip()
    }

    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        data = []

    data.append(entry)

    try:
        with open(LOG_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"❌ Failed to write to logs.json: {e}")