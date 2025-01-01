from crewai import Agent
from typing import Dict, List
from src.utils.data_scraper import NFLDataScraper
from pydantic import Field, ConfigDict
import math

class MatchupAnalysisAgent(Agent):
    """Agent for analyzing team matchups and historical performance"""
    
    model_config = ConfigDict(arbitrary_types_allowed=True)
    data_scraper: NFLDataScraper = Field(default_factory=NFLDataScraper)
    
    def __init__(self):
        super().__init__(
            name="Matchup Analysis Specialist",
            role="Expert in analyzing team matchups and identifying key advantages",
            goal="Analyze head-to-head matchups and historical performance",
            backstory="Senior NFL analyst with deep expertise in comparative team analysis and historical matchup patterns",
            allow_delegation=False
        )
    
    def analyze_matchup(self, team1: str, team2: str) -> Dict:
        """
        Analyze head-to-head matchup between two teams
        
        Args:
            team1 (str): First team name
            team2 (str): Second team name
            
        Returns:
            Dict: Matchup analysis results
        """
        # Get historical matchup data
        historical_matchups = self.data_scraper.get_historical_matchups(team1, team2)
        
        # Get recent games data for both teams
        team1_games = self.data_scraper.get_recent_games(team1)
        team2_games = self.data_scraper.get_recent_games(team2)
        
        # Analyze offensive matchup
        offensive_analysis = self._analyze_offensive_matchup(team1_games, team2_games)
        
        # Analyze defensive matchup
        defensive_analysis = self._analyze_defensive_matchup(team1_games, team2_games)
        
        # Calculate matchup advantages
        advantages = self._calculate_advantages(offensive_analysis, defensive_analysis)
        
        # Analyze historical trends
        historical_analysis = self._analyze_historical_trends(historical_matchups)
        
        return {
            'team1': team1,
            'team2': team2,
            'offensive_analysis': offensive_analysis,
            'defensive_analysis': defensive_analysis,
            'advantages': advantages,
            'historical_analysis': historical_analysis,
            'matchup_score': self._calculate_matchup_score(offensive_analysis, defensive_analysis, historical_analysis)
        }
    
    def _analyze_offensive_matchup(self, team1_games: List[Dict], team2_games: List[Dict]) -> Dict:
        """Analyze offensive matchup between teams"""
        if not team1_games or not team2_games:
            return {}
            
        # Calculate offensive metrics for both teams
        team1_metrics = {
            'points': sum(g['points_scored'] for g in team1_games) / len(team1_games),
            'total_yards': sum(g['total_yards'] for g in team1_games) / len(team1_games),
            'pass_yards': sum(g['passing_yards'] for g in team1_games) / len(team1_games),
            'rush_yards': sum(g['rushing_yards'] for g in team1_games) / len(team1_games),
            'third_down': sum(g['third_down_conv'] for g in team1_games) / len(team1_games),
            'red_zone': sum(g['red_zone_conversions'] for g in team1_games) / max(1, sum(g['red_zone_attempts'] for g in team1_games))
        }
        
        team2_metrics = {
            'points': sum(g['points_scored'] for g in team2_games) / len(team2_games),
            'total_yards': sum(g['total_yards'] for g in team2_games) / len(team2_games),
            'pass_yards': sum(g['passing_yards'] for g in team2_games) / len(team2_games),
            'rush_yards': sum(g['rushing_yards'] for g in team2_games) / len(team2_games),
            'third_down': sum(g['third_down_conv'] for g in team2_games) / len(team2_games),
            'red_zone': sum(g['red_zone_conversions'] for g in team2_games) / max(1, sum(g['red_zone_attempts'] for g in team2_games))
        }
        
        # Calculate differentials
        differentials = {
            'points': round(team1_metrics['points'] - team2_metrics['points'], 1),
            'total_yards': round(team1_metrics['total_yards'] - team2_metrics['total_yards'], 1),
            'pass_yards': round(team1_metrics['pass_yards'] - team2_metrics['pass_yards'], 1),
            'rush_yards': round(team1_metrics['rush_yards'] - team2_metrics['rush_yards'], 1),
            'third_down': round((team1_metrics['third_down'] - team2_metrics['third_down']) * 100, 1),
            'red_zone': round((team1_metrics['red_zone'] - team2_metrics['red_zone']) * 100, 1)
        }
        
        return {
            'team1_metrics': {k: round(v, 1) for k, v in team1_metrics.items()},
            'team2_metrics': {k: round(v, 1) for k, v in team2_metrics.items()},
            'differentials': differentials,
            'offensive_score': self._calculate_offensive_score(differentials)
        }
        
    def _analyze_defensive_matchup(self, team1_games: List[Dict], team2_games: List[Dict]) -> Dict:
        """Analyze defensive matchup between teams"""
        if not team1_games or not team2_games:
            return {}
            
        # Calculate defensive metrics for both teams
        team1_metrics = {
            'points_allowed': sum(g['points_allowed'] for g in team1_games) / len(team1_games),
            'sacks': sum(g['sacks'] for g in team1_games) / len(team1_games),
            'interceptions': sum(g['interceptions'] for g in team1_games) / len(team1_games),
            'turnovers': sum(g['turnovers'] for g in team1_games) / len(team1_games)
        }
        
        team2_metrics = {
            'points_allowed': sum(g['points_allowed'] for g in team2_games) / len(team2_games),
            'sacks': sum(g['sacks'] for g in team2_games) / len(team2_games),
            'interceptions': sum(g['interceptions'] for g in team2_games) / len(team2_games),
            'turnovers': sum(g['turnovers'] for g in team2_games) / len(team2_games)
        }
        
        # Calculate differentials (positive means team1 is better defensively)
        differentials = {
            'points_allowed': round(team2_metrics['points_allowed'] - team1_metrics['points_allowed'], 1),
            'sacks': round(team1_metrics['sacks'] - team2_metrics['sacks'], 1),
            'interceptions': round(team1_metrics['interceptions'] - team2_metrics['interceptions'], 1),
            'turnovers': round(team1_metrics['turnovers'] - team2_metrics['turnovers'], 1)
        }
        
        return {
            'team1_metrics': {k: round(v, 1) for k, v in team1_metrics.items()},
            'team2_metrics': {k: round(v, 1) for k, v in team2_metrics.items()},
            'differentials': differentials,
            'defensive_score': self._calculate_defensive_score(differentials)
        }
        
    def _calculate_advantages(self, offensive_analysis: Dict, defensive_analysis: Dict) -> Dict:
        """Calculate team advantages based on matchup analysis"""
        advantages = {
            'team1': [],
            'team2': []
        }
        
        # Offensive advantages
        off_diff = offensive_analysis.get('differentials', {})
        if off_diff.get('points', 0) > 3:
            advantages['team1'].append('Scoring')
        elif off_diff.get('points', 0) < -3:
            advantages['team2'].append('Scoring')
            
        if off_diff.get('pass_yards', 0) > 30:
            advantages['team1'].append('Passing game')
        elif off_diff.get('pass_yards', 0) < -30:
            advantages['team2'].append('Passing game')
            
        if off_diff.get('rush_yards', 0) > 30:
            advantages['team1'].append('Running game')
        elif off_diff.get('rush_yards', 0) < -30:
            advantages['team2'].append('Running game')
            
        # Defensive advantages
        def_diff = defensive_analysis.get('differentials', {})
        if def_diff.get('points_allowed', 0) > 3:
            advantages['team1'].append('Defense')
        elif def_diff.get('points_allowed', 0) < -3:
            advantages['team2'].append('Defense')
            
        if def_diff.get('turnovers', 0) > 0.5:
            advantages['team1'].append('Turnover creation')
        elif def_diff.get('turnovers', 0) < -0.5:
            advantages['team2'].append('Turnover creation')
        
        return advantages
        
    def _analyze_historical_trends(self, historical_matchups: List[Dict]) -> Dict:
        """Analyze historical matchup trends"""
        if not historical_matchups:
            return {
                'total_games': 0,
                'team1_wins': 0,
                'team2_wins': 0,
                'avg_point_diff': 0,
                'recent_trend': 'No historical data'
            }
            
        team1_wins = sum(1 for game in historical_matchups if game['winner'] == 'team1')
        team2_wins = sum(1 for game in historical_matchups if game['winner'] == 'team2')
        point_diffs = [game['point_differential'] for game in historical_matchups]
        
        # Analyze recent trend (last 3 games)
        recent_games = historical_matchups[-3:]
        recent_wins = sum(1 for game in recent_games if game['winner'] == 'team1')
        
        if recent_wins >= 2:
            trend = 'Team 1 dominant'
        elif recent_wins <= 1:
            trend = 'Team 2 dominant'
        else:
            trend = 'Evenly matched'
        
        return {
            'total_games': len(historical_matchups),
            'team1_wins': team1_wins,
            'team2_wins': team2_wins,
            'win_percentage': round(team1_wins / len(historical_matchups) * 100, 1),
            'avg_point_diff': round(sum(point_diffs) / len(historical_matchups), 1),
            'recent_trend': trend
        }
        
    def _calculate_offensive_score(self, differentials: Dict) -> float:
        """Calculate offensive advantage score (-100 to 100)"""
        weights = {
            'points': 0.3,
            'total_yards': 0.2,
            'pass_yards': 0.15,
            'rush_yards': 0.15,
            'third_down': 0.1,
            'red_zone': 0.1
        }
        
        score = 0
        for metric, weight in weights.items():
            if metric in differentials:
                normalized_diff = differentials[metric] / (100 if 'yards' in metric else 20)
                score += normalized_diff * weight * 100
                
        return round(max(-100, min(100, score)), 1)
        
    def _calculate_defensive_score(self, differentials: Dict) -> float:
        """Calculate defensive advantage score (-100 to 100)"""
        weights = {
            'points_allowed': 0.4,
            'sacks': 0.2,
            'interceptions': 0.2,
            'turnovers': 0.2
        }
        
        score = 0
        for metric, weight in weights.items():
            if metric in differentials:
                normalized_diff = differentials[metric] / (20 if metric == 'points_allowed' else 2)
                score += normalized_diff * weight * 100
                
        return round(max(-100, min(100, score)), 1)
        
    def _calculate_matchup_score(self, offensive_analysis: Dict, defensive_analysis: Dict, historical_analysis: Dict) -> Dict:
        """Calculate overall matchup score and win probability"""
        # Get component scores
        offensive_score = offensive_analysis.get('offensive_score', 0)
        defensive_score = defensive_analysis.get('defensive_score', 0)
        
        # Calculate historical weight
        historical_games = historical_analysis.get('total_games', 0)
        historical_weight = min(0.2, historical_games * 0.02)  # Max 20% weight for historical data
        
        # Calculate historical score
        historical_score = 0
        if historical_games > 0:
            win_pct = historical_analysis.get('win_percentage', 50)
            point_diff = historical_analysis.get('avg_point_diff', 0)
            historical_score = (win_pct - 50) + point_diff * 2
        
        # Calculate composite score
        composite_score = (
            offensive_score * 0.4 +
            defensive_score * 0.4 +
            historical_score * historical_weight
        ) / (0.8 + historical_weight)
        
        # Convert to win probability (logistic function)
        win_probability = 1 / (1 + math.exp(-composite_score/30)) * 100
        
        return {
            'composite_score': round(composite_score, 1),
            'win_probability': round(win_probability, 1),
            'confidence': round(min(abs(composite_score), 100), 1)
        }
