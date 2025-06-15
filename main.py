# main.py
import argparse
import sys
import pandas as pd
from src.data_loader import DataLoader
from src.dtype_checker import analyze_data_types  # Updated import
from src.knowledge_retriever import KnowledgeRetriever
from src.analysis_orchestrator import AnalysisOrchestrator
from src.report_generator import ReportGenerator

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='LLM-Assisted Statistical Analysis Tool')
    parser.add_argument('--input', default='data.csv', help='Path to CSV file')
    parser.add_argument('--format', choices=['markdown', 'html'], default='markdown',
                       help='Output report format')
    args = parser.parse_args()

    # Initialize components
    loader = DataLoader(args.input)
    knowledge_retriever = KnowledgeRetriever()
    orchestrator = AnalysisOrchestrator()

    try:
        # Load data
        print(f"Loading data from {args.input}...")
        df = loader.load_csv()
        if df is None or df.empty:
            print("Error: Failed to load data or empty dataset")
            sys.exit(1)

        # Analyze data structure
        print("Analyzing data structure...")
        dtype_info = analyze_data_types(df)  # Use the correct function
        print(f"Detected structure: {dtype_info['structures']}")
        print(f"Column types: {dtype_info['columns']}")

        # Execute analysis
        print("Running analysis...")
        results = orchestrator.analyze_data(df)

        # Generate report
        print("Generating report...")
        report_path = orchestrator.generate_report(df, results, output_path=None)
        print(f"\nAnalysis complete! Report saved to: {report_path}")

    except Exception as e:
        print(f"Error during analysis: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
