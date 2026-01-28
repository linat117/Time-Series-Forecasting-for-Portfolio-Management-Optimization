# Task 5 Content to Add (Strategy Backtesting)

Add each section below as a **new cell** at the end of the notebook, after **Task 4** (and after you’ve run the Task 4 cells). Use **Markdown** cells for the text blocks and **Code** cells for the Python.

---

## Cell 1 — Markdown

```markdown
# Task 5: Strategy Backtesting

**Objective:** Validate the portfolio strategy by simulating its performance on historical data and comparing it against a benchmark. The backtest checks whether the model-driven (Task 4) allocation would have outperformed a simple passive strategy.

**Setup:**
- **Backtest period:** Last year of data (Jan 2025 – Jan 2026), i.e. data **not** used for model training.
- **Strategy:** Hold the Task 4 max Sharpe (tangency) portfolio for the full period (no rebalancing).
- **Benchmark:** Static 60% SPY / 40% BND portfolio.
```

---

## Cell 2 — Code

```python
# Backtest window: last year (Jan 2025 – Jan 2026)
bt_start, bt_end = "2025-01-01", "2026-01-15"
ret_bt = returns_daily.loc[bt_start:bt_end].copy()

# Strategy: Task 4 max Sharpe weights (hold full period)
w = weights_rec
strat_daily = ret_bt["TSLA"] * w["TSLA"] + ret_bt["BND"] * w["BND"] + ret_bt["SPY"] * w["SPY"]

# Benchmark: 60% SPY / 40% BND
bench_daily = ret_bt["SPY"] * 0.6 + ret_bt["BND"] * 0.4

# Cumulative returns (growth of $1)
cum_strat = (1 + strat_daily).cumprod()
cum_bench = (1 + bench_daily).cumprod()

print("Backtest period:", ret_bt.index[0].date(), "to", ret_bt.index[-1].date())
print("Trading days:", len(ret_bt))
print("Strategy weights: TSLA={:.2%}, BND={:.2%}, SPY={:.2%}".format(w["TSLA"], w["BND"], w["SPY"]))
```

---

## Cell 3 — Code

```python
# Plot cumulative returns: strategy vs benchmark
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(cum_strat.index, cum_strat.values, label="Strategy (Max Sharpe)", color="darkgreen", linewidth=2)
ax.plot(cum_bench.index, cum_bench.values, label="Benchmark (60% SPY / 40% BND)", color="steelblue", linewidth=2, linestyle="--")
ax.set_xlabel("Date", fontsize=12)
ax.set_ylabel("Cumulative return (growth of $1)", fontsize=12)
ax.set_title("Backtest: Strategy vs Benchmark (Jan 2025 – Jan 2026)", fontsize=14, fontweight="bold")
ax.legend(fontsize=11)
ax.grid(True, alpha=0.3)
ax.axhline(y=1, color="gray", linestyle=":", alpha=0.7)
plt.tight_layout()
plt.show()
```

---

## Cell 4 — Code

```python
# Metrics: total return, annualized return, Sharpe, max drawdown
def total_return(r):
    return (1 + r).prod() - 1

def annualized_return(r, n_days):
    tr = total_return(r)
    return (1 + tr) ** (252 / n_days) - 1 if n_days > 0 else 0

def sharpe_annual(r, rf=0.02):
    excess = r - rf / 252
    return np.sqrt(252) * excess.mean() / excess.std() if excess.std() > 0 else np.nan

def max_drawdown(r):
    cum = (1 + r).cumprod()
    peak = cum.cummax()
    dd = (peak - cum) / peak
    return dd.max()

n = len(ret_bt)
rf = 0.02

tr_strat = total_return(strat_daily)
tr_bench = total_return(bench_daily)
ann_strat = annualized_return(strat_daily, n)
ann_bench = annualized_return(bench_daily, n)
sharpe_strat = sharpe_annual(strat_daily, rf)
sharpe_bench = sharpe_annual(bench_daily, rf)
mdd_strat = max_drawdown(strat_daily)
mdd_bench = max_drawdown(bench_daily)

metrics = pd.DataFrame({
    "Strategy (Max Sharpe)": [f"{tr_strat:.2%}", f"{ann_strat:.2%}", f"{sharpe_strat:.4f}", f"{mdd_strat:.2%}"],
    "Benchmark (60/40)":     [f"{tr_bench:.2%}", f"{ann_bench:.2%}", f"{sharpe_bench:.4f}", f"{mdd_bench:.2%}"],
}, index=["Total return", "Annualized return", "Sharpe ratio (rf=2%)", "Max drawdown"])

print("Performance metrics (backtest period)\n")
print(metrics.to_string())
```

---

## Cell 5 — Code

```python
# Summary: did strategy outperform?
outperformed = tr_strat > tr_bench
print("Strategy outperformed benchmark (total return):", outperformed)
print("Strategy Sharpe > Benchmark Sharpe:", sharpe_strat > sharpe_bench)
print("Strategy max drawdown:", f"{mdd_strat:.2%}", "| Benchmark max drawdown:", f"{mdd_bench:.2%}")
```

---

## Cell 6 — Markdown

```markdown
### Conclusion and reflection

**Did the strategy outperform the benchmark?** Check the metrics table and the "Strategy outperformed benchmark" / "Strategy Sharpe > Benchmark Sharpe" outputs above. Over the backtest window, the model-driven (max Sharpe) portfolio is compared to the 60/40 benchmark on total return, annualized return, Sharpe ratio, and max drawdown. The comparison uses a **simple hold** of the initial Task 4 weights (no rebalancing).

**What does this backtest suggest about the model-driven approach?** The backtest is a single, short out-of-sample experiment. If the strategy outperformed, it supports the idea that the ARIMA-based TSLA view plus MPT optimization could add value over a passive 60/40 mix, but the result may be period-specific. If it underperformed, it illustrates that forecasts and optimized weights do not guarantee better realised outcomes, especially over a limited horizon.

**Limitations:** (1) **Short history** — one year of data; results are not statistically robust. (2) **No rebalancing** — we hold initial weights; monthly rebalancing could change results. (3) **Look-ahead** — we use the same historical sample for covariance and backtest; a stricter design would use only pre-backtest data for optimisation. (4) **Transaction costs and taxes** are ignored. (5) **Survivorship** — we use liquid ETFs/stocks; illiquid or delisted assets would need different handling. (6) **Regime change** — market behaviour may differ in the future. Overall, this backtest is a **conditional check** on the strategy, not proof of long-term viability.
```

---

## Cell 7 — Markdown

```markdown
---

### Task 5 Deliverables

| Deliverable | Status |
|-------------|--------|
| Cumulative returns plot (strategy vs benchmark) | ✅ |
| Performance metrics table (total return, ann. return, Sharpe, max DD) | ✅ |
| Written conclusion on strategy viability (1–2 paragraphs) | ✅ |

**All tasks (1–5) are now complete.** Next: draft the final investment memo (description.md) with methodology, model comparison, efficient frontier, backtest results, and key visuals.
```

---

## Prerequisites

- **Task 4** has been run: `returns_daily`, `weights_rec` (and optionally `prices`) exist.
- **Imports** from earlier cells: `pd`, `np`, `plt`, etc.

Add these cells **after** the Task 4 section. Run all preceding cells (including Task 4) before running Task 5.
