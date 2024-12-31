from crewai import Agent
from typing import Dict
from langchain.tools import Tool

class InjuryAnalysisAgent:
    @staticmethod
    def create() -> Agent:
        return Agent(
            role='Injury Report Analysis Agent',
            goal='Analyze impact of injuries on team performance',
            backstory="""You are an expert in analyzing NFL injury reports and their impact on team performance.
                        You understand how different injuries affect player availability and team strategy.""",
            tools=[
                Tool(
                    name="analyze_injury_impact",
                    func=InjuryAnalysisAgent.analyze_injury_impact,
                    description="Analyze injury reports and their impact"
                )
            ],
            verbose=True
        )

    @staticmethod
    def analyze_injury_impact(injury_data: Dict) -> Dict:
        analysis = {
            'key_injuries': [],
            'position_groups_affected': set(),
            'overall_impact': 'neutral',
            'gameplan_adjustments': []
        }
        
        for player_injury in injury_data:
            if player_injury['status'] in ['Out', 'Doubtful']:
                analysis['key_injuries'].append({
                    'player': player_injury['player'],
                    'position': player_injury['position'],
                    'impact': 'high' if player_injury['position'] in ['QB', 'RB', 'WR'] else 'moderate'
                })
                analysis['position_groups_affected'].add(player_injury['position'])
        
        return analysis
