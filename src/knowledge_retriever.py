# src/knowledge_retriever.py
import json
from pathlib import Path
import pandas as pd

class KnowledgeRetriever:
    def __init__(self):
        self.knowledge_dir = Path(__file__).parent.parent / "knowledge_base"
        self.univariate_rules = self._load_rules("univariate_tree.json")
        self.bivariate_rules = self._load_rules("bivariate_tree.json")
        self.statistical_methods = self._load_rules("statistical_methods.json")
        self.knowledge_base = self._load_knowledge_base()

    def _load_rules(self, filename):
        """Load JSON rules with robust error handling"""
        filepath = self.knowledge_dir / filename
        try:
            with open(filepath) as f:
                data = json.load(f)
                if "rules" not in data and "methods" not in data:
                    print(f"Error: Missing 'rules' or 'methods' key in {filename}")
                    return []
                return data.get("rules", data.get("methods", []))
        except FileNotFoundError:
            print(f"Warning: Missing knowledge file {filename}")
            return []
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON format in {filename}")
            return []
        except KeyError:
            print(f"Error: Missing required key in {filename}")
            return []

    def _load_knowledge_base(self):
        """Load the statistical methods knowledge base"""
        knowledge_path = self.knowledge_dir / "statistical_methods.json"
        with open(knowledge_path) as f:
            return json.load(f)

    def get_univariate_methods(self, data: pd.DataFrame) -> list:
        """Get appropriate univariate analysis methods based on data types"""
        methods = []
        for col in data.columns:
            if pd.api.types.is_numeric_dtype(data[col]):
                methods.append("descriptive_stats")
            else:
                methods.append("frequency_analysis")
        return list(set(methods))  # Remove duplicates

    def get_bivariate_methods(self, data: pd.DataFrame) -> list:
        """Get appropriate bivariate analysis methods based on data types"""
        methods = []
        numeric_cols = data.select_dtypes(include=['int64', 'float64']).columns
        
        # If we have at least 2 numeric columns, add correlation methods
        if len(numeric_cols) >= 2:
            methods.extend(["pearson_correlation", "spearman_correlation", "linear_regression"])
        
        # If we have exactly 2 numeric columns, add t-test
        if len(numeric_cols) == 2:
            methods.append("t_test")
        
        # If we have more than 2 numeric columns, add ANOVA
        if len(numeric_cols) > 2:
            methods.append("anova")
        
        return list(set(methods))  # Remove duplicates

    def get_method_info(self, method_name: str) -> dict:
        """Get information about a specific statistical method"""
        if method_name not in self.knowledge_base["methods"]:
            raise ValueError(f"Unknown statistical method: {method_name}")
        return self.knowledge_base["methods"][method_name]

    # Rest of the class remains the same...
