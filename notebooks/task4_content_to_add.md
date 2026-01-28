# Task 4 Content to Add (Portfolio Optimization)

Add each section below as a **new cell** at the end of the notebook, after **Task 3** (and after you’ve run the Task 3 cells). Use **Markdown** cells for the text blocks and **Code** cells for the Python.

---

## Cell 1 — Markdown

```markdown
# Task 4: Optimize Portfolio Based on Forecast

**Objective:** Use the forecast from Task 3 to construct an optimal portfolio with Modern Portfolio Theory (MPT). We combine the ARIMA-based expected return for TSLA with historical returns for BND and SPY, compute the covariance matrix from historical daily returns, and generate the efficient frontier.

**Approach:**
- **TSLA:** Use the 12‑month ARIMA forecast to derive expected annual return (forecast view).
- **BND, SPY:** Use historical average daily returns, annualized.
- **Covariance:** Historical daily returns of TSLA, BND, SPY (annualized).
- **Optimization:** PyPortfolioOpt — efficient frontier, max Sharpe (tangency), min volatility.
```

---

## Cell 2 — Code

```python
# Fetch BND and SPY; use TSLA from notebook. Align dates and compute returns.
import yfinance as yf

start, end = "2015-01-01", "2026-01-15"
tsla_series = tsla_prices.squeeze() if isinstance(tsla_prices, pd.DataFrame) else tsla_prices
tsla_series = tsla_series.dropna()
tsla_series.name = "TSLA"

bnd = yf.download("BND", start=start, end=end, auto_adjust=True, progress=False)["Close"].rename("BND")
spy = yf.download("SPY", start=start, end=end, auto_adjust=True, progress=False)["Close"].rename("SPY")

prices = pd.concat([tsla_series, bnd, spy], axis=1).dropna()
returns_daily = prices.pct_change().dropna()

print("Prices shape:", prices.shape)
print("Daily returns shape:", returns_daily.shape)
print("Sample returns:\n", returns_daily.tail())
```

---

## Cell 3 — Code

```python
# Expected returns: TSLA from forecast, BND/SPY from history (annualized)
# TSLA: implied 1‑year return from ARIMA forecast
tsla_ann_return = (future_mean.iloc[-1] / full_data.iloc[-1]) - 1.0

# BND, SPY: mean daily return * 252
bnd_ann_return = returns_daily["BND"].mean() * 252
spy_ann_return = returns_daily["SPY"].mean() * 252

expected_returns = pd.Series({
    "TSLA": tsla_ann_return,
    "BND": bnd_ann_return,
    "SPY": spy_ann_return,
})

# Covariance matrix (annualized): cov(daily returns) * 252
cov_matrix = returns_daily.cov() * 252

print("Expected annual returns:\n", expected_returns.round(4))
print("\nCovariance matrix (annualized):\n", cov_matrix.round(6))
```

---

## Cell 4 — Code

```python
# Efficient frontier, max Sharpe, min volatility (PyPortfolioOpt)
from pypfopt import EfficientFrontier, plotting

ef = EfficientFrontier(expected_returns, cov_matrix, weight_bounds=(0, 1))
ef_maxsharpe = EfficientFrontier(expected_returns, cov_matrix, weight_bounds=(0, 1))
ef_minvol = EfficientFrontier(expected_returns, cov_matrix, weight_bounds=(0, 1))

# Plot efficient frontier (BEFORE optimizing ef)
fig, ax = plt.subplots(figsize=(10, 6))
plotting.plot_efficient_frontier(ef, ax=ax, show_assets=True, showfig=False)

# Max Sharpe (tangency) and min vol
ef_maxsharpe.max_sharpe(risk_free_rate=0.02)
ret_sharpe, vol_sharpe, sharpe_sharpe = ef_maxsharpe.portfolio_performance(risk_free_rate=0.02)
ef_minvol.min_volatility()
ret_minvol, vol_minvol, sharpe_minvol = ef_minvol.portfolio_performance(risk_free_rate=0.02)

ax.scatter(vol_sharpe, ret_sharpe, marker="*", s=400, c="red", edgecolors="black", label="Max Sharpe (Tangency)", zorder=5)
ax.scatter(vol_minvol, ret_minvol, marker="s", s=200, c="blue", edgecolors="black", label="Min Volatility", zorder=5)
ax.set_xlabel("Volatility (risk)")
ax.set_ylabel("Expected return")
ax.set_title("Efficient Frontier — TSLA, BND, SPY (Max Sharpe & Min Vol marked)")
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
```

---

## Cell 5 — Code

```python
# Covariance matrix heatmap
ax_cov = plotting.plot_covariance(cov_matrix, plot_correlation=False, show_tickers=True, showfig=False)
ax_cov.set_title("Covariance Matrix (Annualized)")
plt.tight_layout()
plt.show()
```

---

## Cell 6 — Code

```python
# Recommended portfolio: Max Sharpe (tangency)
weights_rec = ef_maxsharpe.clean_weights()
ret_rec, vol_rec, sharpe_rec = ef_maxsharpe.portfolio_performance(risk_free_rate=0.02)

print("Recommended portfolio (Max Sharpe / Tangency)")
print("=" * 50)
print("Weights: TSLA = {:.2%}, BND = {:.2%}, SPY = {:.2%}".format(
    weights_rec["TSLA"], weights_rec["BND"], weights_rec["SPY"]))
print("Expected annual return: {:.2%}".format(ret_rec))
print("Expected volatility:    {:.2%}".format(vol_rec))
print("Sharpe ratio (rf=2%):   {:.4f}".format(sharpe_rec))
print("\nMin Volatility portfolio (for comparison)")
print("Weights: TSLA = {:.2%}, BND = {:.2%}, SPY = {:.2%}".format(
    ef_minvol.clean_weights()["TSLA"], ef_minvol.clean_weights()["BND"], ef_minvol.clean_weights()["SPY"]))
print("Expected annual return: {:.2%}, Volatility: {:.2%}, Sharpe: {:.4f}".format(
    ret_minvol, vol_minvol, sharpe_minvol))
```

---

## Cell 7 — Markdown

```markdown
### Portfolio recommendation and justification

We recommend the **maximum Sharpe ratio (tangency) portfolio** as the primary allocation. It offers the highest risk‑adjusted return among long‑only portfolios on the efficient frontier, which is appropriate for investors who can tolerate moderate volatility in exchange for better expected reward per unit of risk. The tangency portfolio tilts toward assets with higher expected returns (here, TSLA, given our ARIMA forecast) while diversification with BND and SPY limits risk. The **minimum volatility portfolio** is available for more risk‑averse investors; it sacrifices some return for lower volatility. In practice, the exact weights depend on the forecast (TSLA) and historical data (BND, SPY) and should be reviewed when the forecast or market regime changes.
```

---

## Cell 8 — Markdown

```markdown
---

### Task 4 Deliverables

| Deliverable | Status |
|-------------|--------|
| Efficient frontier plot with max Sharpe & min vol marked | ✅ |
| Covariance matrix heatmap | ✅ |
| Final portfolio recommendation (weights, return, vol, Sharpe) | ✅ |
| Written justification (1 paragraph) | ✅ |

**Next (Task 5):** Backtest the recommended portfolio vs a 60% SPY / 40% BND benchmark over the last year.
```

---

## Prerequisites

- **Task 3** has been run: `tsla_prices`, `full_data`, `future_mean` exist.
- **Imports** from earlier cells: `pd`, `np`, `plt`, etc.
- **PyPortfolioOpt** installed (`pypfopt`).

Add these cells **after** the Task 3 section. Run all preceding cells (including Task 3) before running Task 4.
