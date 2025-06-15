import pandas as pd

def analyze_data(data):
    """Analyze the data and return insights"""
    insights = []
    
    # Get column names
    columns = data.columns.tolist()
    
    # Skip ID column if it exists
    if 'ID' in columns:
        columns.remove('ID')
    
    # Analyze each column
    for column in columns:
        # Skip if column is not numeric
        if not pd.api.types.is_numeric_dtype(data[column]):
            continue
            
        # Calculate statistics
        mean = data[column].mean()
        median = data[column].median()
        std = data[column].std()
        min_val = data[column].min()
        max_val = data[column].max()
        
        # Create insight for this column
        insight = f"Column '{column}':\n"
        insight += f"- Mean: {mean:.2f}\n"
        insight += f"- Median: {median:.2f}\n"
        insight += f"- Standard Deviation: {std:.2f}\n"
        insight += f"- Range: {min_val:.2f} to {max_val:.2f}\n"
        
        insights.append(insight)
    
    return "\n".join(insights)

def main():
    # Load the data
    data = pd.read_csv('data.csv')
    
    # Analyze the data
    insights = analyze_data(data)
    
    # Print the insights
    print("\nData Analysis Insights:")
    print(insights)

if __name__ == "__main__":
    main() 