

10 Academy: Artificial Intelligence Mastery

Week 9 Challenge Document
Time Series Forecasting for Portfolio Management Optimization

Date: 21 Jan 2026 - 27 Jan 2026 



















Business objective
Guide Me in Finance (GMF) Investments is a forward-thinking financial advisory firm that specializes in personalized portfolio management. GMF leverages cutting-edge technology and data-driven insights to provide clients with tailored investment strategies. By integrating advanced time series forecasting models, GMF aims to predict market trends, optimize asset allocation, and enhance portfolio performance. The company’s goal is to help clients achieve their financial objectives by minimizing risks and capitalizing on market opportunities.
The Efficient Market Hypothesis suggests that predicting exact stock prices using only historical price data is exceptionally difficult. Therefore, in an industry setting, these models are more often used to forecast volatility, identify momentum factors, or serve as one of many inputs into a larger decision-making framework, rather than for direct, standalone price prediction.
At GMF Investments, financial analysts play a crucial role in interpreting complex financial data and providing actionable insights. By utilizing real-time financial data from sources like YFinance, GMF ensures its strategies are based on the latest market conditions, thereby maintaining a competitive edge.
Situational Overview (Business Need)
As a Financial Analyst at GMF Investments, your objective is to apply time series forecasting to historical financial data to enhance portfolio management strategies. Your role involves analyzing data, building predictive models, and recommending portfolio adjustments based on forecasted trends.
You will:
Utilize YFinance data to extract historical financial information such as stock prices, market indices, and other relevant financial metrics.
Preprocess and analyze this data to identify trends and patterns.
Develop and evaluate forecasting models to predict future market movements.
Use the insights gained to recommend changes to client portfolios that aim to optimize returns while managing risks.





Data
Use historical financial data for three key assets sourced from the YFinance Python library covering the period from January 1, 2015 to January 15, 2026.
Assets
Asset
Ticker
Description
Risk Profile
Tesla
TSLA
High-growth stock in the consumer discretionary sector (Automobile Manufacturing)
High risk, high potential return
Vanguard Total Bond Market ETF
BND
Tracks U.S. investment-grade bonds
Low risk, stability and income
S&P 500 ETF
SPY
Tracks the S&P 500 Index
Moderate risk, broad market exposure

Data Fields
Each dataset includes:
Date: Trading day timestamp
Open, High, Low, Close: Daily price metrics
Adj Close: Adjusted close price accounting for dividends and splits
Volume: Total number of shares/units traded each day
Usage in Portfolio Analysis
TSLA provides potential high returns with high volatility
BND contributes stability and low risk
SPY offers diversified, moderate-risk market exposure
Learning Outcomes
Skills:
API Usage: Skillfully fetching financial data from an API (yfinance)
Data Wrangling: Using pandas for cleaning, handling missing dates/values, time-based indexing, and merging datasets
Feature Engineering: Calculating daily returns, rolling volatility, and other relevant metrics
Data Scaling: Applying normalization or standardization as preprocessing
Statistical Modeling: Building, training, and optimizing ARIMA/SARIMA models using statsmodels and pmdarima
Deep Learning Modeling: Constructing, training, and evaluating an LSTM model for time series forecasting
Model Evaluation: Calculating and comparing performance metrics (MAE, RMSE, MAPE)
Optimization & Visualization: Running simulations to generate and plot the Efficient Frontier
MPT Implementation: Using libraries like PyPortfolioOpt
Simulation: Implementing a simple backtesting loop to simulate portfolio performance
Knowledge:
Understanding the characteristics of different asset classes: high-growth stocks (TSLA), bonds for stability (BND), and market indices for diversification (SPY)
Familiarity with the Efficient Market Hypothesis (EMH) and its practical implication that pure price prediction is difficult
Deeply understanding what stationarity is, why it's crucial for models like ARIMA, and how to test for it
Knowing what the Efficient Frontier represents and the significance of portfolios that lie on it
Understanding the purpose and methodology of backtesting a financial strategy
Knowing the importance of using a benchmark for objective performance evaluation
Behaviors:
Critical Evaluation: The ability to compare and contrast different modeling approaches
Problem Framing & Synthesis: The ability to translate a high-level business objective into technical requirements
Data-Driven Decision Making: Making recommendations grounded in evidence

Communication:
Writing professional investment memos for non-technical stakeholders
Presenting model comparisons with clear justifications
Team
Tutors:
Kerod
Mahbubah
Filimon  
Smegnsh
Key Dates
Challenge Introduction – 10:30 AM UTC on Wednesday, 21 Jan 2026
Interim Submission – 8:00 PM UTC on Sunday, 25 Jan 2026
Final Submission – 8:00 PM UTC on Tuesday, 27 Jan 2026
Communication & Support
Slack channel: #all-week9
Office hours: Mon–Fri, 08:00–15:00 UTC















Deliverables
Project Structure

portfolio-optimization/
├── .vscode/
│   └── settings.json
├── .github/
│   └── workflows/
│       └── unittests.yml
├── .gitignore
├── requirements.txt
├── README.md
├── data/
│   └── processed/
├── notebooks/
│   ├── __init__.py
│   └── README.md
├── src/
│   └── __init__.py
├── tests/
│   └── __init__.py
└── scripts/
       └── __init__.py
Task 1 - Preprocess and Explore the Data
Objective: Load, clean, and understand the data to prepare it for modeling.
Before building any forecasting model, you must understand your data. This task focuses on extracting financial data, cleaning it, and performing exploratory analysis to identify trends, patterns, and statistical properties that will inform your modeling choices.
Instructions:
Extract Historical Financial Data
Use the YFinance Python library to fetch data for TSLA, BND, and SPY
Cover the period from January 1, 2015 to January 15, 2026
Store the data in an organized format (e.g., separate DataFrames or a combined DataFrame with asset identifiers)
Data Cleaning and Understanding
Check basic statistics to understand the distribution of the data
Ensure all columns have appropriate data types
Check for missing values and handle them by either filling, interpolating, or removing them
Normalize or scale the data if required, especially for machine learning models
Conduct Exploratory Data Analysis (EDA)
Visualize the closing price over time to identify trends and patterns
Calculate and plot the daily percentage change to observe volatility
Analyze volatility by calculating rolling means and standard deviations to understand short-term trends and fluctuations
Perform outlier detection to identify significant anomalies
Analyze days with unusually high or low returns
Seasonality and Trend Analysis
Perform a statistical test (e.g., Augmented Dickey-Fuller test) on the closing prices and daily returns
Discuss the results and their implications
A non-stationary series requires differencing (the 'd' in ARIMA) to become stationary, which is a prerequisite for the model
Calculate Risk Metrics
Calculate foundational risk metrics, including:
Value at Risk (VaR)
Sharpe Ratio (historical risk-adjusted returns)
Document key insights like the overall direction of Tesla's stock price and fluctuations in daily returns
Deliverables:
Jupyter notebook with all EDA code and visualizations
Summary of data quality issues and how they were addressed
Stationarity test results with interpretation
At least 3 insightful visualizations capturing key patterns
Task 2 - Build Time Series Forecasting Models
Objective: Develop, train, and evaluate time series forecasting models to predict Tesla's future stock prices.
This task involves building multiple forecasting models to compare their performance. You will implement both classical statistical models and deep learning approaches to understand the trade-offs between model complexity, performance, and interpretability.
Instructions:
Prepare Data for Modeling
Divide the dataset into training and testing sets
Critical: Split chronologically to preserve temporal order (e.g., train on 2015-2024, test on 2025-2026)
Random shuffling is inappropriate for time series data
Implement ARIMA/SARIMA Model
Use ACF/PACF plots or auto_arima from pmdarima to find the best (p, d, q) parameters
For seasonal data, determine (P, D, Q, m) parameters for SARIMA
Fit the model on training data
Generate forecasts for the test period
Implement LSTM Model
Prepare sequence data with appropriate window sizes (e.g., use last 60 days to predict next day)
Build the LSTM architecture:
Input layer matching sequence length
One or more LSTM layers
Dense output layer
Train with appropriate hyperparameters (epochs, batch size)
Generate forecasts for the test period
Optimize Model Parameters
For ARIMA: Use grid search or auto_arima to find optimal parameters
For LSTM: Experiment with architecture (layers, neurons) and hyperparameters (epochs, batch size, learning rate)
Evaluate and Compare Models
Calculate performance metrics for all models:
MAE (Mean Absolute Error)
RMSE (Root Mean Squared Error)
MAPE (Mean Absolute Percentage Error)
Provide a brief discussion on which model performed better and why that might be the case
Deliverables:
Trained ARIMA/SARIMA model with documented parameters
Trained LSTM model with documented architecture
Model comparison table with all metrics
Discussion of model selection rationale
Task 3 - Forecast Future Market Trends
Objective: Use your trained models to forecast Tesla's future stock prices and analyze the results for actionable insights.
A forecast is only useful if it can be interpreted and acted upon. In this task, you will generate future predictions, visualize them with uncertainty bounds, and translate the results into business insights about market opportunities and risks.

Instructions:
Generate Future Forecasts
Using your best-performing model from Task 2, generate forecasts for 6-12 months into the future
For ARIMA/SARIMA: Use the forecast() or predict() method
For LSTM: Iteratively predict and feed predictions back for multi-step forecasting
Visualize Forecasts with Confidence Intervals
Plot the forecast alongside historical data
Include confidence intervals to show the range within which future prices are expected to lie
Clearly distinguish between historical data, test predictions, and future forecasts
Perform Trend Analysis
Look for long-term trends (upward, downward, or stable)
Identify any patterns or anomalies in the forecast
Critically analyze the confidence intervals:
How does their width change over the 6-12 month forecast horizon?
What does this imply about the reliability and certainty of long-term forecasts?
Assess Market Opportunities and Risks
Based on the forecast, outline potential market opportunities (e.g., expected price increases)
Identify risks (e.g., high volatility or expected declines)
Discuss the level of uncertainty captured by the confidence intervals
Deliverables:
Forecast visualization with confidence intervals
Trend analysis summary (1-2 paragraphs)
List of identified opportunities and risks
Critical assessment of forecast reliability over different time horizons
Task 4 - Optimize Portfolio Based on Forecast
Objective: Use insights from your forecast to construct an optimal portfolio using Modern Portfolio Theory (MPT).
Modern Portfolio Theory provides a mathematical framework for assembling a portfolio of assets that maximizes expected return for a given level of risk. In this task, you will combine your Tesla forecast with historical data for other assets to build an optimized portfolio.
Instructions:
Prepare Expected Returns
TSLA (Forecasted Asset): Use the return forecast generated by your best-performing model from Task 2 as the expected return for Tesla
BND and SPY (Historical Assets): Use their historical average daily returns (annualized) as the proxy for expected returns
This simulates a common approach where an analyst has a specific "view" on one asset while relying on historical data for others
Compute Covariance Matrix
Calculate the covariance matrix based on historical daily returns of all three assets (TSLA, BND, SPY)
This matrix is crucial for understanding how the assets move together and for calculating portfolio risk
Generate the Efficient Frontier
Using the expected returns vector and the covariance matrix, run an optimization simulation
Generate the Efficient Frontier - the set of optimal portfolios that offer the highest expected return for a defined level of risk
Use libraries like PyPortfolioOpt or scipy.optimize
Visualize and Identify Key Portfolios
Plot the Efficient Frontier with:
X-axis: Portfolio volatility (risk/standard deviation)
Y-axis: Portfolio expected return
Identify and mark two key portfolios:
The Maximum Sharpe Ratio Portfolio (Tangency Portfolio)
The Minimum Volatility Portfolio
Recommend Optimal Portfolio
Based on your analysis, select and recommend an optimal portfolio
Justify your choice (e.g., prioritizing maximum risk-adjusted return vs. lower risk)
Summarize your final recommended portfolio including:
Optimal weights for TSLA, BND, and SPY
Expected annual return
Expected volatility
Sharpe Ratio
Deliverables:
Efficient Frontier plot with key portfolios marked
Covariance matrix visualization (heatmap)
Final portfolio recommendation with weights and metrics
Written justification for portfolio selection (1 paragraph)

Task 5 - Strategy Backtesting
Objective: Validate your portfolio strategy by simulating its performance on historical data and comparing it against a benchmark.
A forecast and an optimized portfolio are hypotheses. A backtest is the experiment that validates them. This task will help you understand whether your model-driven approach would have outperformed a simple passive strategy.
Instructions:
Define Backtesting Period
Use the last year of your dataset (e.g., January 2025 - January 2026) as your backtesting window
This should be data that was NOT used for training your models
Define a Benchmark
Create a simple benchmark portfolio to compare against
Suggested benchmark: Static 60% SPY / 40% BND portfolio (a common balanced portfolio)
Simulate Your Strategy
Start with the initial optimal weights you found in Task 4
"Hold" this portfolio for a set period (e.g., one month)
Options for simulation:
Simple: Hold initial weights for the full backtesting period
Advanced: Perform monthly rebalancing back to target weights
Analyze Performance
Plot the cumulative returns of your strategy portfolio against the benchmark portfolio over the backtesting period
Calculate the final metrics for both portfolios:
Total return
Annualized return
Sharpe Ratio
Maximum drawdown
Conclude and Reflect
Did your strategy outperform the benchmark?
What does this initial backtest suggest about the viability of your model-driven approach?
What are the limitations of this backtest?
Deliverables:
Cumulative returns comparison plot (strategy vs. benchmark)
Performance metrics table for both portfolios
Written conclusion on strategy viability (1-2 paragraphs)
Due Date (Submission)
Interim Submission - Sunday (25 Jan 2026): 8:00 PM UTC
GitHub Repository containing: Completed Task 1 (data extraction, EDA, stationarity testing), and Initial progress on Task 2 (at least one model implemented)
Interim Report:
Summary of data extraction and cleaning steps
Key EDA visualizations and insights
Stationarity test results and interpretation
Volatility analysis and risk metrics
Feedback: You may not receive detailed comments on your interim submission but will receive a grade.
Final Submission - Tuesday (27 Jan 2026): 8:00 PM UTC
GitHub Repository containing: All completed tasks with clean, well-documented code
Final Report (Investment Memo format, suitable for GMF's investment committee):
Professional PDF report OR detailed technical blog post (e.g., on Medium)
Methodology description for each task
Model comparison results with justification for selection
Efficient Frontier visualization with portfolio recommendation
Backtest results and conclusions
Screenshots demonstrating key outputs
Feedback: You will receive comments/feedback in addition to a grade for your final submission.
Other Considerations
Documentation: Maintain detailed documentation in code comments and README files
Collaboration: Use GitHub issues and projects for task tracking
Communication: Regular check-ins, Q&A sessions, and a supportive community atmosphere
Flexibility: Acknowledge potential challenges (API rate limits, data gaps) and communicate proactively
Professionalism: Emphasize work ethics and professional behavior
Time Management: Start early, especially for Tasks 1 and 2 which are foundational for later tasks
Tutorials Schedule
In the following, the color purple indicates morning sessions, and blue indicates afternoon sessions.
Wednesday

Introduction to the challenge (Kerod)
Comparing time series modeling (Filimon)
Thursday

Time Series Forecasting and Portfolio Optimization (Mahbubah)
Backtesting and Simulation for Trading Strategies (Smegnsh)
Friday
Integrating robust risk analysis into portfolio management (Mahbubah)
Monday (26 Jan)
Q&A (Filimon)
Tuesday (27 Jan)
Q&A (Mahbubah)










References
Time Series Analysis and Forecasting
DataCamp: ARIMA Tutorial
Machine Learning Mastery: ARIMA for Time Series Forecasting
GeeksforGeeks: Time Series Analysis and Forecasting
Complete Guide to Time Series Forecasting
Time Series Analysis in Python
Time Series Analysis in Python
Portfolio Optimization
Complete Guide to Portfolio Optimization
Portfolio Optimization Python Example
Portfolio Optimization with Python
Portfolio Optimization using MPT in Python
PyPortfolioOpt Documentation
Portfolio Optimization with Datalore
Building an Optimal Portfolio with Python
Efficient Market Hypothesis
Investopedia: Efficient Market Hypothesis
Investopedia: Adaptive Market Hypothesis
Investopedia: Behavioral Finance
Asset Classes Overview
LSTM for Time Series
LSTM Networks for Time Series Forecasting
TensorFlow: Time Series Tutorial
DataCamp: LSTM Python Stock Market
Backtesting
Investopedia: Backtesting
QuantStart: Backtesting Systematic Trading Strategies
