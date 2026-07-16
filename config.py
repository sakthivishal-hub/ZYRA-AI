import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # AI Settings
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    AI_NAME = os.getenv("AI_NAME", "ZYRA")
    USER_NAME = os.getenv("USER_NAME", "User")
    AI_MODEL = "models/gemini-flash-latest"
    
    # Voice Settings
    VOICE_ENABLED = os.getenv("VOICE_ENABLED", "true").lower() == "true"
    VOICE_RATE = 180
    VOICE_VOLUME = 0.9
    
    # Memory Settings
    MEMORY_FILE = "data/memory.json"
    MAX_MEMORY_ITEMS = 100
    
    # Paths
    DATA_DIR = "data"
    ASSETS_DIR = "assets"
    
    # System
    DEBUG_MODE = False

os.makedirs(Config.DATA_DIR, exist_ok=True)