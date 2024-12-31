from crewai import Agent
from typing import Dict, List
from src.utils.data_scraper import NFLDataScraper
from pydantic import Field, ConfigDict

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
            'matchup_score': self._calculate_matchup_score(advantages, historical_analysis)
        }
    
    def _analyze_offensive_matchup(self, team1_games: List[Dict], team2_games: List[Dict]) -> Dict:
        """Analyze offensive matchup between teams"""
        team1_offense = self._calculate_offensive_metrics(team1_games)
        team2_offense = self._calculate_offensive_metrics(team2_games)
        
        return {
            'team1': {
                'metrics': team1_offense,
                'strengths': self._identify_offensive_strengths(team1_offense),
                'weaknesses': self._identify_offensive_weaknesses(team1_offense)
            },
            'team2': {
                'metrics': team2_offense,
                'strengths': self._identify_offensive_strengths(team2_offense),
                'weaknesses': self._identify_offensive_weaknesses(team2_offense)
            }
        }
    
    def _analyze_defensive_matchup(self, team1_games: List[Dict], team2_games: List[Dict]) -> Dict:
        """Analyze defensive matchup between teams"""
        team1_defense = self._calculate_defensive_metrics(team1_games)
        team2_defense = self._calculate_defensive_metrics(team2_games)
        
        return {
            'team1': {
                'metrics': team1_defense,
                'strengths': self._identify_defensive_strengths(team1_defense),
                'weaknesses': self._identify_defensive_weaknesses(team1_defense)
            },
            'team2': {
                'metrics': team2_defense,
                'strengths': self._identify_defensive_strengths(team2_defense),
                'weaknesses': self._identify_defensive_weaknesses(team2_defense)
            }
        }
    
    def _calculate_advantages(self, offensive_analysis: Dict, defensive_analysis: Dict) -> Dict:
        """Calculate matchup advantages for each team"""
        advantages = {
            'team1': [],
            'team2': []
        }
        
        # Compare offensive strengths vs defensive weaknesses
        self._compare_offense_vs_defense(
            offensive_analysis['team1']['strengths'],
            defensive_analysis['team2']['weaknesses'],
            advantages['team1']
        )
        
        self._compare_offense_vs_defense(
            offensive_analysis['team2']['strengths'],
            defensive_analysis['team1']['weaknesses'],
            advantages['team2']
        )
        
        return advantages
    
    def _analyze_historical_trends(self, matchups: List[Dict]) -> Dict:
        """Analyze historical matchup trends"""
        if not matchups:
            return {
                'head_to_head_record': {'wins': 0, 'losses': 0},
                'average_point_differential': 0,
                'trends': [],
                'notable_factors': []
            }
        
        team1_wins = sum(1 for game in matchups if game['winner'] == game['team1'])
        total_diff = sum(game['team1_score'] - game['team2_score'] for game in matchups)
        
        trends = []
        if len(matchups) >= 3:
            recent_games = matchups[-3:]
            if all(game['winner'] == game['team1'] for game in recent_games):
                trends.append("Team 1 has won last 3 matchups")
            elif all(game['winner'] == game['team2'] for game in recent_games):
                trends.append("Team 2 has won last 3 matchups")
        
        return {
            'head_to_head_record': {
                'wins': team1_wins,
                'losses': len(matchups) - team1_wins
            },
            'average_point_differential': total_diff / len(matchups),
            'trends': trends,
            'notable_factors': self._identify_notable_factors(matchups)
        }
    
    def _calculate_matchup_score(self, advantages: Dict, historical: Dict) -> float:
        """Calculate overall matchup score (-1 to 1, positive favors team1)"""
        score = 0.0
        
        # Advantage score (60% weight)
        advantage_score = (len(advantages['team1']) - len(advantages['team2'])) * 0.2
        score += advantage_score * 0.6
        
        # Historical score (40% weight)
        if historical['head_to_head_record']['wins'] + historical['head_to_head_record']['losses'] > 0:
            win_rate = historical['head_to_head_record']['wins'] / (
                historical['head_to_head_record']['wins'] + historical['head_to_head_record']['losses']
            )
            historical_score = (win_rate - 0.5) * 2  # Convert to -1 to 1 scale
            score += historical_score * 0.4
        
        return max(-1.0, min(1.0, score))  # Clamp between -1 and 1
    
    def _calculate_offensive_metrics(self, games: List[Dict]) -> Dict:
        """Calculate offensive metrics from game data"""
        return {
            'avg_points': sum(game['points_scored'] for game in games) / len(games),
            'avg_yards': sum(game['total_yards'] for game in games) / len(games),
            'third_down_rate': sum(game['third_down_conv'] for game in games) / len(games)
        }
    
    def _calculate_defensive_metrics(self, games: List[Dict]) -> Dict:
        """Calculate defensive metrics from game data"""
        return {
            'avg_points_allowed': sum(game['points_allowed'] for game in games) / len(games),
            'avg_yards_allowed': sum(game['total_yards'] for game in games) / len(games),
            'third_down_stop_rate': 1 - sum(game['third_down_conv'] for game in games) / len(games)
        }
    
    def _identify_offensive_strengths(self, metrics: Dict) -> List[str]:
        """Identify strengths of a team's offense"""
        strengths = []
        if metrics['avg_points'] > 25:
            strengths.append('high scoring')
        if metrics['avg_yards'] > 350:
            strengths.append('high yardage')
        if metrics['third_down_rate'] > 0.4:
            strengths.append('third down efficiency')
        return strengths
    
    def _identify_offensive_weaknesses(self, metrics: Dict) -> List[str]:
        """Identify weaknesses of a team's offense"""
        weaknesses = []
        if metrics['avg_points'] < 15:
            weaknesses.append('low scoring')
        if metrics['avg_yards'] < 250:
            weaknesses.append('low yardage')
        if metrics['third_down_rate'] < 0.3:
            weaknesses.append('third down inefficiency')
        return weaknesses
    
    def _identify_defensive_strengths(self, metrics: Dict) -> List[str]:
        """Identify strengths of a team's defense"""
        strengths = []
        if metrics['avg_points_allowed'] < 15:
            strengths.append('low points allowed')
        if metrics['avg_yards_allowed'] < 250:
            strengths.append('low yardage allowed')
        if metrics['third_down_stop_rate'] > 0.6:
            strengths.append('third down stops')
        return strengths
    
    def _identify_defensive_weaknesses(self, metrics: Dict) -> List[str]:
        """Identify weaknesses of a team's defense"""
        weaknesses = []
        if metrics['avg_points_allowed'] > 25:
            weaknesses.append('high points allowed')
        if metrics['avg_yards_allowed'] > 350:
            weaknesses.append('high yardage allowed')
        if metrics['third_down_stop_rate'] < 0.4:
            weaknesses.append('third down inefficiency')
        return weaknesses
    
    def _compare_offense_vs_defense(self, offense: List[str], defense: List[str], advantages: List[str]) -> None:
        """Compare offense strengths vs defense weaknesses"""
        for strength in offense:
            if strength in defense:
                advantages.append(strength)
    
    def _identify_notable_factors(self, matchups: List[Dict]) -> List[str]:
        """Identify notable factors in historical matchups"""
        notable_factors = []
        if any(game['weather'] == 'rain' for game in matchups):
            notable_factors.append('rain')
        if any(game['weather'] == 'snow' for game in matchups):
            notable_factors.append('snow')
        return notable_factors
