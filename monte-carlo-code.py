# src/monte_carlo.py
import numpy as np
import pandas as pd
from scipy.optimize import minimize
import yfinance as yf
from typing import List, Tuple, Dict
import logging

class PortfolioOptimizer:
    def __init__(self, tickers: List[str], portfolio_size: float = 10_000_000):
        """
        Initialize Portfolio Optimizer
        
        Args:
            tickers (List[str]): List of asset tickers
            portfolio_size (float): Portfolio value in dollars
        """
        self.tickers = tickers
        self.portfolio_size = portfolio_size
        self.returns_data = None
        self.cov_matrix = None
        self.avg_returns = None
        
    def fetch_data(self, start_date: str, end_date: str) -> None:
        """Fetch historical price data"""
        data = pd.DataFrame()
        
        for ticker in self.tickers:
            stock = yf.Ticker(ticker)
            hist = stock.history(start=start_date, end=end_date)['Close']
            data[ticker] = hist
            
        # Calculate daily returns
        self.returns_data = data.pct_change().dropna()
        self.cov_matrix = self.returns_data.cov()
        self.avg_returns = self.returns_data.mean()
        
    def generate_portfolio(self) -> Dict[str, float]:
        """Generate random portfolio weights"""
        weights = np.random.random(len(self.tickers))
        weights /= np.sum(weights)
        return dict(zip(self.tickers, weights))
        
    def calculate_portfolio_metrics(self, weights: np.array) -> Tuple[float, float, float]:
        """
        Calculate portfolio return, volatility, and Sharpe ratio
        
        Returns:
            Tuple[float, float, float]: (return, volatility, sharpe_ratio)
        """
        portfolio_return = np.sum(self.avg_returns * weights) * 252
        portfolio_volatility = np.sqrt(
            np.dot(weights.T, np.dot(self.cov_matrix * 252, weights))
        )
        sharpe_ratio = portfolio_return / portfolio_volatility
        return portfolio_return, portfolio_volatility, sharpe_ratio
        
    def run_monte_carlo(self, num_simulations: int = 10000) -> pd.DataFrame:
        """
        Run Monte Carlo simulation
        
        Args:
            num_simulations (int): Number of simulations to run
            
        Returns:
            pd.DataFrame: Simulation results
        """
        results = []
        
        for _ in range(num_simulations):
            weights = list(self.generate_portfolio().values())
            ret, vol, sharpe = self.calculate_portfolio_metrics(np.array(weights))
            results.append({
                'return': ret,
                'volatility': vol,
                'sharpe_ratio': sharpe,
                'weights': weights
            })
            
        return pd.DataFrame(results)
        
    def optimize_portfolio(self, risk_free_rate: float = 0.02) -> Dict:
        """
        Optimize portfolio weights for maximum Sharpe ratio
        
        Args:
            risk_free_rate (float): Risk-free rate
            
        Returns:
            Dict: Optimized portfolio information
        """
        def neg_sharpe_ratio(weights):
            ret, vol, sharpe = self.calculate_portfolio_metrics(weights)
            return -sharpe
            
        constraints = (
            {'type': 'eq', 'fun': lambda x: np.sum(x) - 1}
        )
        bounds = tuple((0, 1) for _ in range(len(self.tickers)))
        
        # Initial guess (equal weights)
        initial_weights = np.array([1/len(self.tickers)] * len(self.tickers))
        
        # Optimize
        result = minimize(
            neg_sharpe_ratio,
            initial_weights,
            method='SLSQP',
            bounds=bounds,
            constraints=constraints
        )
        
        # Calculate metrics for optimized portfolio
        opt_return, opt_vol, opt_sharpe = self.calculate_portfolio_metrics(result.x)
        
        return {
            'weights': dict(zip(self.tickers, result.x)),
            'return': opt_return,
            'volatility': opt_vol,
            'sharpe_ratio': opt_sharpe
        }

# Main execution
if __name__ == "__main__":
    # Define asset universe
    tickers = ['SPY', 'AGG', 'VEA', 'VWO', 'GLD', 'REET']
    
    # Initialize optimizer
    optimizer = PortfolioOptimizer(tickers, portfolio_size=10_000_000)
    
    # Fetch historical data
    optimizer.fetch_data('2018-01-01', '2023-12-31')
    
    # Run Monte Carlo simulation
    simulation_results = optimizer.run_monte_carlo(num_simulations=10000)
    
    # Find optimal portfolio
    optimal_portfolio = optimizer.optimize_portfolio()
    
    # Save results
    simulation_results.to_csv('data/results/simulation_results.csv')
    pd.DataFrame([optimal_portfolio]).to_csv('data/results/optimal_portfolio.csv')
