from crewai import Agent
from typing import Dict, List
from src.utils.data_scraper import NFLDataScraper
from pydantic import Field, ConfigDict

class InjuryAnalysisAgent(Agent):
    """Agent for analyzing team injuries and their impact"""
    
    model_config = ConfigDict(arbitrary_types_allowed=True)
    data_scraper: NFLDataScraper = Field(default_factory=NFLDataScraper)
    
    def __init__(self):
        super().__init__(
            name="Injury Impact Analyst",
            role="Medical professional specializing in sports injuries and their impact on team performance",
            goal="Assess impact of team injuries on game outcome",
            backstory="Sports medicine expert with extensive experience in NFL injury analysis and recovery assessment",
            allow_delegation=False
        )
    
    def analyze_injuries(self, team: str) -> Dict:
        """
        Analyze current injuries for a team
        
        Args:
            team (str): Team name
            
        Returns:
            Dict: Injury analysis results
        """
        # Get injury data
        injuries = self.data_scraper.get_injury_report(team)
        
        # Analyze impact by position
        impact_by_position = self._analyze_position_impact(injuries)
        
        # Calculate overall impact score
        impact_score = self._calculate_impact_score(injuries)
        
        # Get depth chart impact
        depth_impact = self._analyze_depth_chart_impact(injuries)
        
        return {
            'team': team,
            'total_injuries': len(injuries),
            'impact_by_position': impact_by_position,
            'depth_chart_impact': depth_impact,
            'overall_impact_score': impact_score
        }
    
    def _analyze_position_impact(self, injuries: List[Dict]) -> Dict:
        """Analyze injury impact by position group"""
        position_impact = {}
        for injury in injuries:
            position = injury['position']
            if position not in position_impact:
                position_impact[position] = {
                    'count': 0,
                    'severity': 0,
                    'key_players': []
                }
            
            position_impact[position]['count'] += 1
            position_impact[position]['severity'] += self._get_injury_severity(injury)
            
            if injury.get('is_starter', False):
                position_impact[position]['key_players'].append(injury['player'])
        
        return position_impact
    
    def _calculate_impact_score(self, injuries: List[Dict]) -> float:
        """Calculate overall injury impact score"""
        total_impact = 0
        weights = {
            'QB': 1.5,
            'WR': 1.2,
            'RB': 1.2,
            'TE': 1.1,
            'OL': 1.3,
            'DL': 1.2,
            'LB': 1.1,
            'DB': 1.2,
            'K': 0.8,
            'P': 0.7
        }
        
        for injury in injuries:
            severity = self._get_injury_severity(injury)
            position_weight = weights.get(injury['position'], 1.0)
            starter_weight = 1.5 if injury.get('is_starter', False) else 1.0
            
            impact = severity * position_weight * starter_weight
            total_impact += impact
            
        return total_impact / len(injuries) if injuries else 0
    
    def _get_injury_severity(self, injury: Dict) -> float:
        """Get severity score for an injury"""
        severity_scores = {
            'OUT': 1.0,
            'DOUBTFUL': 0.8,
            'QUESTIONABLE': 0.5,
            'PROBABLE': 0.2
        }
        return severity_scores.get(injury['status'].upper(), 0.0)
    
    def _analyze_depth_chart_impact(self, injuries: List[Dict]) -> Dict:
        """Analyze impact on team's depth chart"""
        depth_impact = {
            'starters_injured': 0,
            'backups_injured': 0,
            'critical_positions_affected': set(),
            'position_groups_depleted': []
        }
        
        position_counts = {}
        for injury in injuries:
            pos = injury['position']
            if injury.get('is_starter', False):
                depth_impact['starters_injured'] += 1
                depth_impact['critical_positions_affected'].add(pos)
            else:
                depth_impact['backups_injured'] += 1
            
            position_counts[pos] = position_counts.get(pos, 0) + 1
            
            # Check for depleted position groups (more than 2 injuries)
            if position_counts[pos] >= 2:
                depth_impact['position_groups_depleted'].append(pos)
        
        depth_impact['critical_positions_affected'] = list(depth_impact['critical_positions_affected'])
        return depth_impact
