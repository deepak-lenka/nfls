from crewai import Agent
from typing import Dict
from langchain.tools import Tool

class WeatherAnalysisAgent:
    @staticmethod
    def create() -> Agent:
        return Agent(
            role='Weather Impact Analysis Agent',
            goal='Analyze weather conditions and their potential impact on game performance',
            backstory="""You are an expert in analyzing how weather conditions affect NFL games.
                        You understand how different weather conditions impact team performance.""",
            tools=[
                Tool(
                    name="analyze_weather_impact",
                    func=WeatherAnalysisAgent.analyze_weather_impact,
                    description="Analyze weather impact on game performance"
                )
            ],
            verbose=True
        )

    @staticmethod
    def analyze_weather_impact(weather_data: Dict) -> Dict:
        impact_analysis = {
            'overall_impact': 'neutral',
            'passing_game_impact': 'neutral',
            'running_game_impact': 'neutral',
            'kicking_game_impact': 'neutral',
            'risk_factors': []
        }

        # Analyze temperature impact
        temp = weather_data.get('temperature', 70)
        if temp < 32:
            impact_analysis['overall_impact'] = 'negative'
            impact_analysis['passing_game_impact'] = 'negative'
            impact_analysis['risk_factors'].append('Cold weather may affect ball handling')
        
        # Analyze wind impact
        wind_speed = weather_data.get('wind_speed', 0)
        if wind_speed > 15:
            impact_analysis['passing_game_impact'] = 'negative'
            impact_analysis['kicking_game_impact'] = 'negative'
            impact_analysis['risk_factors'].append('High winds may affect passing and kicking')

        # Analyze precipitation
        if weather_data.get('precipitation_chance', 0) > 50:
            impact_analysis['passing_game_impact'] = 'negative'
            impact_analysis['running_game_impact'] = 'positive'
            impact_analysis['risk_factors'].append('Wet conditions favor running game')

        return impact_analysis
