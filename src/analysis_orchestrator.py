import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
from .llm_statistical_engine import LLMStatisticalEngine
from .report_generator import ReportGenerator
from .knowledge_retriever import KnowledgeRetriever

class AnalysisOrchestrator:
    def __init__(self):
        self.llm_engine = LLMStatisticalEngine()
        self.knowledge_retriever = KnowledgeRetriever()

    def _generate_dtype_info(self, data: pd.DataFrame):
        # Simple dtype info generator
        columns = {col: str(dtype) for col, dtype in data.dtypes.items()}
        structures = []
        if data.shape[1] == 1:
            structures.append('univariate')
        elif data.shape[1] > 1:
            structures.extend(['univariate', 'bivariate'])
        return {'columns': columns, 'structures': structures}

    def analyze_data(self, data: pd.DataFrame) -> dict:
        results = {'univariate': {}, 'bivariate': {}}
        univariate_methods = self.knowledge_retriever.get_univariate_methods(data)
        bivariate_methods = self.knowledge_retriever.get_bivariate_methods(data)
        
        # Get valid columns for analysis (skip ID and non-numeric columns)
        valid_columns = []
        for col in data.columns:
            # Skip if it's an ID column
            if col.upper() == 'ID' or col.lower() == 'id':
                continue
            # Only keep numeric columns
            if pd.api.types.is_numeric_dtype(data[col]):
                valid_columns.append(col)
        
        # Univariate analysis
        for col in valid_columns:
            results['univariate'][col] = {}
            for method in univariate_methods:
                try:
                    method_results = self.llm_engine.analyze(
                        method,
                        data[col],
                        calculation_type="univariate"
                    )
                    results['univariate'][col][method] = method_results
                except Exception as e:
                    results['univariate'][col][method] = {"error": str(e)}
        
        # Bivariate analysis
        for i, col1 in enumerate(valid_columns):
            for col2 in valid_columns[i+1:]:
                pair_key = f"{col1}_vs_{col2}"
                results['bivariate'][pair_key] = {}
                for method in bivariate_methods:
                    try:
                        method_results = self.llm_engine.analyze(
                            method,
                            data[[col1, col2]],
                            calculation_type="bivariate"
                        )
                        results['bivariate'][pair_key][method] = method_results
                    except Exception as e:
                        results['bivariate'][pair_key][method] = {"error": str(e)}
        
        return results

    def generate_report(self, data: pd.DataFrame, results: dict, output_path: str = None) -> str:
        """Generate a comprehensive report using LLM"""
        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"reports/report_{timestamp}.md"
            
        # Ensure reports directory exists
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        
        dtype_info = self._generate_dtype_info(data)
        report_generator = ReportGenerator(results, dtype_info)
        report = '\n'.join(report_generator.report)
        
        # Save report
        with open(output_path, 'w') as f:
            f.write(report)
            
        return output_path

    def run_analysis(self, data: pd.DataFrame, output_path: str = None) -> str:
        """Run complete analysis pipeline"""
        # Perform analysis
        results = self.analyze_data(data)
        
        # Generate and save report
        report_path = self.generate_report(data, results, output_path)
        
        return report_path
