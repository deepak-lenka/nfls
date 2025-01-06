# Multi-Agent System for NFL Team Performance and Winning Probability Analysis

## Project Overview

This project involves the development of a **multi-agent system** designed to analyze NFL team performance and predict winning probabilities. The implementation leverages open-source frameworks, such as CrewAI, to coordinate the actions of multiple agents in a collaborative environment.

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

## System Features

### 1. Data Scraping
- Collect relevant NFL data from various online sources.
- Employ efficient methods, including potential "hacky" approaches, to gather comprehensive datasets. For example:
  - **APIs**: Use available APIs to fetch team statistics, player data, and historical game outcomes.
  - **Web Scraping**: Utilize tools like BeautifulSoup or Selenium to extract information from sports websites and forums.
  - **Data Aggregation**: Combine data from multiple sources to ensure completeness and accuracy, leveraging scripts to automate repetitive tasks.

### 2. Data Analysis
- Process the scraped data to extract actionable insights.
- Identify key performance indicators (KPIs) and other metrics impacting team performance.

### 3. Probability Calculation
- Develop algorithms to create custom agents focused on specific analytical sub-agendas.
- Compute team winning probabilities using the collected and processed data.

### 4. Multi-Agent Architecture
- Utilize a **multi-agent system architecture** for task division and collaboration.
- Implement the system using CrewAI or similar frameworks to coordinate agent workflows.

## Enhancements

1. **Retrieval-Augmented Generation (RAG)**
   - Integrate RAG techniques for advanced data retrieval and analysis.
   - **Benefits**: Improves the relevance and accuracy of retrieved data by leveraging contextual understanding.
   - **Use Case**: Automatically fetching and synthesizing team performance metrics from multiple sources.

2. **Directed Acyclic Graphs (DAGs)**
   - Use DAGs to define and manage agent workflows systematically.
   - **Benefits**: Ensures a clear and non-cyclic flow of tasks, improving reliability and efficiency in multi-agent coordination.
   - **Use Case**: Orchestrating data scraping, processing, and analysis in a structured manner.

3. **Embedding Systems and Vector Stores**
   - Incorporate embeddings for improved data representation and enhanced querying capabilities.
   - **Benefits**: Enables semantic search and similarity analysis, enhancing insight generation.
   - **Use Case**: Comparing player performance metrics across seasons or teams.

## Deliverables

1. **Code**
   - Fully functional multi-agent system.
2. **Documentation**
   - Explanation of system architecture and agent interactions.
   - User guide detailing setup, execution, and interpretation of results.
3. **Sample Outputs**
   - Demonstrations of system capabilities with real or test data, such as:
     - **Example 1**: A tabular summary showing team statistics, player performance metrics, and calculated probabilities for the upcoming matches.
     - **Example 2**: A graphical visualization (e.g., bar charts or pie charts) comparing the winning probabilities of different teams.
     - **Example 3**: A textual report summarizing insights like "Team A has a 75% chance of winning against Team B based on current performance metrics and historical data."

## Project Structure

```
nfls/
├── src/
│   ├── agents/         # AI agent definitions
│   ├── core/           # Core system components
│   ├── utils/          # Utility functions
│   └── tasks/          # Task definitions
├── requirements.txt    # Project dependencies
├── run.py              # Main execution script
└── .env                # Environment variables
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
- Python Support: 3.10+.

---

This system provides an innovative approach to leveraging multi-agent systems for predictive sports analytics, ensuring modularity, scalability, and actionable insights for NFL enthusiasts and analysts.
