# Change Point Analysis and Statistical Modeling of Time Series Data

## Project Overview
This project analyzes the impact of major political and economic events on Brent oil prices using Bayesian change point analysis. The goal is to identify significant structural breaks in oil prices and associate them with specific events.

## Project Structure
```
├── data/                      # All data files
├── notebooks/                 # Jupyter notebooks for analysis
├── src/                       # Source code
├── models/                    # Trained models
├── reports/                   # Generated reports and figures
└── dashboard/                 # Interactive dashboard
```

## Setup
1. Clone the repository
2. Create a virtual environment:
   ```
   conda env create -f environment.yml
   conda activate oil-analysis
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage
1. Run the Jupyter notebooks in order:
   - `01_eda.ipynb`: Exploratory data analysis
   - `02_preprocessing.ipynb`: Data cleaning and feature engineering
   - `03_analysis.ipynb`: Statistical analysis and modeling

2. To run the dashboard:
   ```
   cd dashboard/backend
   python app.py
   ```
   Then open `http://localhost:5000` in your browser.

## Data
- Source: [Add data source here]
- Raw data location: `data/raw/`
- Processed data: `data/processed/`

## Dependencies
- Python 3.8+
- Jupyter Notebook
- PyMC3
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Flask
- React (for dashboard)

## License
[Add license information]