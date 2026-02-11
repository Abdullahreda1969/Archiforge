import os
import yaml
from pathlib import Path

# الشعار الذي يظهر في بداية البرنامج
LOGO = r"""
    _              _     _  __                        
   / \   _ __ ___| |__ (_)/ _| ___  _ __ __ _  ___ 
  / _ \ | '__/ __| '_ \| | |_ / _ \| '__/ _` |/ _ \
 / ___ \| | | (__| | | | |  _| (_) | | | (_| |  __/
/_/   \_\_|  \___|_| |_|_|_|  \___/|_|  \__, |\___|
                                        |___/      
        --- Build your future, folder by folder ---
"""

CONFIG_PATH = Path.home() / ".archiforge_config.yaml"

def get_config():
    if not CONFIG_PATH.exists():
        return {}
    with open(CONFIG_PATH, "r") as f:
        return yaml.safe_load(f) or {}

def save_config(config_data):
    existing_config = get_config()
    existing_config.update(config_data)
    with open(CONFIG_PATH, "w") as f:
        yaml.safe_dump(existing_config, f)