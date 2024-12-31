import requests
from bs4 import BeautifulSoup
from typing import List, Dict
import json
import logging
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class NFLDataScraper:
    """Scraper for NFL game data and statistics"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.base_url = "https://api.sportsdata.io/v3/nfl"
        self.api_key = os.getenv("SPORTS_DATA_API_KEY")
        if not self.api_key:
            raise ValueError("SPORTS_DATA_API_KEY environment variable is required")
        self.headers = {
            "Ocp-Apim-Subscription-Key": self.api_key
        }
        
        # Team name mappings
        self.team_mappings = {
            "San Francisco 49ers": "SF",
            "Kansas City Chiefs": "KC",
            # Add more mappings as needed
        }
        
    def _get_team_code(self, team_name: str) -> str:
        """Convert full team name to API team code"""
        return self.team_mappings.get(team_name, team_name)
        
    def get_recent_games(self, team: str, n_games: int = 3) -> List[Dict]:
        """
        Get data from recent games for a team
        
        Args:
            team (str): Team name
            n_games (int): Number of recent games to retrieve
            
        Returns:
            List[Dict]: List of game data dictionaries
        """
        try:
            # Convert team name to API format
            team_code = self._get_team_code(team)
            
            # Get current season
            current_year = datetime.now().year
            season = current_year if datetime.now().month > 8 else current_year - 1
            
            # Get team schedule
            url = f"{self.base_url}/scores/json/Schedules/{season}"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            # Filter games for the team and sort by date
            games = response.json()
            team_games = [g for g in games if team_code in (g.get('HomeTeam'), g.get('AwayTeam')) 
                         and g.get('Status') == 'Final']
            team_games.sort(key=lambda x: x['Date'], reverse=True)
            
            # Get detailed stats for each game
            recent_games = []
            for game in team_games[:n_games]:
                game_id = game['GameKey']
                stats_url = f"{self.base_url}/stats/json/BoxScoreByGameID/{game_id}"
                stats_response = requests.get(stats_url, headers=self.headers)
                stats_response.raise_for_status()
                game_stats = stats_response.json()
                
                # Process game stats
                is_home = team_code == game['HomeTeam']
                team_stats = game_stats['HomeTeam'] if is_home else game_stats['AwayTeam']
                opponent_stats = game_stats['AwayTeam'] if is_home else game_stats['HomeTeam']
                
                recent_games.append({
                    'date': game['Date'],
                    'points_scored': team_stats['Score'],
                    'points_allowed': opponent_stats['Score'],
                    'total_yards': team_stats['TotalYards'],
                    'turnovers': team_stats['Turnovers'],
                    'third_down_conv': team_stats['ThirdDownConversions'] / team_stats['ThirdDownAttempts'] if team_stats['ThirdDownAttempts'] > 0 else 0
                })
                
            return recent_games
            
        except Exception as e:
            self.logger.error(f"Error fetching recent games: {str(e)}")
            raise
    
    def get_injury_report(self, team: str) -> List[Dict]:
        """
        Get current injury report for a team
        
        Args:
            team (str): Team name
            
        Returns:
            List[Dict]: List of injured players and their status
        """
        try:
            # Convert team name to API format
            team_code = self._get_team_code(team)
            
            url = f"{self.base_url}/stats/json/Injuries"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            injuries = response.json()
            team_injuries = [injury for injury in injuries if injury['Team'] == team_code]
            
            return [{
                'player': injury['Name'],
                'position': injury['Position'],
                'injury': injury['InjuryDescription'],
                'status': injury['Status']
            } for injury in team_injuries]
            
        except Exception as e:
            self.logger.error(f"Error fetching injury report: {str(e)}")
            raise
    
    def get_weather_forecast(self, location: str, game_date: str) -> Dict:
        """
        Get weather forecast for game location and date
        
        Args:
            location (str): Game location
            game_date (str): Date of the game
            
        Returns:
            Dict: Weather forecast data
        """
        try:
            # For now, return mock weather data until we have OpenWeather API key
            return {
                'temperature': 45,
                'conditions': 'Partly Cloudy',
                'wind_speed': 8,
                'precipitation_chance': 20
            }
            
        except Exception as e:
            self.logger.error(f"Error fetching weather forecast: {str(e)}")
            raise
