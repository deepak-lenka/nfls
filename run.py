from dotenv import load_dotenv
import os
from src.main import NFLAnalysisSystem

def check_environment():
    """Check if all required API keys are present"""
    required_vars = ["OPENAI_API_KEY"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

def main():
    try:
        # Load and check environment variables
        load_dotenv()
        check_environment()
        
        # Initialize the system
        system = NFLAnalysisSystem()
        
        # Run the analysis
        print("Starting NFL game analysis...")
        print("Gathering data from sources...")
        
        # Get results
        result = system.analyze_game()
        
        # Print results
        print("\n" + "="*50)
        print("ANALYSIS RESULTS")
        print("="*50 + "\n")
        print(result)
        
    except ValueError as e:
        print(f"Environment Error: {str(e)}")
    except Exception as e:
        print(f"Error running analysis: {str(e)}")
        
if __name__ == "__main__":
    main()