from crewai import Task
from typing import List, Dict
from datetime import datetime

def create_analysis_tasks(agents: Dict, team1: str, team2: str, game_date: str) -> List[Task]:
    """Create tasks for NFL game analysis"""
    tasks = []
    
    # Task 1: Performance Analysis
    tasks.append(Task(
        description=f"Analyze recent performance trends for {team1} and {team2}",
        expected_output="Detailed analysis of each team's recent performance metrics",
        agent=agents["Performance Analysis Expert"]
    ))
    
    # Task 2: Injury Analysis
    tasks.append(Task(
        description=f"Assess impact of current injuries for {team1} and {team2}",
        expected_output="Analysis of injury impacts on both teams",
        agent=agents["Injury Impact Analyst"]
    ))
    
    # Task 3: Location Analysis
    tasks.append(Task(
        description=f"Analyze home/away performance impact for both teams",
        expected_output="Analysis of location-based performance factors",
        agent=agents["Location Impact Analyst"]
    ))
    
    # Task 4: Matchup Analysis
    tasks.append(Task(
        description=f"Analyze head-to-head matchups between {team1} and {team2}",
        expected_output="Historical matchup analysis and key factors",
        agent=agents["Matchup Analysis Specialist"]
    ))
    
    # Task 5: Weather Analysis
    tasks.append(Task(
        description=f"Analyze weather impact for the game on {game_date}",
        expected_output="Weather forecast and potential impact analysis",
        agent=agents["Weather Impact Analyst"]
    ))
    
    return tasks

def format_analysis_output(task_results: List[Dict]) -> Dict:
    """Format the analysis results into a structured output"""
    return {
        'task_id': datetime.now().strftime('%Y%m%d%H%M%S'),
        'agent_results': task_results,
        'analysis': _generate_overall_analysis(task_results),
        'insights': extract_key_insights(task_results),
        'probability_score': calculate_probability_score(task_results),
        'thematic_breakdown': create_thematic_breakdown(task_results)
    }

def calculate_probability_score(results: List[Dict]) -> float:
    """Calculate overall probability score based on all analyses"""
    # In a real implementation, this would use a more sophisticated algorithm
    return 0.65  # Example probability

def extract_key_insights(results: List[Dict]) -> Dict:
    """Extract key insights from all analyses"""
    return {
        'performance': 'Team A shows strong offensive momentum',
        'injuries': 'Key defensive players are questionable',
        'location': 'Strong home field advantage history',
        'matchups': 'Historical advantage in similar weather conditions',
        'weather': 'Moderate impact expected on passing game'
    }

def create_thematic_breakdown(results: List[Dict]) -> Dict:
    """Create thematic breakdown of analysis results"""
    return {
        'offense': 'Strong passing game expected',
        'defense': 'Vulnerable against run plays',
        'special_teams': 'Above average field goal accuracy',
        'coaching': 'Aggressive play-calling trends',
        'environment': 'Weather and location factors favor home team'
    }

def _generate_overall_analysis(results: List[Dict]) -> str:
    """Generate overall analysis summary"""
    return """
    Based on comprehensive analysis of recent performance, injuries, location factors,
    matchups, and weather conditions, Team A shows a slight advantage. Key factors 
    include strong offensive momentum, historical success in similar conditions, and
    favorable home field advantage, despite some defensive injuries.
    """
