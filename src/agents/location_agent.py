from crewai import Agent
from typing import Dict
from langchain.tools import Tool

class LocationAnalysisAgent:
    @staticmethod
    def create() -> Agent:
        return Agent(
            role='Home/Away Performance Analysis Agent',
            goal='Review performance differences in home and away games',
            backstory="""You are an expert in analyzing how teams perform differently at home versus away games.
                        You understand home field advantages and travel impacts.""",
            tools=[
                Tool(
                    name="analyze_location_impact",
                    func=LocationAnalysisAgent.analyze_location_impact,
                    description="Analyze home/away performance differences"
                )
            ],
            verbose=True
        )

    @staticmethod
    def analyze_location_impact(team_data: Dict) -> Dict:
        return {
            'home_performance': {
                'win_rate': team_data.get('home_win_rate', 0),
                'avg_points_scored': team_data.get('home_avg_points', 0),
                'avg_points_allowed': team_data.get('home_avg_points_allowed', 0)
            },
            'away_performance': {
                'win_rate': team_data.get('away_win_rate', 0),
                'avg_points_scored': team_data.get('away_avg_points', 0),
                'avg_points_allowed': team_data.get('away_avg_points_allowed', 0)
            },
            'location_advantage': 'home' if team_data.get('home_win_rate', 0) > team_data.get('away_win_rate', 0) else 'neutral'
        }
