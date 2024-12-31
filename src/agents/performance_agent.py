from crewai import Agent
from typing import Dict, List
from src.utils.data_scraper import NFLDataScraper
from pydantic import Field, ConfigDict

class PerformanceAnalysisAgent(Agent):
    """Agent for analyzing team performance trends"""
    
    model_config = ConfigDict(arbitrary_types_allowed=True)
    data_scraper: NFLDataScraper = Field(default_factory=NFLDataScraper)
    
    def __init__(self):
        super().__init__(
            name="Performance Analysis Expert",
            role="Expert sports analyst specializing in NFL team performance metrics and trends",
            goal="Analyze recent team performance trends and metrics",
            backstory="Expert sports analyst with over 10 years of experience in analyzing NFL team statistics and performance patterns",
            allow_delegation=False
        )
    
    def analyze_performance(self, team: str, n_games: int = 3) -> Dict:
        """
        Analyze recent performance for a team
        
        Args:
            team (str): Team name
            n_games (int): Number of recent games to analyze
            
        Returns:
            Dict: Performance analysis results
        """
        # Get recent games data
        games = self.data_scraper.get_recent_games(team, n_games)
        
        # Calculate performance metrics
        offensive_metrics = self._calculate_offensive_metrics(games)
        defensive_metrics = self._calculate_defensive_metrics(games)
        efficiency_metrics = self._calculate_efficiency_metrics(games)
        
        # Identify trends
        trends = self._identify_trends(games)
        
        return {
            'team': team,
            'games_analyzed': len(games),
            'offensive_metrics': offensive_metrics,
            'defensive_metrics': defensive_metrics,
            'efficiency_metrics': efficiency_metrics,
            'trends': trends,
            'momentum_score': self._calculate_momentum_score(games)
        }
    
    def _calculate_offensive_metrics(self, games: List[Dict]) -> Dict:
        """Calculate offensive performance metrics"""
        return {
            'avg_points': sum(game['points_scored'] for game in games) / len(games),
            'avg_yards': sum(game['total_yards'] for game in games) / len(games),
            'scoring_trend': self._calculate_trend([game['points_scored'] for game in games])
        }
    
    def _calculate_defensive_metrics(self, games: List[Dict]) -> Dict:
        """Calculate defensive performance metrics"""
        return {
            'avg_points_allowed': sum(game['points_allowed'] for game in games) / len(games),
            'avg_yards_allowed': sum(game['total_yards'] for game in games) / len(games),
            'turnover_ratio': sum(game['turnovers'] for game in games) / len(games)
        }
    
    def _calculate_efficiency_metrics(self, games: List[Dict]) -> Dict:
        """Calculate efficiency metrics"""
        return {
            'third_down_efficiency': sum(game['third_down_conv'] for game in games) / len(games),
            'red_zone_efficiency': self._calculate_red_zone_efficiency(games),
            'turnover_margin': self._calculate_turnover_margin(games)
        }
    
    def _identify_trends(self, games: List[Dict]) -> Dict:
        """Identify performance trends"""
        return {
            'scoring_trend': self._calculate_trend([game['points_scored'] for game in games]),
            'defense_trend': self._calculate_trend([game['points_allowed'] for game in games]),
            'yardage_trend': self._calculate_trend([game['total_yards'] for game in games])
        }
    
    def _calculate_trend(self, values: List[float]) -> str:
        """Calculate trend direction from a list of values"""
        if len(values) < 2:
            return 'stable'
            
        diffs = [values[i] - values[i-1] for i in range(1, len(values))]
        avg_diff = sum(diffs) / len(diffs)
        
        if avg_diff > 5:
            return 'improving'
        elif avg_diff < -5:
            return 'declining'
        else:
            return 'stable'
    
    def _calculate_red_zone_efficiency(self, games: List[Dict]) -> float:
        """Calculate red zone efficiency"""
        # In real implementation, would use actual red zone stats
        # For mock data, using a simplified calculation
        return sum(game['points_scored'] / max(1, game['total_yards'] / 20) for game in games) / len(games)
    
    def _calculate_turnover_margin(self, games: List[Dict]) -> float:
        """Calculate turnover margin"""
        return sum(game.get('turnovers', 0) for game in games) / len(games)
    
    def _calculate_momentum_score(self, games: List[Dict]) -> float:
        """Calculate overall momentum score"""
        if not games:
            return 0.0
            
        # Weight recent games more heavily
        weights = [1.5, 1.2, 1.0][:len(games)]
        normalized_weights = [w/sum(weights) for w in weights]
        
        # Calculate weighted average of key metrics
        momentum = 0
        for game, weight in zip(games, normalized_weights):
            game_score = (
                game['points_scored'] / 35.0 +  # Normalize to typical max points
                game['total_yards'] / 500.0 +   # Normalize to typical max yards
                game['third_down_conv']         # Already normalized (0-1)
            ) / 3.0
            momentum += game_score * weight
            
        return min(1.0, max(0.0, momentum))
