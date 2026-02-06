import json
import os
from typing import Dict, Any

CONFIG_FILE = "config.json"

class ConfigManager:
    def __init__(self):
        self.config: Dict[str, Any] = {
            "groq_api_key": "",
            "theme": "System",  # System, Dark, Light
            "autosave_reports": True
        }
        self.load_config()

    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r') as f:
                    data = json.load(f)
                    self.config.update(data)
            except json.JSONDecodeError:
                print("Error decoding config file. Using defaults.")

    def save_config(self):
        try:
            with open(CONFIG_FILE, 'w') as f:
                json.dump(self.config, f, indent=4)
        except IOError as e:
            print(f"Error saving config: {e}")

    def get(self, key: str, default=None):
        return self.config.get(key, default)

    def set(self, key: str, value: Any):
        self.config[key] = value
        self.save_config()
