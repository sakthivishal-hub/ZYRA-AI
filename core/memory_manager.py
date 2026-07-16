import json
from datetime import datetime
from config import Config
import os

class MemoryManager:
    def __init__(self):
        self.preferences_file = "data/preferences.json"
        self.preferences = self.load_preferences()
    
    def load_preferences(self):
        """Load user preferences"""
        try:
            with open(self.preferences_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return self.create_default_preferences()
    
    def create_default_preferences(self):
        """Create default preferences"""
        defaults = {
            "user_name": Config.USER_NAME,
            "theme": "dark",
            "voice_enabled": Config.VOICE_ENABLED,
            "favorite_apps": [],
            "frequent_files": [],
            "custom_commands": {},
            "created_at": datetime.now().isoformat()
        }
        self.save_preferences(defaults)
        return defaults
    
    def save_preferences(self, preferences=None):
        """Save preferences to file"""
        if preferences is None:
            preferences = self.preferences
        
        with open(self.preferences_file, 'w') as f:
            json.dump(preferences, f, indent=2)
    
    def get(self, key, default=None):
        """Get preference value"""
        return self.preferences.get(key, default)
    
    def set(self, key, value):
        """Set preference value"""
        self.preferences[key] = value
        self.save_preferences()
    
    def add_favorite_app(self, app_name):
        """Add app to favorites"""
        if app_name not in self.preferences["favorite_apps"]:
            self.preferences["favorite_apps"].append(app_name)
            self.save_preferences()
    
    def add_frequent_file(self, file_path):
        """Track frequently accessed files"""
        frequent = self.preferences.get("frequent_files", [])
        
        # Add or update access count
        found = False
        for item in frequent:
            if item["path"] == file_path:
                item["count"] += 1
                item["last_access"] = datetime.now().isoformat()
                found = True
                break
        
        if not found:
            frequent.append({
                "path": file_path,
                "count": 1,
                "last_access": datetime.now().isoformat()
            })
        
        # Keep only top 20
        frequent = sorted(frequent, key=lambda x: x["count"], reverse=True)[:20]
        self.preferences["frequent_files"] = frequent
        self.save_preferences()