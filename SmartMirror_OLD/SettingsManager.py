import json
from pathlib import Path

class SettingsManager:
    _config = None  # This will store the configuration data
    configPath = "config.json"
    loaded = False

    @staticmethod
    def load_config(path):
        try:
            with open(path, 'r') as file:
                SettingsManager._config = json.load(file)
            print("Configuration loaded successfully.")
        except FileNotFoundError:
            print(f"Configuration file not found at {path}.")
        except json.JSONDecodeError:
            print("Failed to decode JSON from the configuration file.")

    @staticmethod
    def get_setting(key):
        if not SettingsManager.loaded: 
            SettingsManager.load_config(SettingsManager.configPath)
            SettingsManager.loaded = True
        try:
            return SettingsManager._config[key]
        except KeyError:
            print(f"Setting '{key}' not found in the configuration.")
            return None
        except TypeError:
            print("Configuration not loaded.")
            return None
        
    @staticmethod
    def get_path(key):
        return Path(SettingsManager.get_setting(key))
