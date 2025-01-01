# NFL Game Analysis System

## Overview
This project is a multi-agent AI system that analyzes NFL games and predicts outcomes. It uses CrewAI framework to coordinate multiple AI agents, each specializing in different aspects of game analysis.

## Prerequisites
- Python 3.10 or higher
- OpenAI API key
- Sports Data API key
- Weather API key

## Quick Setup

1. **Clone the Repository**
```bash
git clone <repository-url>
cd nfls
```

2. **Set Up Python Environment**
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

3. **Configure API Keys**
Create a `.env` file in the project root:
```
OPENAI_API_KEY=your_openai_api_key_here
SPORTS_DATA_API_KEY=your_sports_data_api_key_here
WEATHER_API_KEY=your_weather_api_key_here
```

## Running the Analysis

### Basic Usage
```bash
python run.py --team1 "Team Name 1" --team2 "Team Name 2" --date "YYYY-MM-DD"
```

### Example Commands
```bash
# Analyze Super Bowl LVIII
python run.py --team1 "San Francisco 49ers" --team2 "Kansas City Chiefs" --date "2024-02-11"

# Analyze a regular season game
python run.py --team1 "Baltimore Ravens" --team2 "Buffalo Bills" --date "2024-01-20"
```

### Command Options
- `--team1`: First team name (required)
- `--team2`: Second team name (required)
- `--date`: Game date in YYYY-MM-DD format (optional, defaults to 7 days ahead)
- `--output`: Save analysis to a file (optional)

## What the Analysis Includes

1. **Team Performance Analysis**
   - Recent game statistics
   - Scoring trends
   - Offensive/defensive metrics

2. **Injury Analysis**
   - Current team injuries
   - Impact on performance
   - Depth chart implications

3. **Location & Weather Impact**
   - Stadium factors
   - Weather conditions
   - Travel considerations

4. **Historical Matchup Data**
   - Head-to-head records
   - Performance in similar conditions
   - Key matchup statistics

5. **Win Probability Prediction**
   - Overall prediction
   - Key factors
   - Confidence level

## Project Structure

```
nfls/
├── src/
│   ├── agents/         # AI agent definitions
│   ├── core/           # Core system components
│   ├── utils/          # Utility functions
│   └── tasks/          # Task definitions
├── requirements.txt    # Project dependencies
├── run.py             # Main execution script
└── .env               # Environment variables
```

## Troubleshooting

### Common Issues

1. **API Key Errors**
   ```
   Error: Invalid API key
   ```
   - Check if API keys in `.env` are correct
   - Verify API key permissions
   - Ensure no spaces around API keys

2. **Installation Issues**
   ```
   Error: No module found
   ```
   - Verify virtual environment is activated
   - Run `pip install -r requirements.txt` again
   - Check Python version compatibility

3. **Analysis Errors**
   ```
   Error: Could not fetch data
   ```
   - Verify team names are correct
   - Check internet connection
   - Confirm date format is YYYY-MM-DD

### Quick Fixes

1. **Reset Environment**
```bash
deactivate
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. **Clear Cache**
```bash
rm -rf __pycache__
rm nfl_analysis.log
```

3. **Update Dependencies**
```bash
pip install --upgrade -r requirements.txt
```

## Tips for Best Results

1. **Team Names**
   - Use official team names
   - Example: "San Francisco 49ers" not "49ers" or "SF 49ers"

2. **Date Format**
   - Always use YYYY-MM-DD
   - Example: "2024-02-11" not "02/11/2024"

3. **Analysis Time**
   - Analysis typically takes 2-3 minutes
   - More detailed analysis may take longer

## Support

If you encounter any issues:
1. Check the log file: `nfl_analysis.log`
2. Verify all prerequisites are met
3. Ensure API keys are valid
4. Check internet connectivity

## Version Information
- Current Version: 1.2.0
- Last Updated: January 2024
- Python Support: 3.10+