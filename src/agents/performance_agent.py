from crewai import Agent
from typing import Dict
from langchain.tools import Tool
import pandas as pd
import numpy as np

class PerformanceAnalysisAgent:
    @staticmethod
    def create() -> Agent:
        return Agent(
            role='Performance Trend Analysis Agent',
            goal='Analyze team performance trends and momentum',
            backstory="""You are an expert in analyzing NFL team performance trends. 
                        You specialize in evaluating recent game statistics and team momentum.""",
            tools=[
                Tool(
                    name="analyze_recent_games",
                    func=PerformanceAnalysisAgent.analyze_recent_games,
                    description="Analyze team's recent game performance"
                ),
                Tool(
                    name="calculate_momentum_score",
                    func=PerformanceAnalysisAgent.calculate_momentum_score,
                    description="Calculate team's current momentum score"
                )
            ],
            verbose=True
        )

    @staticmethod
    def analyze_performance(self, data: Dict) -> Dict:
        return {
            'task': 'Examine the current form and momentum...',
            'role': 'Performance Trend Analysis Agent',
            'priority': 'High',
            'findings': [
                # Real analysis results here
            ]
        }

    @staticmethod
    def analyze_recent_games(team_data: Dict) -> Dict:
        games = team_data.get('recent_games', [])
        
        analysis = {
            'total_yards': [],
            'points_scored': [],
            'third_down_conv': [],
            'first_downs': [],
            'trends': {}
        }
        
        for game in games:
            analysis['total_yards'].append(game.get('total_yards', 0))
            analysis['points_scored'].append(game.get('points', 0))
            analysis['third_down_conv'].append(game.get('third_down_rate', 0))
            analysis['first_downs'].append(game.get('first_downs', 0))
        
        # Calculate trends
        analysis['trends'] = {
            'yards_trend': np.gradient(analysis['total_yards']).tolist(),
            'scoring_trend': np.gradient(analysis['points_scored']).tolist(),
            'efficiency_trend': np.gradient(analysis['third_down_conv']).tolist()
        }
        
        return analysis

    @staticmethod
    def calculate_momentum_score(recent_games_analysis: Dict) -> float:
        # Weight factors for momentum calculation
        weights = {
            'yards_trend': 0.3,
            'scoring_trend': 0.4,
            'efficiency_trend': 0.3
        }
        
        trends = recent_games_analysis.get('trends', {})
        
        momentum_score = sum(
            np.mean(trends[key]) * weights[key]
            for key in weights.keys()
        )
        
        return float(momentum_score)
