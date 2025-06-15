# src/report_generator.py
import os
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib import image as mpimg
import pandas as pd
import numpy as np
from pathlib import Path
from IPython.display import display, Markdown, HTML
import base64
from io import BytesIO

class ReportGenerator:
    def __init__(self, results, dtype_info):
        self.results = results
        self.dtype_info = dtype_info
        self.report = []
        self.output_dir = "reports"
        self.notebook_output = []
        os.makedirs(self.output_dir, exist_ok=True)
        self._generate_report()

    def _generate_report(self):
        """Generate the complete report"""
        self._add_header()
        self._add_univariate_section()
        self._add_bivariate_section()
        
    def _add_header(self):
        """Add report header with metadata"""
        self.report.append(f"# Statistical Analysis Report\n")
        self.report.append(f"**Generated at**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        self.report.append(f"**Dataset Structure**: {', '.join(self.dtype_info['structures']).title()}\n")
        self.report.append(f"**Columns Analyzed**: {list(self.dtype_info['columns'].keys())}\n")
        self.report.append("\n---\n")
        
        # For notebook display
        self.notebook_output.append(Markdown(f"# Statistical Analysis Report\n"))
        self.notebook_output.append(Markdown(f"**Generated at**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"))
        self.notebook_output.append(Markdown(f"**Dataset Structure**: {', '.join(self.dtype_info['structures']).title()}\n"))
        self.notebook_output.append(Markdown(f"**Columns Analyzed**: {list(self.dtype_info['columns'].keys())}\n"))
        self.notebook_output.append(Markdown("---\n"))

    def _add_univariate_section(self):
        """Format univariate analysis results"""
        if 'univariate' not in self.results:
            return
        self.report.append("## Univariate Analysis\n")
        for col, analysis in self.results['univariate'].items():
            self.report.append(f"### Column: {col}\n")
            if not analysis:
                self.report.append("No results.\n\n---\n")
                continue
            for method, result in analysis.items():
                self.report.append(f"**Method:** {method}\n")
                if isinstance(result, dict):
                    if "results" in result and "interpretation" in result:
                        self.report.append("#### Results:\n")
                        for k, v in result["results"].items():
                            self.report.append(f"- {k}: {v}\n")
                        self.report.append("\n#### Interpretation:\n")
                        for k, v in result["interpretation"].items():
                            self.report.append(f"- {k}: {v}\n")
                    elif "conclusions" in result and isinstance(result["conclusions"], dict):
                        for k, v in result.items():
                            if k == "conclusions":
                                self.report.append("\n**Conclusion:** " + str(result["conclusions"].get("interpretation", "")) + "\n")
                                self.report.append("**Significance:** " + str(result["conclusions"].get("significance", "")) + "\n")
                                self.report.append("**Confidence:** " + str(result["conclusions"].get("confidence", "")) + "\n")
                            else:
                                self.report.append(f"- {k}: {v}\n")
                    else:
                        for k, v in result.items():
                            self.report.append(f"- {k}: {v}\n")
                else:
                    self.report.append(f"- Result: {result}\n")
            self.report.append("\n---\n")

    def _add_bivariate_section(self):
        """Format bivariate analysis results"""
        if 'bivariate' not in self.results:
            return
        self.report.append("## Bivariate Analysis\n")
        for pair, analysis in self.results['bivariate'].items():
            self.report.append(f"### Pair: {pair}\n")
            if not analysis:
                self.report.append("No results.\n\n---\n")
                continue

            # Add t-test results
            if 't_test' in analysis:
                self.report.append("**Method:** t_test\n")
                result = analysis['t_test']
                if isinstance(result, dict):
                    for k, v in result.items():
                        if k != 'conclusions':
                            self.report.append(f"- {k}: {v}\n")
                    if 'conclusions' in result:
                        self.report.append("\n**Conclusion:** " + str(result['conclusions'].get('interpretation', '')) + "\n")
                        self.report.append("**Significance:** " + str(result['conclusions'].get('significance', '')) + "\n")
                        self.report.append("**Confidence:** " + str(result['conclusions'].get('confidence', '')) + "\n")
                self.report.append("\n---\n")

            # Add Pearson correlation results
            if 'pearson_correlation' in analysis:
                self.report.append("**Method:** pearson_correlation\n")
                result = analysis['pearson_correlation']
                if isinstance(result, dict):
                    for k, v in result.items():
                        if k != 'conclusions':
                            self.report.append(f"- {k}: {v}\n")
                    if 'conclusions' in result:
                        self.report.append("\n**Conclusion:** " + str(result['conclusions'].get('interpretation', '')) + "\n")
                        self.report.append("**Significance:** " + str(result['conclusions'].get('significance', '')) + "\n")
                        self.report.append("**Confidence:** " + str(result['conclusions'].get('confidence', '')) + "\n")
                self.report.append("\n---\n")

            # Add Spearman correlation results
            if 'spearman_correlation' in analysis:
                self.report.append("**Method:** spearman_correlation\n")
                result = analysis['spearman_correlation']
                if isinstance(result, dict):
                    for k, v in result.items():
                        if k != 'conclusions':
                            self.report.append(f"- {k}: {v}\n")
                    if 'conclusions' in result:
                        self.report.append("\n**Conclusion:** " + str(result['conclusions'].get('interpretation', '')) + "\n")
                        self.report.append("**Significance:** " + str(result['conclusions'].get('significance', '')) + "\n")
                        self.report.append("**Confidence:** " + str(result['conclusions'].get('confidence', '')) + "\n")
                self.report.append("\n---\n")

            # Add linear regression results
            if 'linear_regression' in analysis:
                self.report.append("**Method:** linear_regression\n")
                result = analysis['linear_regression']
                if isinstance(result, dict):
                    for k, v in result.items():
                        if k != 'conclusions':
                            self.report.append(f"- {k}: {v}\n")
                    if 'conclusions' in result:
                        self.report.append("\n**Conclusion:** " + str(result['conclusions'].get('interpretation', '')) + "\n")
                        self.report.append("**Significance:** " + str(result['conclusions'].get('significance', '')) + "\n")
                        self.report.append("**Confidence:** " + str(result['conclusions'].get('confidence', '')) + "\n")
                self.report.append("\n---\n")

    def generate_markdown(self):
        """Return the already generated markdown report"""
        return "\n".join(self.report)

    def generate_html(self):
        """Convert markdown to HTML using basic formatting"""
        md = self.generate_markdown()
        html = md.replace("\n# ", "\n<h1>").replace("\n## ", "\n<h2>").replace("\n### ", "\n<h3>")
        html = html.replace("\n**", "<strong>").replace("**\n", "</strong>")
        html = html.replace("\n- ", "\n<li>").replace("\n", "</li>\n")
        html = html.replace("![", "<img src='").replace("](", "' alt='Plot' style='width:600px;'>")
        return f"<html><body>{html}</body></html>"

    def save_report(self, format='markdown'):
        """Save report to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(self.output_dir, f"report_{timestamp}")
        
        if format == 'markdown':
            content = self.generate_markdown()
            filename += ".md"
        elif format == 'html':
            content = self.generate_html()
            filename += ".html"
        
        with open(filename, 'w') as f:
            f.write(content)
        
        print(f"Report saved to: {filename}")
        return filename

    def show_in_notebook(self):
        """Display report directly in Jupyter notebooks"""
        for output in self.notebook_output:
            display(output)

    def display_notebook(self):
        """Display the report in a Jupyter notebook"""
        for output in self.notebook_output:
            display(output)
