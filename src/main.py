from crewai import Agent, Task, Crew, Process
from src.core.config import AGENT_CONFIG, OPENAI_API_KEY
from src.utils.data_scraper import NFLDataScraper
from src.tasks.task_definitions import create_analysis_tasks
from src.agents import (
    PerformanceAnalysisAgent,
    InjuryAnalysisAgent,
    MatchupAnalysisAgent,
    WeatherAnalysisAgent,
    LocationAnalysisAgent
)

class NFLAnalysisSystem:
    """Main class for NFL game analysis system"""
    
    def __init__(self):
        self.data_scraper = NFLDataScraper()
        self.agents = {}
        
    def create_agents(self):
        """Create and configure analysis agents"""
        # Initialize agents
        performance_agent = PerformanceAnalysisAgent()
        injury_agent = InjuryAnalysisAgent()
        location_agent = LocationAnalysisAgent()
        matchup_agent = MatchupAnalysisAgent()
        weather_agent = WeatherAnalysisAgent()
        
        # Store agents by name
        self.agents = {
            "Performance Analysis Expert": performance_agent,
            "Injury Impact Analyst": injury_agent,
            "Location Impact Analyst": location_agent,
            "Matchup Analysis Specialist": matchup_agent,
            "Weather Impact Analyst": weather_agent
        }
        
        return list(self.agents.values())

    def analyze_game(self, team1, team2, game_date):
        """
        Analyze an NFL game and predict the outcome
        
        Args:
            team1 (str): Name of the first team
            team2 (str): Name of the second team
            game_date (str): Date of the game (YYYY-MM-DD)
            
        Returns:
            dict: Analysis results including predictions and insights
        """
        # Create agents
        agents = self.create_agents()
        
        # Create tasks with agents
        tasks = create_analysis_tasks(self.agents, team1, team2, game_date)
        
        # Create crew
        crew = Crew(
            agents=agents,
            tasks=tasks,
            process=Process.sequential,
            verbose=True
        )
        
        # Execute analysis
        result = crew.kickoff()
        
        return result

def main():
    # Initialize the system
    nfl_system = NFLAnalysisSystem()
    
    # Example usage
    result = nfl_system.analyze_game(
        team1="New York Jets",
        team2="Jacksonville Jaguars",
        game_date="2024-12-15"
    )
    
    # Display results
    print(f"Task ID: {result.get('task_id')}")
    print(f"Analysis: {result.get('analysis')}")
    print(f"Probability Score: {result.get('probability_score')}")
    print(f"Key Insights: {result.get('insights')}")
    print(f"Thematic Breakdown: {result.get('thematic_breakdown')}")

if __name__ == "__main__":
    main()
