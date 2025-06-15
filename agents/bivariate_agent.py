import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import uuid
from scipy.stats import (
    pearsonr, spearmanr, ttest_ind, f_oneway,
    mannwhitneyu, kruskal, normaltest
)
from scipy import stats
import statsmodels.api as sm

class BivariateAgent:
    def __init__(self):
        self.output_dir = Path("results/plots")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def analyze(self, df):
        """Analyze dataframe with multiple columns"""
        results = {
            'correlation': {},
            'inferential': {},
            'plots': {}
        }
        
        try:
            # Get only numerical columns
            numerical_cols = df.select_dtypes(include=[np.number]).columns
            
            # Only analyze if we have at least 2 numerical columns
            if len(numerical_cols) >= 2:
                # Analyze numerical-numerical relationships
                for i, col1 in enumerate(numerical_cols):
                    for col2 in numerical_cols[i+1:]:
                        # Calculate correlations
                        results['correlation'][f"{col1}_{col2}"] = {
                            'pearson': pearsonr(df[col1], df[col2])[0],
                            'spearman': spearmanr(df[col1], df[col2])[0]
                        }
                        
                        # Perform inferential analysis
                        results['inferential'][f"{col1}_{col2}"] = self._numerical_inferential(df[col1], df[col2])
                        
                        # Generate scatter plot with regression line
                        results['plots'][f"{col1}_{col2}"] = self._scatter_plot_with_regression(df, col1, col2)
                
        except Exception as e:
            print(f"Bivariate analysis error: {str(e)}")
            results['error'] = str(e)
            
        return results

    def _numerical_inferential(self, series1, series2):
        """Perform inferential analysis on numerical pairs"""
        results = {}
        
        # Test for normality only if sample size is sufficient
        if len(series1) >= 8 and len(series2) >= 8:
            _, p1 = normaltest(series1)
            _, p2 = normaltest(series2)
            results['normality_test'] = {
                'series1_pvalue': p1,
                'series2_pvalue': p2,
                'both_normal': p1 > 0.05 and p2 > 0.05
            }
        else:
            results['normality_test'] = {
                'note': 'Sample size too small for normality test (minimum 8 observations required)',
                'series1_size': len(series1),
                'series2_size': len(series2)
            }
        
        # Linear Regression
        try:
            # Ensure data is numeric and convert to numpy arrays
            X = np.array(series1, dtype=float)
            y = np.array(series2, dtype=float)
            
            # Add constant term for intercept
            X = sm.add_constant(X)
            
            # Fit the model
            model = sm.OLS(y, X).fit()
            
            results['regression'] = {
                'r_squared': model.rsquared,
                'adj_r_squared': model.rsquared_adj,
                'f_statistic': model.fvalue,
                'f_pvalue': model.f_pvalue,
                'coefficients': {
                    'intercept': model.params[0],
                    'slope': model.params[1]
                }
            }
        except Exception as e:
            results['regression'] = {
                'error': f'Regression analysis failed: {str(e)}'
            }
        
        # Correlation tests
        try:
            pearson_corr, pearson_p = pearsonr(series1, series2)
            spearman_corr, spearman_p = spearmanr(series1, series2)
            results['correlation_tests'] = {
                'pearson': {
                    'correlation': pearson_corr,
                    'p_value': pearson_p
                },
                'spearman': {
                    'correlation': spearman_corr,
                    'p_value': spearman_p
                }
            }
        except Exception as e:
            results['correlation_tests'] = {
                'error': f'Correlation tests failed: {str(e)}'
            }
        
        return results

    def _scatter_plot_with_regression(self, df, col1, col2):
        """Create scatter plot with regression line"""
        plt.figure(figsize=(10, 6))
        
        # Scatter plot
        plt.scatter(df[col1], df[col2], alpha=0.5)
        
        # Add regression line
        slope, intercept, r_value, p_value, std_err = stats.linregress(df[col1], df[col2])
        line = slope * df[col1] + intercept
        plt.plot(df[col1], line, color='red', label=f'y={slope:.2f}x+{intercept:.2f}')
        
        plt.title(f"{col1} vs {col2}\nR² = {r_value**2:.3f}")
        plt.xlabel(col1)
        plt.ylabel(col2)
        plt.legend()
        
        filename = self._generate_filename(f"{col1}_vs_{col2}", "scatter_regression")
        plt.savefig(filename)
        plt.close()
        return str(filename)

    def _numerical_analysis(self, df, col1, col2):
        return {
            'correlation': {
                'pearson': pearsonr(df[col1], df[col2])[0],
                'spearman': spearmanr(df[col1], df[col2])[0]
            },
            'scatter_plot': self._scatter_plot(df, col1, col2)
        }

    def _categorical_analysis(self, df, col1, col2):
        contingency_table = pd.crosstab(df[col1], df[col2])
        chi2, p, dof, _ = chi2_contingency(contingency_table)
        return {
            'contingency_table': contingency_table.to_dict(),
            'chi_square_test': {
                'chi2': chi2,
                'p_value': p,
                'degrees_of_freedom': dof
            }
        }

    def _mixed_analysis(self, df, col1, col2):
        num_col = col1 if pd.api.types.is_numeric_dtype(df[col1]) else col2
        cat_col = col2 if num_col == col1 else col1
        
        return {
            'grouped_stats': df.groupby(cat_col)[num_col].describe().to_dict(),
            'box_plot': self._box_plot(df, cat_col, num_col)
        }

    def _scatter_plot(self, df, col1, col2):
        plt.figure(figsize=(10, 6))
        plt.scatter(df[col1], df[col2])
        plt.title(f"{col1} vs {col2}")
        filename = self._generate_filename(f"{col1}_vs_{col2}", "scatter")
        plt.savefig(filename)
        plt.close()
        return str(filename)

    def _box_plot(self, df, cat_col, num_col):
        plt.figure(figsize=(10, 6))
        df.boxplot(column=num_col, by=cat_col)
        plt.title(f"{num_col} by {cat_col}")
        plt.suptitle('')
        filename = self._generate_filename(f"{cat_col}_vs_{num_col}", "boxplot")
        plt.savefig(filename)
        plt.close()
        return str(filename)

    def _generate_filename(self, cols, plot_type):
        return self.output_dir / f"{cols}_{plot_type}_{uuid.uuid4().hex[:8]}.png"
