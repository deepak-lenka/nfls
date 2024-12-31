from crewai import Agent
from typing import Dict
from langchain.tools import Tool

class SeasonStatsAnalysisAgent:
    @staticmethod
    def create() -> Agent:
        return Agent(
            role='Season Statistics Analysis Agent',
            goal='Analyze season-long performance statistics',
            backstory="""You are an expert in analyzing NFL team season statistics.
                        You understand trends in scoring, defense, and overall performance.""",
            tools=[
                Tool(
                    name="analyze_season_stats",
                    func=SeasonStatsAnalysisAgent.analyze_season_stats,
                    description="Analyze season statistics for teams"
                )
            ],
            verbose=True
        )

    @staticmethod
    def analyze_season_stats(season_data: Dict) -> Dict:
        return {
            'offensive_stats': {
                'points_per_game': season_data.get('avg_points_per_game', 0),
                'yards_per_game': season_data.get('avg_yards_per_game', 0),
                'third_down_efficiency': season_data.get('third_down_rate', 0)
            },
            'defensive_stats': {
                'points_allowed_per_game': season_data.get('avg_points_against', 0),
                'yards_allowed_per_game': season_data.get('avg_yards_against', 0)
            },
            'overall_assessment': 'neutral'
        }
