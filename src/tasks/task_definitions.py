from crewai import Task
from typing import List
from ..agents.performance_agent import PerformanceAnalysisAgent
from ..agents.weather_agent import WeatherAnalysisAgent
from ..agents.roster_agent import RosterAnalysisAgent
from ..agents.location_agent import LocationAnalysisAgent
from ..agents.injury_agent import InjuryAnalysisAgent
from ..agents.matchup_agent import MatchupAnalysisAgent
from ..agents.season_stats_agent import SeasonStatsAnalysisAgent
from ..agents.coaching_agent import CoachingAnalysisAgent

class NFLAnalysisTasks:
    @staticmethod
    def create_all_tasks(game_data: dict) -> List[Task]:
        """Create all analysis tasks for a given game"""
        tasks = [
            Task(
                description="Examine the current form and momentum of both teams by reviewing their last three games",
                agent=PerformanceAnalysisAgent.create(),
                context=game_data
            ),
            Task(
                description="Investigate roster changes and their impact",
                agent=RosterAnalysisAgent.create(),
                context=game_data
            )
        ]
        return tasks
