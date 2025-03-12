# data_utils.py
import pandas as pd
import numpy as np

def load_data(filepath):
    """
    Load and preprocess data with Sharpe ratios from the specified file path.
    """
    df = pd.read_csv(filepath)
    df['date'] = pd.to_datetime(df['date'])
    
    # Calculate 30-day rolling volatility scaled to annualized volatility
    df['30d_volatility'] = df.groupby('ticker')['close'].transform(
        lambda x: x.pct_change().rolling(30).std() * np.sqrt(252)
    )
    
    # Calculate Sharpe ratios per ticker
    def calculate_sharpe(group):
        returns = group['close'].pct_change().dropna()
        if len(returns) > 0:
            return returns.mean() / returns.std() * np.sqrt(252)
        return np.nan

    sharpe_ratios = df.groupby('ticker').apply(calculate_sharpe, include_groups=False).to_dict()
    df['sharpe_ratio'] = df['ticker'].map(sharpe_ratios)
    
    return df

def calculate_mutual_dates(df):
    """
    Calculate the earliest and latest mutual dates for all tickers.
    """
    min_dates = df.groupby('ticker')['date'].min()
    max_dates = df.groupby('ticker')['date'].max()
    
    earliest_mutual_date = max(min_dates)
    latest_mutual_date = min(max_dates)
    
    return earliest_mutual_date, latest_mutual_date

def calculate_correlation_matrix(df, start_date, end_date):
    """
    Calculate the correlation matrix of daily returns for the given date range.
    """
    filtered_data = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
    returns = filtered_data.pivot(index='date', columns='ticker', values='close').pct_change().dropna()
    return returns.corr()


def calculate_52_week_high_low(df, ticker):
    """
    Calculate the 52-week high and low for a given ticker.
    """
    last_year = df[df['ticker'] == ticker].sort_values('date').tail(252)  # 252 trading days ≈ 1 year
    high_52w = last_year['high'].max()
    low_52w = last_year['low'].min()
    return high_52w, low_52w

def calculate_moving_averages(df, ticker, windows=[50, 100, 200]):
    """
    Calculate multiple moving averages (50-day, 100-day, 200-day) for a given ticker.
    """
    ticker_data = df[df['ticker'] == ticker].sort_values('date').copy()
    
    for window in windows:
        ticker_data[f'{window}d_MA'] = ticker_data['close'].rolling(window=window).mean()
    
    return {window: ticker_data[f'{window}d_MA'].iloc[-1] for window in windows if len(ticker_data) >= window}


def calculate_relative_strength(df, ticker, benchmark_ticker="SOCL"):
    """
    Calculate relative strength (RS) as the ratio of the stock's price performance to the benchmark.
    RS = (Stock Price Performance) / (Benchmark Performance)
    """
    stock_returns = df[df['ticker'] == ticker].sort_values('date').set_index('date')['close'].pct_change().dropna()
    benchmark_returns = df[df['ticker'] == benchmark_ticker].sort_values('date').set_index('date')['close'].pct_change().dropna()

    if len(stock_returns) > 0 and len(benchmark_returns) > 0:
        relative_strength = (1 + stock_returns).cumprod().iloc[-1] / (1 + benchmark_returns).cumprod().iloc[-1]
        return relative_strength
    return None