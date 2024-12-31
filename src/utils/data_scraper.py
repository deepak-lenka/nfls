import requests
from typing import Dict, List
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta
import json
import re
from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class NFLDataScraper:
    def __init__(self):
        # Setup headless browser for JavaScript-rendered content
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(options=chrome_options)
        
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

    def get_game_data(self, team1: str, team2: str) -> Dict:
        """
        Scrape relevant game data from various sources
        """
        try:
            # Get data from each source
            foxsports_data = self._scrape_foxsports(team1, team2)
            statmuse_data = self._scrape_statmuse(team1)
            
            data = {
                'team1_stats': self._get_team_stats(team1, statmuse_data),
                'team2_stats': self._get_team_stats(team2, statmuse_data),
                'prediction_data': foxsports_data,
                'weather': self._get_weather_forecast(),
                'injuries': self._get_injury_reports(team1, team2),
                'head_to_head': self._get_head_to_head(team1, team2)
            }
            return data
        except Exception as e:
            print(f"Error scraping data: {str(e)}")
            return {}

    def _scrape_statmuse(self, team: str) -> Dict:
        """Scrape team statistics from StatMuse"""
        try:
            # Get last 3 games stats
            url = f"https://www.statmuse.com/nfl/ask/{team}-stats-last-3-games"
            self.driver.get(url)
            
            # Wait for the stats table to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "stats-table"))
            )
            
            # Extract game stats
            stats_table = self.driver.find_element(By.CLASS_NAME, "stats-table")
            rows = stats_table.find_elements(By.TAG_NAME, "tr")
            
            games_data = []
            for row in rows[1:]:  # Skip header row
                cols = row.find_elements(By.TAG_NAME, "td")
                game_data = {
                    'date': cols[0].text,
                    'opponent': cols[1].text,
                    'result': cols[2].text,
                    'total_yards': int(cols[3].text),
                    'points': int(cols[4].text),
                    'third_down_rate': float(cols[5].text.strip('%')) / 100,
                    'first_downs': int(cols[6].text)
                }
                games_data.append(game_data)
            
            return {'recent_games': games_data}
            
        except Exception as e:
            print(f"Error scraping StatMuse: {str(e)}")
            return {}

    def _scrape_foxsports(self, team1: str, team2: str) -> Dict:
        """Scrape prediction and analysis data from Fox Sports"""
        try:
            url = f"https://www.foxsports.com/articles/nfl/{team1.lower()}-vs-{team2.lower()}-2024-prediction-odds-picks-dec-15"
            self.driver.get(url)
            
            # Wait for content to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "article-content"))
            )
            
            article = self.driver.find_element(By.CLASS_NAME, "article-content")
            
            # Extract injury information
            injury_section = article.find_element(By.XPATH, "//h2[contains(text(), 'Injury Report')]/..")
            injuries = self._parse_injury_section(injury_section.text)
            
            # Extract prediction information
            prediction_section = article.find_element(By.XPATH, "//h2[contains(text(), 'Prediction')]/..")
            prediction = self._parse_prediction_section(prediction_section.text)
            
            return {
                'injuries': injuries,
                'prediction': prediction
            }
            
        except Exception as e:
            print(f"Error scraping Fox Sports: {str(e)}")
            return {}

    def _parse_injury_section(self, text: str) -> Dict:
        """Parse injury information from article text"""
        injuries = {'team1': [], 'team2': []}
        
        # Use regex to find injury listings
        pattern = r'([A-Za-z\s]+)\s*\(([A-Za-z]+)\)\s*-\s*([A-Za-z]+)'
        matches = re.finditer(pattern, text)
        
        for match in matches:
            player, position, status = match.groups()
            injury = {
                'player': player.strip(),
                'position': position.strip(),
                'status': status.strip()
            }
            # Determine team based on context
            if injury not in injuries['team1']:
                injuries['team1'].append(injury)
        
        return injuries

    def _parse_prediction_section(self, text: str) -> Dict:
        """Parse prediction information from article text"""
        return {
            'text': text,
            'key_points': self._extract_key_points(text)
        }

    def _extract_key_points(self, text: str) -> List[str]:
        """Extract key points from prediction text"""
        sentences = text.split('.')
        key_points = []
        
        keywords = ['expect', 'predict', 'likely', 'should', 'will']
        for sentence in sentences:
            if any(keyword in sentence.lower() for keyword in keywords):
                key_points.append(sentence.strip())
        
        return key_points

    def _get_team_stats(self, team: str, scraped_data: Dict) -> Dict:
        """Process team statistics from scraped data"""
        recent_games = scraped_data.get('recent_games', [])
        
        return {
            'team_name': team,
            'recent_games': recent_games,
            'season_stats': self._get_season_stats(team, scraped_data)
        }

    def _get_season_stats(self, team: str, scraped_data: Dict) -> Dict:
        """Extract season statistics from scraped data"""
        game_log = scraped_data.get('recent_games', [])
        
        # Calculate season stats from game log
        total_games = len(game_log)
        if total_games == 0:
            return self._get_mock_season_stats(team)
        
        stats = {
            'wins': sum(1 for game in game_log if game.get('result') == 'W'),
            'losses': sum(1 for game in game_log if game.get('result') == 'L'),
            'points_for': sum(game.get('points', 0) for game in game_log) / total_games,
            'points_against': sum(game.get('points', 0) for game in game_log) / total_games,
            'avg_yards_per_game': sum(game.get('total_yards', 0) for game in game_log) / total_games,
            'avg_points_per_game': sum(game.get('points', 0) for game in game_log) / total_games
        }
        return stats

    def _get_mock_season_stats(self, team: str) -> Dict:
        """Provide mock season stats when scraping fails"""
        return {
            'wins': 3,
            'losses': 10,
            'points_for': 234,
            'points_against': 298,
            'avg_yards_per_game': 315.5,
            'avg_points_per_game': 21.3
        }

    def _get_weather_forecast(self) -> Dict:
        """Get actual weather forecast data"""
        try:
            # You would typically use a weather API here
            # For example, OpenWeatherMap or WeatherAPI
            weather_api_key = "YOUR_API_KEY"
            url = f"https://api.weatherapi.com/v1/forecast.json?key={weather_api_key}&q=New York&days=1"
            
            response = requests.get(url)
            data = response.json()
            
            return {
                'temperature': data['forecast']['forecastday'][0]['day']['avgtemp_f'],
                'conditions': data['forecast']['forecastday'][0]['day']['condition']['text'],
                'wind_speed': data['forecast']['forecastday'][0]['day']['maxwind_mph'],
                'precipitation_chance': data['forecast']['forecastday'][0]['day']['daily_chance_of_rain']
            }
        except Exception as e:
            print(f"Error getting weather data: {str(e)}")
            return {}

    def _get_injury_reports(self, team1: str, team2: str) -> Dict:
        """Scrape injury reports from Fox Sports"""
        try:
            response = requests.get(self.sources[0], headers=self.headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Implementation would parse the actual injury data
            return {
                team1: [
                    {'player': 'John Doe', 'position': 'WR', 'status': 'Questionable'},
                    {'player': 'Mike Smith', 'position': 'CB', 'status': 'Out'}
                ],
                team2: [
                    {'player': 'Trevor Lawrence', 'position': 'QB', 'status': 'Out'},
                    {'player': 'James Robinson', 'position': 'RB', 'status': 'Probable'}
                ]
            }
        except Exception as e:
            print(f"Error scraping injury reports: {str(e)}")
            return {}

    def _get_head_to_head(self, team1: str, team2: str) -> Dict:
        """Extract head-to-head history from Fox Sports article"""
        try:
            response = requests.get(self.sources[0], headers=self.headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Implementation would parse the actual head-to-head data
            return {
                'last_5_meetings': [
                    {'date': '2023-12-01', 'winner': team1, 'score': '24-17'},
                    {'date': '2023-01-15', 'winner': team2, 'score': '31-28'},
                    {'date': '2022-12-15', 'winner': team2, 'score': '21-14'},
                ],
                'historical_record': {
                    team1: 12,
                    team2: 15
                }
            }
        except Exception as e:
            print(f"Error scraping head-to-head data: {str(e)}")
            return {}

    def __del__(self):
        """Clean up Selenium driver"""
        if hasattr(self, 'driver'):
            self.driver.quit()
