from crewai import Agent
from typing import Dict
from langchain.tools import Tool

class RosterAnalysisAgent:
    @staticmethod
    def create() -> Agent:
        return Agent(
            role='Roster Changes Analysis Agent',
            goal='Investigate roster changes and their impact on team dynamics',
            backstory="""You are an expert in analyzing NFL roster changes and their impact on team performance.
                        You track trades, injuries, and lineup changes.""",
            tools=[
                Tool(
                    name="analyze_roster_changes",
                    func=RosterAnalysisAgent.analyze_roster_changes,
                    description="Analyze recent roster changes and their impact"
                )
            ],
            verbose=True
        )

    @staticmethod
    def analyze_roster_changes(team_data: Dict) -> Dict:
        analysis = {
            'significant_changes': [],
            'impact_assessment': {},
            'key_players_status': {},
            'team_chemistry_impact': 'neutral'
        }
        
        # Analyze roster changes
        injuries = team_data.get('injuries', [])
        for injury in injuries:
            if injury['status'] == 'Out':
                analysis['significant_changes'].append({
                    'type': 'injury',
                    'player': injury['player'],
                    'impact': 'negative' if injury['position'] in ['QB', 'RB', 'WR'] else 'moderate'
                })
        
        return analysis
