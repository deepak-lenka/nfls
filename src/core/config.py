import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

# Agent Configuration
AGENT_CONFIG = {
    "llm_config": {
        "api_key": OPENAI_API_KEY,
        "model": "gpt-4-1106-preview",
        "temperature": 0.7,
        "max_tokens": 1500
    },
    "tools": [],  # Add any specific tools if needed
    "memory": True,
    "max_iterations": 3,
    "verbose": True
}

# Data Sources
DATA_SOURCES = {
    "fox_sports": "https://www.foxsports.com",
    "statmuse": "https://www.statmuse.com",
    "nfl_stats": "https://www.nfl.com/stats",
    "weather_api": "https://api.weatherapi.com"
}
