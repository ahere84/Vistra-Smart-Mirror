import os
import json
from pathlib import Path

class SettingsManager:
    _config = None
    configPath = "config.json"
    base_path = Path(os.path.dirname(os.path.abspath(__file__)))

    @staticmethod
    def load_config(path=None):
        if path is None:
            path = SettingsManager.configPath
        full_path = SettingsManager.base_path / path
        try:
            with open(full_path, 'r') as file:
                SettingsManager._config = json.load(file)
                print("Configuration loaded successfully.")
        except FileNotFoundError:
            print(f"Configuration file not found at {full_path}.")
        except json.JSONDecodeError:
            print("Failed to decode JSON from the configuration file.")

    @staticmethod
    def get_path(key):
        # Assuming key is something like "image_path/top_right"
        parts = key.split('/')
        result = SettingsManager._config
        try:
            for part in parts:
                result = result[part]
        except KeyError:
            return None  # If any part of the path is not found, return None
        if result:
            return SettingsManager.base_path / result
        return None

    
    @staticmethod
    def get_setting(key):
        if SettingsManager._config is not None and key in SettingsManager._config:
            return SettingsManager._config[key]
        return None
