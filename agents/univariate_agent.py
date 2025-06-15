import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import uuid

class UnivariateAgent:
    def __init__(self):
        self.output_dir = Path("results/plots")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def analyze(self, df, dtype):
        """Analyze single column dataframe"""
        results = {}
        col = df.columns[0]
        
        try:
            if dtype == 'numerical':
                results['summary'] = self._numerical_summary(df[col])
                results['plot'] = self._plot_numerical(df[col])
            else:
                results['summary'] = self._categorical_summary(df[col])
                results['plot'] = self._plot_categorical(df[col])
                
        except Exception as e:
            print(f"Error analyzing {col}: {str(e)}")
            results['error'] = str(e)
            
        return results

    def _numerical_summary(self, series):
        return {
            'mean': series.mean(),
            'median': series.median(),
            'std_dev': series.std(),
            'min': series.min(),
            'max': series.max(),
            'skewness': series.skew(),
            'kurtosis': series.kurtosis()
        }

    def _categorical_summary(self, series):
        counts = series.value_counts()
        return {
            'mode': counts.idxmax(),
            'unique_count': series.nunique(),
            'frequency_distribution': counts.to_dict()
        }

    def _plot_numerical(self, series):
        plt.figure(figsize=(10, 6))
        plt.hist(series, bins='auto')
        plt.title(f"Distribution of {series.name}")
        filename = self._generate_filename(series.name, "histogram")
        plt.savefig(filename)
        plt.close()
        return str(filename)

    def _plot_categorical(self, series):
        plt.figure(figsize=(10, 6))
        series.value_counts().plot(kind='bar')
        plt.title(f"Frequency Distribution of {series.name}")
        filename = self._generate_filename(series.name, "barchart")
        plt.savefig(filename)
        plt.close()
        return str(filename)

    def _generate_filename(self, colname, plot_type):
        return self.output_dir / f"{colname}_{plot_type}_{uuid.uuid4().hex[:8]}.png"
