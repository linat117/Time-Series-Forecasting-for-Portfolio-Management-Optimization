"""
Utility functions for data download, preprocessing, and analysis.

This module provides reusable functions for:
- Downloading financial data from yfinance
- Computing returns
- Detecting outliers
- Creating visualizations
"""

import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple, Optional


def download_data(
    tickers: List[str],
    start: str,
    end: str,
    group_by: str = "ticker",
    auto_adjust: bool = True,
    progress: bool = False,
    threads: bool = False
) -> pd.DataFrame:
    """
    Download historical financial data from yfinance.
    
    Parameters:
    -----------
    tickers : List[str]
        List of ticker symbols to download
    start : str
        Start date in 'YYYY-MM-DD' format
    end : str
        End date in 'YYYY-MM-DD' format
    group_by : str
        How to group the data (default: "ticker")
    auto_adjust : bool
        Whether to auto-adjust prices (default: True)
    progress : bool
        Whether to show progress bar (default: False)
    threads : bool
        Whether to use threads (default: False)
    
    Returns:
    --------
    pd.DataFrame
        Downloaded data with MultiIndex columns
    
    Raises:
    ------
    ValueError
        If download fails or returns empty data
    """
    try:
        data = yf.download(
            tickers,
            start=start,
            end=end,
            group_by=group_by,
            auto_adjust=auto_adjust,
            progress=progress,
            threads=threads
        )
        
        if data.empty:
            raise ValueError(f"Download returned empty data for tickers: {tickers}")
        
        return data
    except Exception as e:
        raise ValueError(f"Failed to download data: {str(e)}")


def extract_prices(data: pd.DataFrame, tickers: List[str]) -> pd.DataFrame:
    """
    Extract closing prices from downloaded yfinance data.
    
    Parameters:
    -----------
    data : pd.DataFrame
        Data downloaded from yfinance
    tickers : List[str]
        List of ticker symbols
    
    Returns:
    --------
    pd.DataFrame
        DataFrame with closing prices for each ticker
    """
    prices = pd.DataFrame({
        ticker: data[ticker]["Close"] for ticker in tickers
    })
    return prices


def compute_returns(prices: pd.DataFrame) -> pd.DataFrame:
    """
    Compute daily returns (percentage change) from prices.
    
    Parameters:
    -----------
    prices : pd.DataFrame
        DataFrame with price data
    
    Returns:
    --------
    pd.DataFrame
        DataFrame with daily returns
    """
    returns = prices.pct_change().dropna()
    return returns


def detect_outliers(
    returns: pd.DataFrame,
    method: str = "iqr",
    threshold: float = 3.0
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Detect outliers in return data using specified method.
    
    Parameters:
    -----------
    returns : pd.DataFrame
        DataFrame with return data
    method : str
        Method to use: 'iqr' (Interquartile Range) or 'zscore' (Z-score)
    threshold : float
        Threshold multiplier for outlier detection (default: 3.0)
    
    Returns:
    --------
    Tuple[pd.DataFrame, pd.DataFrame]
        Tuple of (outlier_flags, outlier_data)
        - outlier_flags: Boolean DataFrame indicating outliers
        - outlier_data: DataFrame with only outlier values
    """
    outlier_flags = pd.DataFrame(index=returns.index, columns=returns.columns, dtype=bool)
    outlier_data = pd.DataFrame()
    
    for col in returns.columns:
        if method == "iqr":
            Q1 = returns[col].quantile(0.25)
            Q3 = returns[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - threshold * IQR
            upper_bound = Q3 + threshold * IQR
            flags = (returns[col] < lower_bound) | (returns[col] > upper_bound)
        elif method == "zscore":
            z_scores = np.abs((returns[col] - returns[col].mean()) / returns[col].std())
            flags = z_scores > threshold
        else:
            raise ValueError(f"Unknown method: {method}. Use 'iqr' or 'zscore'")
        
        outlier_flags[col] = flags
        outlier_values = returns[col][flags]
        if not outlier_values.empty:
            outlier_data[f"{col}_outlier"] = outlier_values
    
    return outlier_flags, outlier_data


def plot_prices(
    prices: pd.DataFrame,
    title: str = "Asset Prices Over Time",
    figsize: Tuple[int, int] = (12, 5)
) -> None:
    """
    Plot asset prices over time.
    
    Parameters:
    -----------
    prices : pd.DataFrame
        DataFrame with price data
    title : str
        Plot title
    figsize : Tuple[int, int]
        Figure size (width, height)
    """
    plt.figure(figsize=figsize)
    for col in prices.columns:
        plt.plot(prices.index, prices[col], label=col, linewidth=1.5)
    plt.title(title, fontsize=14, fontweight='bold')
    plt.xlabel("Date", fontsize=12)
    plt.ylabel("Price (USD)", fontsize=12)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


def plot_returns(
    returns: pd.DataFrame,
    title: str = "Daily Returns",
    figsize: Tuple[int, int] = (12, 5)
) -> None:
    """
    Plot daily returns over time.
    
    Parameters:
    -----------
    returns : pd.DataFrame
        DataFrame with return data
    title : str
        Plot title
    figsize : Tuple[int, int]
        Figure size (width, height)
    """
    plt.figure(figsize=figsize)
    for col in returns.columns:
        plt.plot(returns.index, returns[col], label=col, alpha=0.7, linewidth=1)
    plt.title(title, fontsize=14, fontweight='bold')
    plt.xlabel("Date", fontsize=12)
    plt.ylabel("Daily Return", fontsize=12)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.axhline(y=0, color='black', linestyle='--', linewidth=0.8)
    plt.tight_layout()
    plt.show()


def plot_rolling_statistics(
    returns: pd.DataFrame,
    window: int = 30,
    statistic: str = "std",
    title: str = "Rolling Statistics",
    figsize: Tuple[int, int] = (12, 5)
) -> None:
    """
    Plot rolling statistics (e.g., volatility) over time.
    
    Parameters:
    -----------
    returns : pd.DataFrame
        DataFrame with return data
    window : int
        Rolling window size in days (default: 30)
    statistic : str
        Statistic to compute: 'std' (standard deviation) or 'mean'
    title : str
        Plot title
    figsize : Tuple[int, int]
        Figure size (width, height)
    """
    if statistic == "std":
        rolling_data = returns.rolling(window=window).std()
        ylabel = f"{window}-Day Rolling Volatility (Standard Deviation)"
    elif statistic == "mean":
        rolling_data = returns.rolling(window=window).mean()
        ylabel = f"{window}-Day Rolling Mean Return"
    else:
        raise ValueError(f"Unknown statistic: {statistic}. Use 'std' or 'mean'")
    
    plt.figure(figsize=figsize)
    for col in rolling_data.columns:
        plt.plot(rolling_data.index, rolling_data[col], label=col, linewidth=1.5)
    plt.title(title, fontsize=14, fontweight='bold')
    plt.xlabel("Date", fontsize=12)
    plt.ylabel(ylabel, fontsize=12)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()
