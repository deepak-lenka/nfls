from crewai import Agent
from typing import Dict, List
from src.utils.data_scraper import NFLDataScraper
from pydantic import Field, ConfigDict

class LocationAnalysisAgent(Agent):
    """Agent for analyzing location-based performance"""
    
    model_config = ConfigDict(arbitrary_types_allowed=True)
    data_scraper: NFLDataScraper = Field(default_factory=NFLDataScraper)
    
    def __init__(self):
        super().__init__(
            name="Location Impact Analyst",
            role="Expert in analyzing how venue and travel affect NFL team performance",
            goal="Analyze impact of game location on team performance",
            backstory="Sports analytics expert specializing in venue effects, travel impacts, and home-field advantage analysis",
            allow_delegation=False
        )
    
    def analyze_location_impact(self, team: str, location: str, is_home: bool) -> Dict:
        """
        Analyze location impact for a team
        
        Args:
            team (str): Team name
            location (str): Game location
            is_home (bool): Whether team is home or away
            
        Returns:
            Dict: Location analysis results
        """
        # Get recent games data
        recent_games = self.data_scraper.get_recent_games(team)
        
        # Filter games by location type
        home_games = [g for g in recent_games if g.get('is_home', False)]
        away_games = [g for g in recent_games if not g.get('is_home', False)]
        
        # Calculate location-based performance metrics
        home_performance = self._calculate_location_metrics(home_games)
        away_performance = self._calculate_location_metrics(away_games)
        
        # Calculate travel impact if away game
        travel_impact = self._calculate_travel_impact(location) if not is_home else None
        
        # Get venue-specific analysis
        venue_analysis = self._analyze_venue(location)
        
        # Get historical performance at venue
        historical_performance = self._analyze_historical_venue_performance(team, location)
        
        return {
            'team': team,
            'location': location,
            'is_home_game': is_home,
            'home_performance': home_performance,
            'away_performance': away_performance,
            'travel_impact': travel_impact,
            'venue_analysis': venue_analysis,
            'historical_venue_performance': historical_performance,
            'location_advantage': self._calculate_location_advantage(
                home_performance, 
                away_performance,
                venue_analysis,
                travel_impact
            )
        }
    
    def _calculate_location_metrics(self, games: List[Dict]) -> Dict:
        """Calculate performance metrics for a set of games"""
        if not games:
            return {
                'win_percentage': 0.0,
                'avg_points_scored': 0.0,
                'avg_points_allowed': 0.0,
                'avg_yards_gained': 0.0,
                'avg_yards_allowed': 0.0,
                'turnover_differential': 0.0
            }
        
        total_games = len(games)
        wins = sum(1 for game in games if game['result'] == 'W')
        
        return {
            'win_percentage': wins / total_games,
            'avg_points_scored': sum(game['points_scored'] for game in games) / total_games,
            'avg_points_allowed': sum(game['points_allowed'] for game in games) / total_games,
            'avg_yards_gained': sum(game['total_yards'] for game in games) / total_games,
            'avg_yards_allowed': sum(game['yards_allowed'] for game in games) / total_games,
            'turnover_differential': sum(game['turnover_differential'] for game in games) / total_games
        }
    
    def _calculate_travel_impact(self, location: str) -> Dict:
        """Calculate impact of travel on team performance"""
        travel_data = self.data_scraper.get_travel_data(location)
        
        impact_factors = []
        impact_score = 0.0
        
        # Time zone changes
        if abs(travel_data['time_zone_diff']) >= 2:
            impact_factors.append('significant time zone change')
            impact_score += 0.3
        elif abs(travel_data['time_zone_diff']) == 1:
            impact_factors.append('minor time zone change')
            impact_score += 0.1
        
        # Travel distance
        if travel_data['distance'] > 2000:
            impact_factors.append('long distance travel')
            impact_score += 0.3
        elif travel_data['distance'] > 1000:
            impact_factors.append('moderate distance travel')
            impact_score += 0.2
        
        # Travel time
        if travel_data['travel_time'] > 5:
            impact_factors.append('extended travel time')
            impact_score += 0.2
        
        return {
            'impact_score': min(1.0, impact_score),
            'impact_factors': impact_factors,
            'travel_distance': travel_data['distance'],
            'time_zone_difference': travel_data['time_zone_diff'],
            'estimated_travel_time': travel_data['travel_time']
        }
    
    def _analyze_venue(self, location: str) -> Dict:
        """Analyze venue characteristics"""
        venue_data = self.data_scraper.get_venue_data(location)
        
        advantages = []
        disadvantages = []
        
        # Surface type impact
        if venue_data['surface_type'] == 'artificial':
            advantages.append('consistent playing surface')
        elif venue_data['surface_type'] == 'grass':
            advantages.append('natural playing conditions')
        
        # Stadium type impact
        if venue_data['is_dome']:
            advantages.append('controlled environment')
            advantages.append('no weather impact')
        else:
            disadvantages.append('weather exposure')
        
        # Crowd impact
        if venue_data['capacity'] > 70000:
            advantages.append('large crowd impact')
        
        # Field dimensions and characteristics
        if venue_data.get('unique_characteristics'):
            for char in venue_data['unique_characteristics']:
                if char['impact_type'] == 'positive':
                    advantages.append(char['description'])
                else:
                    disadvantages.append(char['description'])
        
        return {
            'venue_type': 'dome' if venue_data['is_dome'] else 'outdoor',
            'surface_type': venue_data['surface_type'],
            'capacity': venue_data['capacity'],
            'advantages': advantages,
            'disadvantages': disadvantages,
            'notable_characteristics': venue_data.get('unique_characteristics', [])
        }
    
    def _analyze_historical_venue_performance(self, team: str, location: str) -> Dict:
        """Analyze team's historical performance at the venue"""
        historical_games = self.data_scraper.get_historical_venue_games(team, location)
        
        if not historical_games:
            return {
                'games_played': 0,
                'win_percentage': 0.0,
                'performance_trends': [],
                'notable_games': []
            }
        
        wins = sum(1 for game in historical_games if game['result'] == 'W')
        total_games = len(historical_games)
        
        # Identify trends
        trends = []
        recent_games = historical_games[-3:]
        if all(game['result'] == 'W' for game in recent_games):
            trends.append('winning streak at venue')
        elif all(game['result'] == 'L' for game in recent_games):
            trends.append('losing streak at venue')
        
        # Find notable games
        notable_games = sorted(
            historical_games,
            key=lambda x: x['significance_score'],
            reverse=True
        )[:3]
        
        return {
            'games_played': total_games,
            'win_percentage': wins / total_games if total_games > 0 else 0.0,
            'performance_trends': trends,
            'notable_games': [{
                'date': game['date'],
                'result': game['result'],
                'score': f"{game['team_score']}-{game['opponent_score']}",
                'significance': game['significance']
            } for game in notable_games]
        }
    
    def _calculate_location_advantage(
        self,
        home_performance: Dict,
        away_performance: Dict,
        venue_analysis: Dict,
        travel_impact: Dict = None
    ) -> float:
        """Calculate overall location advantage score (-1 to 1)"""
        score = 0.0
        weights = {
            'performance_diff': 0.4,
            'venue': 0.3,
            'travel': 0.3
        }
        
        # Performance differential (home vs away)
        perf_diff = (
            (home_performance['win_percentage'] - away_performance['win_percentage']) +
            (home_performance['avg_points_scored'] - away_performance['avg_points_scored']) / 10.0 +
            (away_performance['avg_points_allowed'] - home_performance['avg_points_allowed']) / 10.0
        ) / 3.0
        score += perf_diff * weights['performance_diff']
        
        # Venue impact
        venue_score = (
            len(venue_analysis['advantages']) - len(venue_analysis['disadvantages'])
        ) * 0.1
        score += venue_score * weights['venue']
        
        # Travel impact
        if travel_impact:
            score -= travel_impact['impact_score'] * weights['travel']
        
        return max(-1.0, min(1.0, score))
