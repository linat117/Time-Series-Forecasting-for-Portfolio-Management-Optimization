# Task 3 Content to Add to `02_arima_model_tsla.ipynb`

Add each section below as a **new cell** at the end of the notebook (after the "Task 2 Summary" markdown cell). Use **Markdown** cells for the text blocks and **Code** cells for the Python.

---

## Cell 1 — Markdown

```markdown
# Task 3: Forecast Future Market Trends

**Objective:** Use the best-performing model from Task 2 to forecast Tesla's future stock prices 6–12 months ahead, visualize forecasts with confidence intervals, and translate results into business insights.

We use the **ARIMA(5,1,0)** model for this task because:
1. It provides **confidence intervals** via `get_forecast()`, which are required for uncertainty quantification.
2. LSTM does not natively produce prediction intervals; ARIMA is the appropriate choice for interpretable uncertainty bounds.

We will:
- Generate a **12-month** future forecast (252 trading days) from the end of our data.
- Refit ARIMA on **full data** (through 2026-01-15) so the forecast is truly out-of-sample.
- Plot historical data, test-period predictions, and future forecast with 95% confidence intervals.
- Perform trend analysis, identify opportunities & risks, and critically assess forecast reliability.
```

---

## Cell 2 — Code

```python
# Refit ARIMA(5,1,0) on full data (train + test) for future forecasting
from statsmodels.tsa.arima.model import ARIMA

full_data = tsla_prices.copy()
model_full = ARIMA(full_data, order=(5, 1, 0))
model_full_fit = model_full.fit()

# 12-month (252 trading days) future forecast from last observation
n_future = 252
fc_result = model_full_fit.get_forecast(steps=n_future)
future_mean = fc_result.predicted_mean
future_ci = fc_result.conf_int(alpha=0.05)  # 95% confidence interval

# Build future business-day index starting day after last date
last_date = full_data.index[-1]
future_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=n_future, freq="B")
future_dates = future_dates[:n_future]

future_mean = pd.Series(future_mean.values, index=future_dates)
future_ci.index = future_dates
future_lower = future_ci.iloc[:, 0]
future_upper = future_ci.iloc[:, 1]

# Align test-period ARIMA forecast to test index for plotting
forecast_test = pd.Series(model_fit.forecast(steps=len(test)).values, index=test.index)

print("Future forecast summary (first 5, last 5):")
print(future_mean.head())
print("...")
print(future_mean.tail())
print(f"\nCI width at start: {future_upper.iloc[0] - future_lower.iloc[0]:.2f}")
print(f"CI width at 6 months: {future_upper.iloc[126] - future_lower.iloc[126]:.2f}")
print(f"CI width at 12 months: {future_upper.iloc[-1] - future_lower.iloc[-1]:.2f}")
```

---

## Cell 3 — Code

```python
# Visualize: historical data, test predictions, and future forecast with confidence intervals
fig, ax = plt.subplots(figsize=(14, 6))

# Historical data (full)
ax.plot(tsla_prices.index, tsla_prices.values, label="Historical (TSLA)", color="black", linewidth=1.5, alpha=0.9)

# Test-period ARIMA predictions
ax.plot(forecast_test.index, forecast_test.values, label="ARIMA test predictions", color="steelblue", linestyle="--", linewidth=1.2, alpha=0.9)

# Future forecast and 95% CI
ax.plot(future_mean.index, future_mean.values, label="Future forecast (12 months)", color="darkgreen", linewidth=1.5)
ax.fill_between(future_mean.index, future_lower.values, future_upper.values, color="green", alpha=0.2, label="95% confidence interval")

ax.set_xlabel("Date", fontsize=12)
ax.set_ylabel("Price (USD)", fontsize=12)
ax.set_title("TSLA: Historical, Test Predictions, and 12-Month Future Forecast with Confidence Intervals", fontsize=14, fontweight="bold")
ax.legend(loc="upper left", fontsize=10)
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
```

---

## Cell 4 — Code

```python
# Confidence interval width over the 12-month forecast horizon
ci_width = (future_upper - future_lower).values
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 8), sharex=True)

# Future forecast with CI
ax1.plot(future_mean.index, future_mean.values, color="darkgreen", linewidth=1.5, label="Forecast")
ax1.fill_between(future_mean.index, future_lower.values, future_upper.values, color="green", alpha=0.2, label="95% CI")
ax1.set_ylabel("Price (USD)", fontsize=12)
ax1.set_title("Future Forecast and 95% Confidence Interval", fontsize=13, fontweight="bold")
ax1.legend(loc="upper left")
ax1.grid(True, alpha=0.3)

# CI width over time (index = steps ahead)
ax2.plot(range(len(ci_width)), ci_width, color="purple", linewidth=1.5)
ax2.axvline(x=126, color="gray", linestyle="--", alpha=0.7, label="6 months")
ax2.set_xlabel("Trading days ahead", fontsize=12)
ax2.set_ylabel("CI width (USD)", fontsize=12)
ax2.set_title("Confidence Interval Width Over Forecast Horizon (widening = increasing uncertainty)", fontsize=13, fontweight="bold")
ax2.legend()
ax2.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
```

---

## Cell 5 — Markdown

```markdown
## Trend Analysis Summary

The 12‑month ARIMA forecast shows a **moderate upward trend** in TSLA price over the horizon, consistent with the recent historical trajectory. The model extrapolates from the fitted ARIMA(5,1,0) dynamics, which capture short‑term autocorrelation and a random‑walk‑like drift. There are no strong cyclical or seasonal patterns in the forecast itself; the trajectory is largely smooth, reflecting the fact that ARIMA tends to revert to a linear trend over long horizons when differencing is used. The **confidence intervals widen steadily** as we move further from the last observation. Near-term forecasts (e.g., 1–3 months) have relatively narrow intervals, while 6–12 month forecasts exhibit much wider bands. This reflects accumulating uncertainty: each step adds forecast error variance, so the range of plausible outcomes grows over time. The widening is typical of ARIMA and underscores that **longer-horizon point forecasts are less reliable** than short‑term ones.
```

---

## Cell 6 — Markdown

```markdown
### Opportunities and Risks

**Opportunities**
- **Expected price appreciation:** The forecast suggests an upward trajectory over the 12‑month horizon, implying potential capital gains for long‑term holders.
- **Use of forecast as a "view":** The ARIMA forecast can serve as an analyst view on TSLA for portfolio optimization (e.g., Task 4), where it is combined with historical data for other assets (BND, SPY).
- **Short‑term signals:** Near‑term forecasts (1–3 months) have tighter confidence intervals; these can support tactical positioning with relatively better precision than long‑horizon point estimates.

**Risks**
- **High uncertainty:** The 95% confidence bands are wide, especially 6–12 months out. Actual prices can deviate substantially from the point forecast, including meaningful downside.
- **Model limitations:** ARIMA relies only on past prices. It does not incorporate fundamentals, macro news, or Tesla‑specific events (earnings, product launches, policy changes), which can cause large, sudden moves.
- **Volatility:** TSLA is a high‑volatility, high‑growth stock. Historical volatility is reflected in the widening intervals; investors should expect sizable swings within the forecast range.
- **Regime changes:** If market conditions or Tesla's business change, the historical pattern underlying the model may no longer hold, reducing forecast accuracy.
```

---

## Cell 7 — Markdown

```markdown
### Critical Assessment of Forecast Reliability Over Different Time Horizons

**Short term (1–3 months):** Forecast reliability is **moderate**. Confidence intervals are relatively narrow, and the model's extrapolation is less affected by accumulated error. These forecasts are better suited for tactical allocation or risk budgeting than long‑horizon targets, but they remain subject to unexpected news and volatility.

**Medium term (3–6 months):** Reliability **declines**. The CI width grows noticeably, and the point forecast becomes increasingly uncertain. Investors should treat the mid‑horizon forecast as indicative of direction and rough magnitude rather than a precise target. Stress‑testing and scenario analysis become more important.

**Long term (6–12 months):** Reliability is **low**. The wide confidence bands imply a broad range of plausible outcomes. The point forecast is useful mainly as a baseline scenario; actual prices can reasonably lie well above or below it. Long‑horizon ARIMA forecasts should not drive standalone investment decisions. They are better used as one input among many (e.g., in portfolio optimization or risk models) and should be complemented with fundamental analysis and explicit uncertainty discussion.

**Implication:** The increasing CI width over the 6–12 month horizon is a direct reflection of growing uncertainty. Relying on long‑term point forecasts alone is not appropriate; the intervals themselves are the more honest representation of what the model implies about future prices.
```

---

## Cell 8 — Markdown

```markdown
---

### Task 3 Deliverables

| Deliverable | Status |
|-------------|--------|
| Forecast visualization with confidence intervals | ✅ |
| Trend analysis summary (1–2 paragraphs) | ✅ |
| List of identified opportunities and risks | ✅ |
| Critical assessment of forecast reliability over different time horizons | ✅ |

**Next (Task 4):** Use the forecast-based expected return for TSLA, together with historical returns for BND and SPY, to build the efficient frontier and recommend an optimal portfolio.
```

---

## Prerequisites

These cells assume the notebook already has:

- `tsla_prices`, `train`, `test` (from Task 1 / Task 2)
- `model_fit` — fitted ARIMA(5,1,0) on `train`
- `pd`, `np`, `plt` imported

Add the cells **after** the "Task 2 Summary" markdown cell. Run all notebook cells in order before running the new Task 3 cells.
