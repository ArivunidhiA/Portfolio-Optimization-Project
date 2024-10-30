# Portfolio Optimization using Monte Carlo Simulation

## Project Overview
This project implements a portfolio optimization strategy using Monte Carlo simulation to maximize returns while managing risk for a $10M multi-asset portfolio. The model runs 10,000 simulations to find the optimal asset allocation strategy.

## Data Sources
1. Yahoo Finance API (yfinance)
   - Historical price data for assets
   - Trading volume
   - Dividend history
2. Federal Reserve Economic Data (FRED)
   - Risk-free rates
   - Economic indicators
3. Sample Portfolio Assets:
   - SPY (S&P 500 ETF)
   - AGG (US Aggregate Bond ETF)
   - VEA (Developed Markets ETF)
   - VWO (Emerging Markets ETF)
   - GLD (Gold ETF)
   - REET (Real Estate ETF)

## Repository Structure
```
portfolio_optimization/
│
├── data/
│   ├── raw/                  # Raw data downloads
│   ├── processed/            # Cleaned and processed data
│   └── results/              # Simulation results
│
├── src/
│   ├── data_collection.py    # Data gathering scripts
│   ├── data_processing.py    # Data cleaning and processing
│   ├── monte_carlo.py        # Monte Carlo simulation
│   ├── optimization.py       # Portfolio optimization
│   └── visualization.py      # Plotting and visualization
│
├── notebooks/
│   ├── 1_data_analysis.ipynb
│   ├── 2_portfolio_simulation.ipynb
│   └── 3_results_analysis.ipynb
│
├── sql/
│   ├── schema.sql           # Database schema
│   └── queries.sql          # Analysis queries
│
├── visualization/
│   ├── dashboard.twb        # Tableau workbook
│   └── charts/              # Exported visualizations
│
├── requirements.txt
├── README.md
└── .gitignore
```

## Key Features
1. **Data Processing**
   - Historical price data collection
   - Returns calculation
   - Risk metrics computation

2. **Portfolio Analysis**
   - Asset correlation analysis
   - Risk-return profiles
   - Sharpe ratio optimization

3. **Monte Carlo Simulation**
   - 10,000 portfolio combinations
   - Efficient frontier calculation
   - Optimal weight distribution

4. **Visualization**
   - Interactive Tableau dashboard
   - Risk-return scatter plots
   - Efficient frontier curve
   - Portfolio composition charts

## Setup Instructions
1. Clone the repository
```bash
git clone https://github.com/yourusername/portfolio-optimization.git
cd portfolio-optimization
```

2. Create and activate virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Set up database
```bash
python src/setup_database.py
```

5. Run data collection
```bash
python src/data_collection.py
```

## Usage
1. Data Collection and Processing
```bash
python src/data_collection.py --start-date 2018-01-01
python src/data_processing.py
```

2. Run Monte Carlo Simulation
```bash
python src/monte_carlo.py --simulations 10000 --portfolio-size 10000000
```

3. Generate Results
```bash
python src/optimization.py
python src/visualization.py
```

## Requirements
- Python 3.8+
- PostgreSQL 12+
- Tableau Desktop 2021.4+

Required Python packages:
- pandas
- numpy
- scipy
- yfinance
- sqlalchemy
- plotly
- scikit-learn

## Results
- Initial Portfolio Return: X%
- Optimized Portfolio Return: X + 22%
- Sharpe Ratio Improvement: Y%
- Risk Reduction: Z%

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing
1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request
