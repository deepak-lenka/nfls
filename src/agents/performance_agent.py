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
        if not games:
            return {}
            
        total_yards = sum(game['total_yards'] for game in games)
        passing_yards = sum(game['passing_yards'] for game in games)
        rushing_yards = sum(game['rushing_yards'] for game in games)
        points_scored = sum(game['points_scored'] for game in games)
        red_zone_attempts = sum(game['red_zone_attempts'] for game in games)
        red_zone_conversions = sum(game['red_zone_conversions'] for game in games)
        
        return {
            'avg_total_yards': round(total_yards / len(games), 1),
            'avg_passing_yards': round(passing_yards / len(games), 1),
            'avg_rushing_yards': round(rushing_yards / len(games), 1),
            'avg_points': round(points_scored / len(games), 1),
            'red_zone_efficiency': round(red_zone_conversions / red_zone_attempts * 100 if red_zone_attempts > 0 else 0, 1),
            'yards_per_point': round(total_yards / points_scored if points_scored > 0 else 0, 1),
            'pass_rush_ratio': round(passing_yards / rushing_yards if rushing_yards > 0 else 0, 1)
        }
        
    def _calculate_defensive_metrics(self, games: List[Dict]) -> Dict:
        """Calculate defensive performance metrics"""
        if not games:
            return {}
            
        points_allowed = sum(game['points_allowed'] for game in games)
        sacks = sum(game['sacks'] for game in games)
        interceptions = sum(game['interceptions'] for game in games)
        turnovers = sum(game['turnovers'] for game in games)
        
        return {
            'avg_points_allowed': round(points_allowed / len(games), 1),
            'avg_sacks': round(sacks / len(games), 1),
            'avg_interceptions': round(interceptions / len(games), 1),
            'avg_turnovers_forced': round(turnovers / len(games), 1),
            'defensive_score': self._calculate_defensive_score(games)
        }
        
    def _calculate_efficiency_metrics(self, games: List[Dict]) -> Dict:
        """Calculate team efficiency metrics"""
        if not games:
            return {}
            
        third_down_efficiency = sum(game['third_down_conv'] for game in games) / len(games)
        fourth_down_efficiency = sum(game['fourth_down_conv'] for game in games) / len(games)
        penalties = sum(game['penalties'] for game in games)
        penalty_yards = sum(game['penalty_yards'] for game in games)
        
        return {
            'third_down_efficiency': round(third_down_efficiency * 100, 1),
            'fourth_down_efficiency': round(fourth_down_efficiency * 100, 1),
            'penalties_per_game': round(penalties / len(games), 1),
            'penalty_yards_per_game': round(penalty_yards / len(games), 1),
            'discipline_score': round(100 - (penalty_yards / (100 * len(games))), 1)
        }
        
    def _identify_trends(self, games: List[Dict]) -> Dict:
        """Identify performance trends from recent games"""
        if len(games) < 2:
            return {'trend_confidence': 0, 'trends': []}
            
        # Sort games by date
        sorted_games = sorted(games, key=lambda x: x['date'])
        
        # Calculate trend indicators
        points_trend = self._calculate_trend([g['points_scored'] for g in sorted_games])
        yards_trend = self._calculate_trend([g['total_yards'] for g in sorted_games])
        defense_trend = self._calculate_trend([g['points_allowed'] for g in sorted_games], inverse=True)
        
        trends = []
        confidence = 0
        
        # Analyze offensive trends
        if points_trend > 0.1:
            trends.append("Improving offensive scoring")
            confidence += 20
        elif points_trend < -0.1:
            trends.append("Declining offensive production")
            confidence -= 20
            
        if yards_trend > 0.1:
            trends.append("Increasing offensive yardage")
            confidence += 15
        elif yards_trend < -0.1:
            trends.append("Decreasing offensive yardage")
            confidence -= 15
            
        # Analyze defensive trends
        if defense_trend > 0.1:
            trends.append("Improving defensive performance")
            confidence += 20
        elif defense_trend < -0.1:
            trends.append("Declining defensive performance")
            confidence -= 20
            
        return {
            'trend_confidence': min(max(confidence, 0), 100),
            'trends': trends
        }
        
    def _calculate_trend(self, values: List[float], inverse: bool = False) -> float:
        """Calculate trend coefficient (-1 to 1) from a series of values"""
        if len(values) < 2:
            return 0
            
        diffs = [values[i+1] - values[i] for i in range(len(values)-1)]
        trend = sum(diffs) / (len(diffs) * max(values))
        return -trend if inverse else trend
        
    def _calculate_momentum_score(self, games: List[Dict]) -> float:
        """Calculate team momentum score (0-100)"""
        if not games:
            return 0
            
        # Weight recent games more heavily
        weights = [1.5, 1.2, 1.0, 0.8, 0.6][:len(games)]
        total_weight = sum(weights)
        
        # Calculate weighted performance scores
        weighted_scores = []
        for game, weight in zip(games, weights):
            score = (
                (game['points_scored'] / 35) * 30 +  # Max 30 points for scoring
                (1 - game['points_allowed'] / 35) * 30 +  # Max 30 points for defense
                (game['third_down_conv']) * 20 +  # Max 20 points for efficiency
                (1 - game['turnovers'] / 5) * 20   # Max 20 points for ball security
            )
            weighted_scores.append(score * weight)
            
        momentum = sum(weighted_scores) / total_weight
        return round(min(max(momentum, 0), 100), 1)
        
    def _calculate_defensive_score(self, games: List[Dict]) -> float:
        """Calculate defensive performance score (0-100)"""
        if not games:
            return 0
            
        scores = []
        for game in games:
            score = (
                (1 - game['points_allowed'] / 35) * 40 +  # Max 40 points for points allowed
                (game['sacks'] / 4) * 20 +  # Max 20 points for sacks
                (game['interceptions'] / 2) * 20 +  # Max 20 points for interceptions
                (game['turnovers'] / 3) * 20  # Max 20 points for total turnovers
            )
            scores.append(score)
            
        return round(min(max(sum(scores) / len(scores), 0), 100), 1)
