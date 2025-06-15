# LLM-Assisted Statistical Analysis Tool

This project provides an LLM-assisted tool for performing statistical analysis on tabular data. It automatically identifies data types, skips irrelevant columns, and generates statistical insights.

## Project Structure

- `main.py`: The main entry point for running the analysis. It handles argument parsing, data loading, and orchestrates the analysis and report generation.
- `src/`:
    - `data_loader.py`: Handles loading data from CSV files.
    - `dtype_checker.py`: Analyzes the data to determine column types (numerical, categorical, identifier) and overall data structure (univariate, bivariate).
    - `llm_statistical_engine.py`: Contains the core logic for interacting with the LLM to perform statistical calculations and interpret results. It now includes logic to skip 'ID' and other non-numeric columns.
    - `knowledge_retriever.py`: (Assumed) Manages the retrieval of statistical methods from a knowledge base.
    - `analysis_orchestrator.py`: Orchestrates the statistical analysis, applying univariate and bivariate methods to relevant numeric columns.
    - `report_generator.py`: Generates a human-readable report from the analysis results.
- `data.csv`: Example dataset used for analysis.
- `reports/`: Directory where generated analysis reports are saved.

## Features

- **Automated Data Type Detection**: Identifies columns as numerical, categorical, or identifiers.
- **Intelligent Column Skipping**: Automatically skips 'ID' columns and other non-numeric data that are not suitable for statistical analysis.
- **Univariate and Bivariate Analysis**: Performs individual (univariate) analysis on numeric columns and pairwise (bivariate) analysis on combinations of numeric columns.
- **LLM-Powered Insights**: Utilizes an LLM (Mistral by default) to perform calculations and provide interpretations of statistical results.
- **Comprehensive Reporting**: Generates a detailed report summarizing the findings.

## `data.csv` Structure

The `data.csv` file contains sample student data with the following columns:

- `ID`: A unique identifier for each student (will be skipped in analysis).
- `Name`: The name of the student (categorical, will be skipped in analysis).
- `Score`: The student's score (numerical).
- `Hours_Studied`: The number of hours the student studied (numerical).
- `Previous_Sem_Score`: The student's score from the previous semester (numerical).

## Setup

To set up the project, you'll need to install the required Python packages. It's recommended to use a virtual environment.

1. **Clone the repository (if you haven't already):**
   ```bash
   git clone <repository_url>
   cd LLM_Stat
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install the dependencies:**
   Given the tools used, the dependencies include `pandas`, `numpy`, `langchain-ollama`, and `langchain-core` (which `langchain-ollama` depends on). You may need to create a `requirements.txt` file first if it doesn't exist.

   ```bash
   pip install pandas numpy langchain-ollama langchain-core
   ```
   *(If you encounter issues, consider creating a `requirements.txt` file with these dependencies and then running `pip install -r requirements.txt`)*

## Running the Analysis

To run the statistical analysis, execute the `main.py` script:

```bash
python main.py --input data.csv
```

You can also specify the output report format (default is markdown):

```bash
python main.py --input data.csv --format html
```

The analysis results and insights will be printed to the console, and a detailed report will be saved in the `reports/` directory.

## How it Works (Key Modifications)

During our session, we've made key modifications to ensure accurate and relevant statistical analysis:

1.  **`src/dtype_checker.py`**:
    -   Modified to correctly identify 'ID' columns as `'identifier'` instead of `'numerical'`.
    -   Improved logic to accurately detect both `'univariate'` and `'bivariate'` structures when there are two or more relevant numeric columns for analysis.

2.  **`src/llm_statistical_engine.py`**:
    -   The `_prepare_data_for_prompt` method was enhanced to ensure that before data is sent to the LLM for analysis, it first drops any 'ID' columns and then filters to include only truly numeric columns, preventing meaningless calculations on non-statistical identifiers or text.

3.  **`src/analysis_orchestrator.py`**:
    -   The `analyze_data` method was updated to leverage the improved column identification. It now explicitly filters out 'ID' and non-numeric columns, ensuring that univariate and bivariate analyses are only performed on relevant numerical data.

These changes ensure that the system intelligently processes your data, providing meaningful statistical insights without attempting calculations on irrelevant columns. 
