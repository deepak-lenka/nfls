#!/usr/bin/env python3
import argparse
from src.main import NFLAnalysisSystem
from datetime import datetime, timedelta
import json
import logging
import os
import re
from dotenv import load_dotenv

def setup_logging():
    """Setup logging configuration"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('nfl_analysis.log'),
            logging.StreamHandler()
        ]
    )

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='NFL Game Analysis System')
    parser.add_argument('--team1', required=True, help='First team name')
    parser.add_argument('--team2', required=True, help='Second team name')
    parser.add_argument('--date', help='Game date (YYYY-MM-DD)', default=None)
    parser.add_argument('--output', help='Output file path for analysis results', default=None)
    return parser.parse_args()

def format_output(result):
    """Format the analysis output for display"""
    output = []
    
    # Task Information
    output.append("\nNFL Game Analysis Results\n")
    output.append("=" * 80 + "\n")
    
    # Process each task result
    for task_output in result.tasks_output:
        # Split the output into sections
        sections = str(task_output).split("\n\n")
        
        # Add each section
        for section in sections:
            if section.strip():
                # Remove ANSI color codes
                clean_section = re.sub(r'\x1b\[[0-9;]*[a-zA-Z]', '', section)
                # Remove # Agent: and ## Task: prefixes
                clean_section = re.sub(r'^#+ (?:Agent|Task): ', '', clean_section)
                output.append(clean_section.strip())
                output.append("-" * 80)
    
    return "\n".join(output)

def main():
    """Main execution function"""
    # Load environment variables
    load_dotenv()
    
    # Check for required API keys
    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError("OPENAI_API_KEY environment variable is required")
    
    # Setup logging
    setup_logging()
    logger = logging.getLogger(__name__)
    
    try:
        # Parse arguments
        args = parse_arguments()
        
        # Set default game date if not provided
        if not args.date:
            args.date = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
        
        # Initialize analysis system
        system = NFLAnalysisSystem()
        
        # Run analysis
        logger.info(f"Starting analysis for {args.team1} vs {args.team2} on {args.date}")
        result = system.analyze_game(args.team1, args.team2, args.date)
        
        # Format output
        output = format_output(result)
        
        # Save or display results
        if args.output:
            with open(args.output, 'w') as f:
                if args.output.endswith('.json'):
                    json.dump(result, f, indent=2)
                else:
                    f.write(output)
            logger.info(f"Analysis results saved to {args.output}")
        else:
            print(output)
            
    except Exception as e:
        logger.error(f"Error during analysis: {str(e)}")
        raise

if __name__ == "__main__":
    main()