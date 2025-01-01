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
        'probability_score': calculate_probability_score(task_results),
        'insights': extract_key_insights(task_results),
        'thematic_breakdown': create_thematic_breakdown(task_results)
    }

def calculate_probability_score(results: List[Dict]) -> float:
    """Calculate overall win probability based on all analyses"""
    weights = {
        'Performance Analysis Expert': 0.25,
        'Matchup Analysis Specialist': 0.25,
        'Injury Impact Analyst': 0.20,
        'Location Impact Analyst': 0.15,
        'Weather Impact Analyst': 0.15
    }
    
    weighted_score = 0
    total_weight = 0
    
    for result in results:
        agent_name = result.get('agent_name')
        if agent_name in weights:
            score = result.get('win_probability', 50)  # Default to 50% if not provided
            weighted_score += score * weights[agent_name]
            total_weight += weights[agent_name]
    
    if total_weight == 0:
        return 50.0  # Default to 50% if no valid results
        
    return round(weighted_score / total_weight, 1)

def extract_key_insights(results: List[Dict]) -> List[str]:
    """Extract key insights from all analyses"""
    insights = []
    
    for result in results:
        # Extract insights based on agent type
        agent_name = result.get('agent_name')
        
        if agent_name == 'Performance Analysis Expert':
            trends = result.get('trends', [])
            if trends:
                insights.extend(trends[:2])  # Add top 2 performance trends
                
        elif agent_name == 'Matchup Analysis Specialist':
            advantages = result.get('advantages', {})
            for team, team_advantages in advantages.items():
                if team_advantages:
                    insights.append(f"{team} has advantages in: {', '.join(team_advantages)}")
                    
        elif agent_name == 'Injury Impact Analyst':
            key_injuries = result.get('key_injuries', [])
            if key_injuries:
                insights.extend(key_injuries[:2])  # Add top 2 injury impacts
                
        elif agent_name == 'Location Impact Analyst':
            location_factor = result.get('location_impact')
            if location_factor:
                insights.append(location_factor)
                
        elif agent_name == 'Weather Impact Analyst':
            weather_impact = result.get('weather_impact')
            if weather_impact:
                insights.append(weather_impact)
    
    # Remove duplicates and limit to top 5 insights
    unique_insights = list(dict.fromkeys(insights))
    return unique_insights[:5]

def create_thematic_breakdown(results: List[Dict]) -> Dict:
    """Create thematic breakdown of analysis results"""
    themes = {
        'offense': {
            'score': 0,
            'factors': []
        },
        'defense': {
            'score': 0,
            'factors': []
        },
        'situational': {
            'score': 0,
            'factors': []
        },
        'external': {
            'score': 0,
            'factors': []
        }
    }
    
    for result in results:
        agent_name = result.get('agent_name')
        
        if agent_name == 'Performance Analysis Expert':
            # Add offensive and defensive metrics
            off_metrics = result.get('offensive_metrics', {})
            def_metrics = result.get('defensive_metrics', {})
            
            themes['offense']['score'] = off_metrics.get('offensive_score', 0)
            themes['defense']['score'] = def_metrics.get('defensive_score', 0)
            
            if 'trends' in result:
                for trend in result['trends']:
                    if 'offensive' in trend.lower():
                        themes['offense']['factors'].append(trend)
                    elif 'defensive' in trend.lower():
                        themes['defense']['factors'].append(trend)
                        
        elif agent_name == 'Matchup Analysis Specialist':
            # Add matchup-specific factors
            matchup_score = result.get('matchup_score', {})
            if matchup_score:
                themes['situational']['score'] = matchup_score.get('composite_score', 0)
                
        elif agent_name in ['Location Impact Analyst', 'Weather Impact Analyst']:
            # Add external factors
            impact_score = result.get('impact_score', 0)
            impact_factor = result.get('impact_factor')
            
            if impact_score:
                themes['external']['score'] = (themes['external']['score'] + impact_score) / 2
            if impact_factor:
                themes['external']['factors'].append(impact_factor)
    
    # Normalize scores to 0-100 range
    for theme in themes.values():
        theme['score'] = round(min(max(theme['score'], 0), 100), 1)
        theme['factors'] = list(dict.fromkeys(theme['factors']))[:3]  # Limit to top 3 unique factors
    
    return themes

def _generate_overall_analysis(results: List[Dict]) -> str:
    """Generate overall analysis summary"""
    # Calculate overall probability
    win_probability = calculate_probability_score(results)
    
    # Get key insights
    insights = extract_key_insights(results)
    
    # Get thematic breakdown
    themes = create_thematic_breakdown(results)
    
    # Generate summary
    summary = []
    
    # Add win probability
    if win_probability > 60:
        summary.append(f"Strong winning probability of {win_probability}%")
    elif win_probability < 40:
        summary.append(f"Lower winning probability of {win_probability}%")
    else:
        summary.append(f"Even matchup with {win_probability}% win probability")
    
    # Add thematic insights
    for theme, data in themes.items():
        if data['score'] > 60:
            summary.append(f"Strong {theme} advantage (Score: {data['score']})")
        elif data['score'] < 40:
            summary.append(f"Weakness in {theme} (Score: {data['score']})")
    
    # Add key insights
    if insights:
        summary.append("\nKey Factors:")
        summary.extend([f"- {insight}" for insight in insights])
    
    return "\n".join(summary)
