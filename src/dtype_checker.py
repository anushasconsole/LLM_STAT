import numpy as np
import pandas as pd
import ollama

def is_identifier_column_llm(col_name: str) -> bool:
    """Uses Ollama (Mistral) to classify if a column name is likely an identifier."""
    prompt = f"""
You are a data expert. Decide if the column name '{col_name}' represents a unique identifier.
Respond with 'Yes' if it's an identifier, or 'No' if it is not.

Examples of identifiers: 'User ID', 'CustomerNumber', 'TransactionCode', 'UUID', 'Emp No'
Examples of non-identifiers: 'Age', 'Salary', 'Country', 'Feedback', 'Score'

Answer with only Yes or No.
"""
    try:
        response = ollama.chat(
            model='mistral',
            messages=[{"role": "user", "content": prompt}]
        )
        return response['message']['content'].strip().lower() == 'yes'
    except Exception as e:
        print(f"LLM check failed for column '{col_name}': {e}")
        return False

def analyze_data_types(df):
    """Analyze dataframe columns and return data type information"""
    n_cols = len(df.columns)
    
    result = {
        'structures': [],
        'columns': {}
    }

    n_rows = len(df)

    def is_identifier(col):
        """
        Determines if a column is likely an identifier based on:
        - uniqueness
        - same number of unique values as rows
        - name pattern (e.g., id, uuid, key)
        """
        is_unique = df[col].is_unique
        high_card = df[col].nunique() == n_rows
        name_match=is_identifier_column_llm(col)
        return is_unique and high_card and name_match

    # Count numeric columns (excluding likely identifier columns)
    numeric_cols = sum( 
        1 for col in df.columns 
        if pd.api.types.is_numeric_dtype(df[col]) and not is_identifier(col)
    )

    # Determine structure type
    if numeric_cols == 1:
        result['structures'].append('univariate')
    elif numeric_cols >= 2:
        result['structures'].extend(['univariate', 'bivariate'])

    # Classify each column
    for col in df.columns:
        if is_identifier(col):
            result['columns'][col] = 'identifier'
        elif pd.api.types.is_numeric_dtype(df[col]):
            result['columns'][col] = 'numerical'
        else:
            result['columns'][col] = 'categorical'

    return result
