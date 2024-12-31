from crewai import Agent
from typing import Dict, List
from src.utils.data_scraper import NFLDataScraper
from pydantic import Field, ConfigDict

class WeatherAnalysisAgent(Agent):
    """Agent for analyzing weather impact on game performance"""
    
    model_config = ConfigDict(arbitrary_types_allowed=True)
    data_scraper: NFLDataScraper = Field(default_factory=NFLDataScraper)
    
    def __init__(self):
        super().__init__(
            name="Weather Impact Analyst",
            role="Meteorologist specializing in sports weather analysis and its effects on game outcomes",
            goal="Analyze weather conditions and their impact on game strategy",
            backstory="Expert meteorologist with 15+ years experience analyzing weather patterns and their effects on NFL games",
            allow_delegation=False
        )
    
    def analyze_weather_impact(self, location: str, game_date: str) -> Dict:
        """
        Analyze weather impact for a game
        
        Args:
            location (str): Game location
            game_date (str): Date of the game
            
        Returns:
            Dict: Weather analysis results
        """
        # Get weather forecast
        weather = self.data_scraper.get_weather_forecast(location, game_date)
        
        # Get historical weather data
        historical_weather = self.data_scraper.get_historical_weather(location, game_date)
        
        # Analyze conditions
        condition_impact = self._analyze_conditions(weather)
        
        # Calculate strategy adjustments
        strategy_adjustments = self._calculate_strategy_adjustments(weather)
        
        # Analyze historical patterns
        historical_analysis = self._analyze_historical_patterns(historical_weather)
        
        # Get field condition impact
        field_impact = self._analyze_field_conditions(weather)
        
        return {
            'location': location,
            'game_date': game_date,
            'weather_conditions': weather,
            'condition_impact': condition_impact,
            'strategy_adjustments': strategy_adjustments,
            'historical_analysis': historical_analysis,
            'field_conditions': field_impact,
            'overall_impact_score': self._calculate_impact_score(weather, field_impact)
        }
    
    def _analyze_conditions(self, weather: Dict) -> Dict:
        """Analyze impact of weather conditions"""
        impacts = {
            'passing_game': self._assess_passing_impact(weather),
            'running_game': self._assess_running_impact(weather),
            'kicking_game': self._assess_kicking_impact(weather),
            'visibility': self._assess_visibility_impact(weather),
            'player_comfort': self._assess_player_comfort(weather)
        }
        
        return impacts
    
    def _calculate_strategy_adjustments(self, weather: Dict) -> Dict:
        """Calculate recommended strategy adjustments"""
        adjustments = {
            'offensive_adjustments': [],
            'defensive_adjustments': [],
            'special_teams_adjustments': []
        }
        
        # Temperature adjustments
        if weather['temperature'] < 32:
            adjustments['offensive_adjustments'].append('Increase run plays')
            adjustments['offensive_adjustments'].append('Short, quick passes')
            adjustments['defensive_adjustments'].append('Focus on run defense')
        elif weather['temperature'] > 90:
            adjustments['offensive_adjustments'].append('Rotate players frequently')
            adjustments['defensive_adjustments'].append('Rotate defensive line')
        
        # Wind adjustments
        if weather['wind_speed'] > 15:
            adjustments['offensive_adjustments'].append('Adjust passing trajectories')
            adjustments['special_teams_adjustments'].append('Adjust kick directions')
            adjustments['special_teams_adjustments'].append('Conservative punt strategy')
        
        # Precipitation adjustments
        if weather['precipitation_type'] in ['rain', 'snow']:
            adjustments['offensive_adjustments'].append('Ball security emphasis')
            adjustments['defensive_adjustments'].append('Aggressive strip attempts')
            adjustments['special_teams_adjustments'].append('Fair catch emphasis')
        
        return adjustments
    
    def _analyze_historical_patterns(self, historical_data: List[Dict]) -> Dict:
        """Analyze historical weather patterns"""
        if not historical_data:
            return {
                'similar_conditions': False,
                'past_impacts': [],
                'notable_games': []
            }
        
        similar_games = []
        impacts = []
        
        for game in historical_data:
            if self._conditions_are_similar(game):
                similar_games.append(game)
                impacts.extend(game['observed_impacts'])
        
        return {
            'similar_conditions': len(similar_games) > 0,
            'past_impacts': list(set(impacts)),
            'notable_games': self._extract_notable_games(similar_games)
        }
    
    def _analyze_field_conditions(self, weather: Dict) -> Dict:
        """Analyze impact on field conditions"""
        field_impact = {
            'traction': self._assess_traction_impact(weather),
            'ball_bounce': self._assess_ball_bounce_impact(weather),
            'field_visibility': self._assess_field_visibility(weather)
        }
        
        # Calculate overall field condition score
        scores = {
            'good': 1.0,
            'moderate': 0.6,
            'poor': 0.3,
            'severe': 0.0
        }
        
        total_score = sum(scores[impact] for impact in field_impact.values())
        field_impact['overall_condition'] = total_score / len(field_impact)
        
        return field_impact
    
    def _assess_passing_impact(self, weather: Dict) -> Dict:
        """Assess impact on passing game"""
        impact = {'level': 'minimal', 'factors': []}
        
        if weather['wind_speed'] > 20:
            impact['level'] = 'severe'
            impact['factors'].append('high winds affecting ball trajectory')
        elif weather['wind_speed'] > 15:
            impact['level'] = 'moderate'
            impact['factors'].append('moderate wind impact')
            
        if weather['precipitation_type'] in ['rain', 'snow']:
            impact['level'] = 'significant'
            impact['factors'].append(f'{weather["precipitation_type"]} affecting ball grip')
            
        return impact
    
    def _assess_running_impact(self, weather: Dict) -> Dict:
        """Assess impact on running game"""
        impact = {'level': 'minimal', 'factors': []}
        
        if weather['precipitation_type'] in ['rain', 'snow']:
            impact['level'] = 'moderate'
            impact['factors'].append('reduced traction')
            
        if weather['temperature'] < 32:
            impact['level'] = 'moderate'
            impact['factors'].append('frozen field conditions')
            
        return impact
    
    def _assess_kicking_impact(self, weather: Dict) -> Dict:
        """Assess impact on kicking game"""
        impact = {'level': 'minimal', 'factors': []}
        
        if weather['wind_speed'] > 15:
            impact['level'] = 'significant'
            impact['factors'].append('wind affecting kick trajectory')
            
        if weather['precipitation_type'] in ['rain', 'snow']:
            impact['level'] = 'moderate'
            impact['factors'].append('reduced ball control')
            
        return impact
    
    def _assess_visibility_impact(self, weather: Dict) -> str:
        """Assess impact on visibility"""
        if weather.get('fog', False):
            return 'severe'
        if weather['precipitation_type'] == 'snow':
            return 'significant'
        if weather['precipitation_type'] == 'rain' and weather['precipitation_intensity'] > 0.3:
            return 'moderate'
        return 'minimal'
    
    def _assess_player_comfort(self, weather: Dict) -> str:
        """Assess impact on player comfort"""
        if weather['temperature'] < 20 or weather['temperature'] > 95:
            return 'severe'
        if weather['temperature'] < 32 or weather['temperature'] > 85:
            return 'moderate'
        if weather['wind_chill'] < 30:
            return 'significant'
        return 'minimal'
    
    def _assess_traction_impact(self, weather: Dict) -> str:
        """Assess impact on field traction"""
        if weather['precipitation_type'] == 'snow':
            return 'severe'
        if weather['precipitation_type'] == 'rain' and weather['precipitation_intensity'] > 0.3:
            return 'poor'
        if weather['precipitation_type'] == 'rain':
            return 'moderate'
        return 'good'
    
    def _assess_ball_bounce_impact(self, weather: Dict) -> str:
        """Assess impact on ball bounce"""
        if weather['precipitation_type'] in ['rain', 'snow']:
            return 'poor'
        if weather.get('field_condition') == 'wet':
            return 'moderate'
        return 'good'
    
    def _assess_field_visibility(self, weather: Dict) -> str:
        """Assess impact on field visibility"""
        if weather.get('fog', False):
            return 'severe'
        if weather['precipitation_type'] == 'snow':
            return 'poor'
        if weather['precipitation_type'] == 'rain' and weather['precipitation_intensity'] > 0.3:
            return 'moderate'
        return 'good'
    
    def _calculate_impact_score(self, weather: Dict, field_impact: Dict) -> float:
        """Calculate overall weather impact score (0-1, higher = more impact)"""
        score = 0.0
        weights = {
            'wind': 0.3,
            'precipitation': 0.25,
            'temperature': 0.2,
            'field': 0.25
        }
        
        # Wind impact
        wind_score = min(weather['wind_speed'] / 25.0, 1.0)
        score += wind_score * weights['wind']
        
        # Precipitation impact
        precip_scores = {'none': 0.0, 'rain': 0.7, 'snow': 1.0}
        score += precip_scores.get(weather['precipitation_type'], 0.0) * weights['precipitation']
        
        # Temperature impact
        temp = weather['temperature']
        if temp < 32:
            temp_score = (32 - temp) / 32.0
        elif temp > 85:
            temp_score = (temp - 85) / 15.0
        else:
            temp_score = 0.0
        score += min(temp_score, 1.0) * weights['temperature']
        
        # Field condition impact
        score += (1 - field_impact['overall_condition']) * weights['field']
        
        return min(score, 1.0)
    
    def _conditions_are_similar(self, historical_game: Dict) -> bool:
        """Check if historical conditions are similar to current"""
        temp_threshold = 5
        wind_threshold = 5
        
        return (
            abs(historical_game['temperature'] - historical_game['current_temperature']) <= temp_threshold and
            abs(historical_game['wind_speed'] - historical_game['current_wind_speed']) <= wind_threshold and
            historical_game['precipitation_type'] == historical_game['current_precipitation_type']
        )
    
    def _extract_notable_games(self, games: List[Dict]) -> List[Dict]:
        """Extract notable games with similar conditions"""
        return sorted(
            games,
            key=lambda x: x['impact_score'],
            reverse=True
        )[:3]  # Return top 3 most impactful games
