import os
from dotenv import load_dotenv
from data_scraper import NFLDataScraper
import json

def main():
    # Initialize scraper
    scraper = NFLDataScraper()
    
    # Test recent games
    print("\nTesting recent games retrieval...")
    games = scraper.get_recent_games("Kansas City Chiefs", n_games=2)
    print(json.dumps(games, indent=2))
    
    # Test injury report
    print("\nTesting injury report retrieval...")
    injuries = scraper.get_injury_report("San Francisco 49ers")
    print(json.dumps(injuries, indent=2))
    
    # Test weather forecast
    print("\nTesting weather forecast retrieval...")
    weather = scraper.get_weather_forecast("Kansas City, MO", "2024-01-15")
    print(json.dumps(weather, indent=2))

if __name__ == "__main__":
    load_dotenv()
    main()
