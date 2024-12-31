# NFL Analysis System

A sophisticated NFL game analysis system utilizing multi-agent architecture to analyze team performance, predict winning probabilities, and assess various factors influencing game outcomes.

## Features

- **Multi-Agent Analysis**: Utilizes specialized AI agents for comprehensive game analysis:
  - Performance Analysis Agent
  - Injury Impact Agent
  - Location/Venue Analysis Agent
  - Matchup Analysis Agent
  - Weather Impact Agent

- **Real-Time Data**: Integrates with Sports Data API for up-to-date statistics and information
- **Comprehensive Analysis**: Evaluates multiple factors including:
  - Team Performance Metrics
  - Injury Reports
  - Weather Conditions
  - Home/Away Performance
  - Historical Matchups

## Prerequisites

- Python 3.10 or higher
- Sports Data API key
- OpenAI API key

## Installation

1. Clone the repository:
```bash
git clone https://github.com/deepak-lenka/nfls.git
cd nfls
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root and add your API keys:
```
SPORTS_DATA_API_KEY=your_sports_data_api_key
OPENAI_API_KEY=your_openai_api_key
```

## Usage

Run the analysis using either method:

1. Using Python directly:
```bash
python run.py --team1 "Team Name 1" --team2 "Team Name 2" --date "YYYY-MM-DD"
```

2. Using the shell script:
```bash
chmod +x run_analysis.sh
./run_analysis.sh
```

## Output Format

The system provides detailed analysis including:
- Performance metrics for both teams
- Injury impact assessment
- Weather conditions and their effects
- Home/away performance analysis
- Historical matchup statistics
- Overall game prediction

## Project Structure

```
nfls/
├── src/
│   ├── agents/            # AI agent implementations
│   ├── core/             # Core system configuration
│   ├── tasks/            # Task definitions
│   └── utils/            # Utility functions and data scraping
├── run.py                # Main execution script
├── run_analysis.sh       # Shell script for easy execution
└── requirements.txt      # Project dependencies
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- CrewAI framework for multi-agent orchestration
- Sports Data API for real-time sports data
- OpenAI for language model capabilities
