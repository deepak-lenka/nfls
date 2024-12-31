from crewai import Crew
from .tasks.task_definitions import NFLAnalysisTasks
from .utils.data_scraper import NFLDataScraper
from typing import Dict
import asyncio
from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv
import os

class NFLAnalysisSystem:
    def __init__(self):
        self.data_scraper = NFLDataScraper()
        self.task_id = 5

    def analyze_game(self) -> str:
        # Header information
        output = [
            f"Task ID: {self.task_id}",
            f"Task: Who will win the NFL Game on Sun, Dec 15, Jets vs Jaguars?",
            f"\nTotal AI Agents: 8",
            "\nFactors Evaluated by AI Agents:"
        ]

        # 1. Gather raw data
        game_data = self.data_scraper.get_game_data()

        # 2. Create tasks for all agents
        tasks = NFLAnalysisTasks.create_all_tasks(game_data)

        # 3. Create and run crew
        crew = Crew(
            tasks=tasks,
            agents=[task.agent for task in tasks],
            verbose=True
        )

        # 4. Get results from all agents
        results = crew.kickoff()
        
        # Process each agent's findings
        for i, (agent_name, findings) in enumerate(results.items(), 1):
            output.extend(self.format_agent_findings(i, findings))

        return "\n".join(output)

    def format_agent_findings(self, agent_num: int, findings: Dict) -> list:
        """Format each agent's findings as shown in screenshot"""
        output = []
        
        # Format exactly as shown in screenshot
        output.append(f"\n- Agent {agent_num}: {findings.get('task', '')}")
        
        if 'findings' in findings:
            output.append("\nTask: " + findings['task'])
            output.append("Role: " + findings['role'])
            output.append("Priority: " + findings['priority'])
            output.append("\nKey Findings:")
            output.extend(findings['findings'])

        return output

    def generate_analysis_overview(self, all_results: Dict) -> str:
        """Generate comprehensive analysis based on all agents' findings"""
        # Collect key findings from all agents
        performance_data = all_results.get('performance', {})
        injury_data = all_results.get('injuries', {})
        weather_data = all_results.get('weather', {})
        matchup_data = all_results.get('matchup', {})
        coaching_data = all_results.get('coaching', {})
        
        # Combine all insights to generate overall analysis
        analysis_points = []
        
        # Add performance insights
        if performance_data:
            analysis_points.extend(performance_data.get('key_findings', []))
            
        # Add injury impact
        if injury_data:
            analysis_points.extend(injury_data.get('key_findings', []))
            
        # Add weather considerations
        if weather_data:
            analysis_points.extend(weather_data.get('impact_factors', []))
            
        # Add historical matchup insights
        if matchup_data:
            analysis_points.extend(matchup_data.get('key_trends', []))
            
        # Add coaching strategy insights
        if coaching_data:
            analysis_points.extend(coaching_data.get('strategic_factors', []))
        
        # Combine all insights into a coherent analysis
        overview = "Based on comprehensive analysis from all agents:\n\n"
        for point in analysis_points:
            overview += f"- {point}\n"
            
        return overview

if __name__ == "__main__":
    system = NFLAnalysisSystem()
    result = system.analyze_game()
    print(result)
