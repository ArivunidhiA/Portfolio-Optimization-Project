-- schema.sql

-- Asset prices table
CREATE TABLE asset_prices (
    id SERIAL PRIMARY KEY,
    ticker VARCHAR(10) NOT NULL,
    date DATE NOT NULL,
    close_price DECIMAL(10,2) NOT NULL,
    volume BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (ticker, date)
);

-- Portfolio allocations table
CREATE TABLE portfolio_allocations (
    id SERIAL PRIMARY KEY,
    simulation_id INTEGER NOT NULL,
    ticker VARCHAR(10) NOT NULL,
    weight DECIMAL(5,4) NOT NULL,
    amount DECIMAL(15,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Simulation results table
CREATE TABLE simulation_results (
    id SERIAL PRIMARY KEY,
    simulation_id INTEGER NOT NULL,
    portfolio_return DECIMAL(10,4) NOT NULL,
    portfolio_volatility DECIMAL(10,4) NOT NULL,
    sharpe_ratio DECIMAL(10,4) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Optimal portfolio table
CREATE TABLE optimal_portfolio (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    ticker VARCHAR(10) NOT NULL,
    weight DECIMAL(5,4) NOT NULL,
    amount DECIMAL(15,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Performance tracking table
CREATE TABLE portfolio_performance (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    portfolio_value DECIMAL(15,2) NOT NULL,
    daily_return DECIMAL(10,4),
    cumulative_return DECIMAL(10,4),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Analysis queries
-- queries.sql

-- Calculate daily returns
SELECT 
    date,
    ticker,
    close_price,
    (close_price - LAG(close_price) OVER (PARTITION BY ticker ORDER BY date)) / 
        LAG(close_price) OVER (PARTITION BY ticker ORDER BY date) as daily_return
FROM asset_prices
ORDER BY ticker, date;

-- Get best performing simulation
SELECT 
    sr.simulation_id,
    sr.portfolio_return,
    sr.portfolio_volatility,
    sr.sharpe_ratio,
    pa.ticker,
    pa.weight,
    pa.amount
FROM simulation_results sr
JOIN portfolio_allocations pa ON sr.simulation_id = pa.simulation_id
WHERE sr.sharpe_ratio = (
    SELECT MAX(sharpe_ratio) 
    FROM simulation_results
)
ORDER BY pa.weight DESC;

-- Track portfolio performance
SELECT 
    date,
    portfolio_value,
    daily_return,
    cumulative_return,
    AVG(daily_return) OVER (ORDER BY date ROWS BETWEEN 30 PRECEDING AND CURRENT ROW) as rolling_30d_return
FROM portfolio_performance
ORDER BY date DESC;

-- Calculate correlation matrix
WITH daily_returns AS (
    SELECT 
        date,
        ticker,
        (close_price - LAG(close_price) OVER (PARTITION BY ticker ORDER BY date)) / 
            LAG(close_price) OVER (PARTITION BY ticker ORDER BY date) as return
    FROM asset_prices
)
SELECT 
    a.ticker as ticker_a,
    b.ticker as ticker_b,
    CORR(a.return, b.return) as correlation
FROM daily_returns a
JOIN daily_returns b ON a.date = b.date
WHERE a.ticker < b.ticker
GROUP BY a.ticker, b.ticker
ORDER BY correlation DESC;
