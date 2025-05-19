import json
import os
import copy
import tempfile
import shutil
from typing import Any, Dict, Optional

# Default application settings
DEFAULT_SETTINGS: Dict[str, Any] = {
    "theme": "system",
    "model_name": "llama3",
    "model_settings": {
        "temperature": 0.7,
        "max_tokens": 500
    }
}

# Path to the settings file (next to this script)
SETTINGS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "settings.json")

def atomic_write(file_path: str, data: dict) -> None:
    """
    Write a JSON file atomically to prevent corruption in case of interruptions.
    """
    temp_fd, temp_path = tempfile.mkstemp(dir=os.path.dirname(file_path))
    try:
        with os.fdopen(temp_fd, 'w', encoding='utf-8') as tmp:
            json.dump(data, tmp, indent=4, ensure_ascii=False)
        shutil.move(temp_path, file_path)
    except Exception as e:
        print(f"❌ Atomic write failed: {e}")

def backup_settings_file():
    """
    Optionally backup the current settings file as .bak before overwriting.
    """
    if os.path.exists(SETTINGS_FILE):
        backup_file = SETTINGS_FILE + ".bak"
        shutil.copy2(SETTINGS_FILE, backup_file)

def load_settings(reset: bool = False) -> dict:
    """
    Load application settings from file, or create defaults if missing or reset is True.
    Auto-fills missing keys from the latest DEFAULT_SETTINGS.
    """
    if reset or not os.path.exists(SETTINGS_FILE):
        atomic_write(SETTINGS_FILE, DEFAULT_SETTINGS)
        return copy.deepcopy(DEFAULT_SETTINGS)

    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            settings = json.load(f)
        # Fill in missing keys for backward compatibility
        for key, value in DEFAULT_SETTINGS.items():
            if key not in settings:
                settings[key] = copy.deepcopy(value)
            elif isinstance(value, dict):
                for subkey, subval in value.items():
                    if subkey not in settings[key]:
                        settings[key][subkey] = subval
        return settings
    except Exception as e:
        print(f"⚠️ Error loading settings: {e}")
        backup_settings_file()
        atomic_write(SETTINGS_FILE, DEFAULT_SETTINGS)
        return copy.deepcopy(DEFAULT_SETTINGS)

def update_setting(key: str, value: Any) -> dict:
    """
    Update a single top-level setting and write to file.
    """
    settings = load_settings()
    settings[key] = value
    atomic_write(SETTINGS_FILE, settings)
    return settings

def update_model_setting(key: str, value: Any) -> dict:
    """
    Update a specific field inside model_settings and write to file.
    """
    settings = load_settings()
    if "model_settings" not in settings:
        settings["model_settings"] = {}
    settings["model_settings"][key] = value
    atomic_write(SETTINGS_FILE, settings)
    return settings

def check_ollama_installed() -> bool:
    """
    Check if Ollama is installed and available in the system PATH.
    """
    import platform
    import subprocess

    try:
        if platform.system() == "Windows":
            result = subprocess.run(["where", "ollama"], capture_output=True, text=True)
        else:
            result = subprocess.run(["which", "ollama"], capture_output=True, text=True)
        return result.stdout.strip() != ""
    except Exception:
        return False

def get_setting(key: str, default: Optional[Any] = None) -> Any:
    """
    Quickly fetch a single setting by key.
    """
    settings = load_settings()
    return settings.get(key, default)

def reset_settings_to_default() -> dict:
    """
    Reset all settings to DEFAULT_SETTINGS.
    """
    atomic_write(SETTINGS_FILE, DEFAULT_SETTINGS)
    return copy.deepcopy(DEFAULT_SETTINGS)


# If run directly, perform quick test:
if __name__ == "__main__":
    print("Active settings:", load_settings())
    print("Ollama installed?", check_ollama_installed())
