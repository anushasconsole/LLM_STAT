import json
from pathlib import Path
from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate
import pandas as pd
import numpy as np

class LLMStatisticalEngine:
    def __init__(self):
        self.llm = OllamaLLM(model="mistral")
        self.knowledge_base = self._load_knowledge_base()
        self.prompt_template = PromptTemplate(
            input_variables=["method", "implementation", "data", "calculation_type"],
            template="""You are a statistical analysis expert. Perform the following statistical calculation on the provided data.

Method: {method}
Implementation Steps: {implementation}
Calculation Type: {calculation_type}

Data:
{data}

IMPORTANT INSTRUCTIONS:
1. Perform the exact calculation steps as specified in the implementation.
2. Return a JSON object with the numerical results AND their interpretation.
3. Format your response as a valid JSON object with two sections:
   - results: containing the numerical values
   - interpretation: containing the statistical conclusions

Example response format:
{{
    "results": {{
        "statistic_name": value,
        "p_value": value,
        "confidence_interval": [lower, upper]
    }},
    "interpretation": {{
        "conclusion": "Statistical conclusion based on the results",
        "significance": "Whether the results are statistically significant",
        "practical_meaning": "Practical interpretation of the findings"
    }}
}}

Now, perform the calculation and return the results with interpretation in JSON format.
"""
        )

    def _load_knowledge_base(self):
        """Load the statistical methods knowledge base"""
        knowledge_path = Path(__file__).parent.parent / "knowledge_base" / "statistical_methods.json"
        with open(knowledge_path) as f:
            return json.load(f)

    def _prepare_data_for_prompt(self, data):
        """Convert data into a format suitable for the LLM prompt"""
        if isinstance(data, pd.DataFrame):
            # Create a copy of the dataframe
            df = data.copy()
            
            # Skip ID columns and non-numeric columns
            numeric_columns = []
            for col in df.columns:
                # Skip if it's an ID column
                if col.upper() == 'ID' or col.lower() == 'id':
                    continue
                # Only keep numeric columns
                if pd.api.types.is_numeric_dtype(df[col]):
                    numeric_columns.append(col)
            
            # Keep only the numeric columns
            df = df[numeric_columns]
            
            return df.to_string()
        elif isinstance(data, (pd.Series, np.ndarray)):
            return str(data.tolist())
        return str(data)

    def analyze(self, method_name, data, calculation_type="full"):
        """Perform statistical analysis using the LLM"""
        if method_name not in self.knowledge_base["methods"]:
            raise ValueError(f"Unknown statistical method: {method_name}")

        method_info = self.knowledge_base["methods"][method_name]
        
        # Prepare the prompt
        prompt = self.prompt_template.format(
            method=method_info["description"],
            implementation=method_info["implementation"],
            data=self._prepare_data_for_prompt(data),
            calculation_type=calculation_type
        )

        print(f"\nExecuting {method_name} analysis...")
        print(f"Data: {self._prepare_data_for_prompt(data)}")
        
        # Get LLM response
        try:
            response = self.llm(prompt)
            print(f"LLM Response: {response}")
            
            # Try to parse the response as JSON
            try:
                results = json.loads(response)
                return results
            except json.JSONDecodeError:
                # If the response isn't valid JSON, try to extract numerical values
                import re
                numbers = re.findall(r"[-+]?\d*\.\d+|\d+", response)
                if numbers:
                    return {
                        "results": {
                            "raw_response": response,
                            "extracted_values": [float(n) for n in numbers]
                        },
                        "interpretation": {
                            "conclusion": "Could not parse full response",
                            "significance": "Unknown",
                            "practical_meaning": "Results could not be fully interpreted"
                        }
                    }
                return {
                    "results": {"error": "Could not parse LLM response as JSON or extract numbers"},
                    "interpretation": {
                        "conclusion": "Analysis failed",
                        "significance": "Unknown",
                        "practical_meaning": "Could not interpret results"
                    }
                }
        except Exception as e:
            return {
                "results": {"error": f"LLM analysis failed: {str(e)}"},
                "interpretation": {
                    "conclusion": "Analysis failed",
                    "significance": "Unknown",
                    "practical_meaning": "Could not interpret results"
                }
            }

    def get_available_methods(self):
        """Return list of available statistical methods"""
        return list(self.knowledge_base["methods"].keys())

    def get_method_info(self, method_name):
        """Get information about a specific statistical method"""
        if method_name not in self.knowledge_base["methods"]:
            raise ValueError(f"Unknown statistical method: {method_name}")
        return self.knowledge_base["methods"][method_name] 