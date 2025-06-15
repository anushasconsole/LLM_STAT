import numpy as np
import pandas as pd

def analyze_data_types(df):
    """Analyze dataframe columns and return data type information"""
    n_cols = len(df.columns)
    
    result = {
        'structures': [],
        'columns': {}
    }
    
    # Count numeric columns
    numeric_cols = sum(1 for col in df.columns if pd.api.types.is_numeric_dtype(df[col]) and col.upper() != 'ID')
    
    # Determine structure
    if numeric_cols == 1:
        result['structures'].append('univariate')
    elif numeric_cols >= 2:
        # If we have 2 or more numeric columns, we can do both univariate and bivariate analysis
        result['structures'].extend(['univariate', 'bivariate'])

    # Determine column types
    for col in df.columns:
        # Check if column is an ID column
        if col.upper() == 'ID' or col.lower() == 'id':
            result['columns'][col] = 'identifier'
        else:
            result['columns'][col] = 'numerical' if pd.api.types.is_numeric_dtype(df[col]) else 'categorical'
    
    return result

