# src/data_loader.py
import pandas as pd
import numpy as np

class DataLoader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = None
    
    def load_csv(self):
        """Load CSV file into DataFrame with robust error handling"""
        try:
            self.df = pd.read_csv(self.file_path)
            
            if self.df.empty:
                raise ValueError("CSV file is empty")
            
            # Preserve original dtypes for accurate type checking
            self.df = self.df.convert_dtypes()
            
            return self.df
            
        except FileNotFoundError:
            print(f"Error: File {self.file_path} not found")
            return None
        except pd.errors.ParserError:
            print(f"Error: Invalid CSV format in {self.file_path}")
            return None
        except Exception as e:
            print(f"Unexpected error loading {self.file_path}: {str(e)}")
            return None

    def get_column_metadata(self):
        """Get data types for analysis orchestration"""
        if self.df is None:
            return None
            
        return {
            col: 'numerical' if np.issubdtype(dtype, np.number) 
                 else 'categorical'
            for col, dtype in self.df.dtypes.items()
        }
