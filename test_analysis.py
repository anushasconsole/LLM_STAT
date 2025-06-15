import pandas as pd
import numpy as np
from src.analysis_orchestrator import AnalysisOrchestrator
import argparse

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Run statistical analysis on CSV data using LLM')
    parser.add_argument('--input', default='data.csv', help='Path to input CSV file')
    args = parser.parse_args()

    try:
        # Read CSV file
        print(f"Reading data from {args.input}...")
        data = pd.read_csv(args.input)
        
        # Initialize orchestrator
        orchestrator = AnalysisOrchestrator()

        # Run analysis
        print("\nStarting LLM-powered statistical analysis...")
        report_path = orchestrator.run_analysis(data)
        print(f"\nAnalysis complete! Report saved to: {report_path}")

        # Print data summary
        print("\nData Summary:")
        print("-------------")
        print(f"Number of rows: {len(data)}")
        print(f"Number of columns: {len(data.columns)}")
        print("\nColumns:")
        for col in data.columns:
            print(f"- {col} ({data[col].dtype})")
        
        print("\nSample of data:")
        print(data.head())
        
        print("\nBasic statistics:")
        print(data.describe())

    except FileNotFoundError:
        print(f"Error: Could not find file '{args.input}'")
        print("Please provide a valid CSV file path using --input")
    except Exception as e:
        print(f"Error during analysis: {str(e)}")

if __name__ == "__main__":
    main() 