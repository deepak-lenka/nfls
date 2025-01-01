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
            "Arizona Cardinals": "ARI",
            "Atlanta Falcons": "ATL",
            "Baltimore Ravens": "BAL",
            "Buffalo Bills": "BUF",
            "Carolina Panthers": "CAR",
            "Chicago Bears": "CHI",
            "Cincinnati Bengals": "CIN",
            "Cleveland Browns": "CLE",
            "Dallas Cowboys": "DAL",
            "Denver Broncos": "DEN",
            "Detroit Lions": "DET",
            "Green Bay Packers": "GB",
            "Houston Texans": "HOU",
            "Indianapolis Colts": "IND",
            "Jacksonville Jaguars": "JAX",
            "Kansas City Chiefs": "KC",
            "Las Vegas Raiders": "LV",
            "Los Angeles Chargers": "LAC",
            "Los Angeles Rams": "LAR",
            "Miami Dolphins": "MIA",
            "Minnesota Vikings": "MIN",
            "New England Patriots": "NE",
            "New Orleans Saints": "NO",
            "New York Giants": "NYG",
            "New York Jets": "NYJ",
            "Philadelphia Eagles": "PHI",
            "Pittsburgh Steelers": "PIT",
            "San Francisco 49ers": "SF",
            "Seattle Seahawks": "SEA",
            "Tampa Bay Buccaneers": "TB",
            "Tennessee Titans": "TEN",
            "Washington Commanders": "WAS"
        }
        
        # Initialize cache
        self.cache = {}
        self.cache_expiry = 3600  # Cache expiry in seconds
        
    def _get_team_code(self, team_name: str) -> str:
        """Convert full team name to API team code"""
        return self.team_mappings.get(team_name, team_name)
        
    def _get_from_cache(self, key: str) -> Dict:
        """Get data from cache if available and not expired"""
        if key in self.cache:
            data, timestamp = self.cache[key]
            if datetime.now().timestamp() - timestamp < self.cache_expiry:
                return data
            del self.cache[key]
        return None

    def _set_cache(self, key: str, data: Dict):
        """Set data in cache with current timestamp"""
        self.cache[key] = (data, datetime.now().timestamp())
        
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
            # Check cache first
            cache_key = f"recent_games_{team}_{n_games}"
            cached_data = self._get_from_cache(cache_key)
            if cached_data:
                return cached_data

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
                    'opponent': opponent_stats['Team'],
                    'is_home': is_home,
                    'points_scored': team_stats['Score'],
                    'points_allowed': opponent_stats['Score'],
                    'total_yards': team_stats['TotalYards'],
                    'passing_yards': team_stats['PassingYards'],
                    'rushing_yards': team_stats['RushingYards'],
                    'turnovers': team_stats['Turnovers'],
                    'third_down_conv': team_stats['ThirdDownConversions'] / team_stats['ThirdDownAttempts'] if team_stats['ThirdDownAttempts'] > 0 else 0,
                    'fourth_down_conv': team_stats['FourthDownConversions'] / team_stats['FourthDownAttempts'] if team_stats['FourthDownAttempts'] > 0 else 0,
                    'time_of_possession': team_stats.get('TimeOfPossession', ''),
                    'sacks': team_stats.get('Sacks', 0),
                    'interceptions': team_stats.get('InterceptionReturns', 0),
                    'fumbles_lost': team_stats.get('FumblesLost', 0),
                    'penalties': team_stats.get('Penalties', 0),
                    'penalty_yards': team_stats.get('PenaltyYards', 0),
                    'red_zone_attempts': team_stats.get('RedZoneAttempts', 0),
                    'red_zone_conversions': team_stats.get('RedZoneConversions', 0)
                })
            
            # Cache the results
            self._set_cache(cache_key, recent_games)
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
        Get weather forecast for game location and date using OpenWeather API
        
        Args:
            location (str): Game location
            game_date (str): Date of the game
            
        Returns:
            Dict: Weather forecast data
        """
        try:
            # Check cache first
            cache_key = f"weather_{location}_{game_date}"
            cached_data = self._get_from_cache(cache_key)
            if cached_data:
                return cached_data

            weather_api_key = os.getenv("WEATHER_API_KEY")
            if not weather_api_key:
                raise ValueError("WEATHER_API_KEY environment variable is required")

            # Get location coordinates
            geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={location},US&limit=1&appid={weather_api_key}"
            geo_response = requests.get(geo_url)
            geo_response.raise_for_status()
            geo_data = geo_response.json()

            if not geo_data:
                raise ValueError(f"Location not found: {location}")

            lat = geo_data[0]['lat']
            lon = geo_data[0]['lon']

            # Get weather forecast
            weather_url = f"http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={weather_api_key}&units=imperial"
            weather_response = requests.get(weather_url)
            weather_response.raise_for_status()
            weather_data = weather_response.json()

            # Find forecast closest to game time
            game_datetime = datetime.strptime(game_date, "%Y-%m-%d")
            game_forecasts = [f for f in weather_data['list'] 
                            if abs((datetime.fromtimestamp(f['dt']) - game_datetime).days) < 1]

            if not game_forecasts:
                raise ValueError(f"No weather forecast available for date: {game_date}")

            forecast = game_forecasts[0]
            weather_info = {
                'temperature': round(forecast['main']['temp']),
                'feels_like': round(forecast['main']['feels_like']),
                'conditions': forecast['weather'][0]['main'],
                'description': forecast['weather'][0]['description'],
                'wind_speed': round(forecast['wind']['speed']),
                'humidity': forecast['main']['humidity'],
                'precipitation_chance': round(forecast.get('pop', 0) * 100)
            }

            # Cache the result
            self._set_cache(cache_key, weather_info)
            return weather_info

        except Exception as e:
            self.logger.error(f"Error fetching weather forecast: {str(e)}")
            raise
