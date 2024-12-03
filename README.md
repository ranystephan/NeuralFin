# NeuralFin-Backend

NeuralFin-Backend is the server-side component of the NeuralFin project, designed to process and analyze financial data from companies in the Middle East and North Africa (MENA) region. It provides APIs and services that support the NeuralFin-Frontend, delivering data and insights to users.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [API Endpoints](#api-endpoints)
- [Data Processing](#data-processing)
- [Metrics Calculation](#metrics-calculation)
- [Contributing](#contributing)
- [License](#license)

## Introduction

NeuralFin-Backend serves as the core engine for the NeuralFin platform, handling data ingestion, processing, and analysis. It integrates with various data sources to collect financial information, processes this data to extract meaningful insights, and exposes APIs consumed by the front-end application.

## Features

- **Data Ingestion**: Collects financial data from multiple sources, including stock prices, financial statements, and economic indicators.
- **Data Processing**: Cleanses and transforms raw data into structured formats suitable for analysis.
- **Financial Metrics Calculation**: Computes key financial ratios and metrics to assess company performance.
- **API Services**: Provides RESTful APIs for the front-end to retrieve processed data and analytics.
- **Authentication and Authorization**: Manages user authentication and access control for secure data access.

## Installation

To set up the NeuralFin-Backend locally, follow these steps:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/ranystephan/NeuralFin-Backend.git
   ```
2. **Navigate to the Project Directory**:
   ```bash
   cd NeuralFin-Backend
   ```
3. **Install Dependencies**:
   ```bash
   npm install
   ```
4. **Set Up Environment Variables**:
   Create a `.env` file in the root directory and define the necessary environment variables, such as database connection strings and API keys.
5. **Run Database Migrations**:
   ```bash
   npm run migrate
   ```
6. **Start the Server**:
   ```bash
   npm start
   ```

## Usage

Once the server is running, it will listen for incoming HTTP requests on the configured port (default is 3000). You can interact with the API endpoints using tools like Postman or through the NeuralFin-Frontend application.

## Project Structure

The project's directory structure is organized as follows:

```
NeuralFin-Backend/
├── src/
│   ├── controllers/
│   ├── models/
│   ├── routes/
│   ├── services/
│   ├── utils/
│   └── index.js
├── tests/
├── migrations/
├── .env
├── package.json
└── README.md
```

- **`src/controllers/`**: Contains controllers that handle incoming requests and orchestrate responses.
- **`src/models/`**: Defines data models and schemas for interacting with the database.
- **`src/routes/`**: Sets up API routes and associates them with corresponding controllers.
- **`src/services/`**: Implements business logic and data processing functionalities.
- **`src/utils/`**: Includes utility functions and helpers used across the application.
- **`src/index.js`**: Entry point of the application, initializing the server and connecting to the database.
- **`tests/`**: Contains test cases to ensure the reliability of the application.
- **`migrations/`**: Holds database migration scripts for schema changes.
- **`.env`**: Environment configuration file (not included in version control).

## API Endpoints

The backend exposes several RESTful API endpoints for data retrieval and manipulation. Below is an overview of the primary endpoints:

- **User Authentication**:
  - **POST `/api/auth/register`**: Registers a new user.
  - **POST `/api/auth/login`**: Authenticates a user and returns a JWT token.
- **Financial Data**:
  - **GET `/api/companies`**: Retrieves a list of companies in the MENA region.
  - **GET `/api/companies/:id`**: Fetches detailed information for a specific company.
  - **GET `/api/companies/:id/metrics`**: Obtains calculated financial metrics for a company.
- **Market Data**:
  - **GET `/api/markets`**: Provides data on various financial markets.
  - **GET `/api/markets/:id`**: Retrieves information about a specific market.

For a comprehensive list of endpoints and their functionalities, refer to the API documentation.

## Data Processing

Data processing is a critical component of NeuralFin-Backend, involving several steps:

1. **Data Ingestion**: Collects raw financial data from external APIs, databases, and other sources.
2. **Data Cleaning**: Removes inconsistencies, handles missing values, and standardizes data formats.
3. **Data Transformation**: Converts raw data into structured formats, creating necessary fields and relationships.
4. **Data Storage**: Saves processed data into the database for efficient retrieval and analysis.

These processes ensure that the data served to the front-end is accurate, up-to-date, and relevant.

## Metrics Calculation

The backend calculates various financial metrics to assess company performance. Below are examples of such metrics along with their calculation formulas:

1. **Price-to-Earnings (P/E) Ratio**:
   
   $$\text{P/E Ratio} = \frac{\text{Market Price per Share}}{\text{Earnings per Share (EPS)}}$$


The backend of NeuralFin supports the computation of both fundamental financial metrics and advanced quantitative finance metrics. These include measures for portfolio optimization, risk assessment, and performance evaluation.

#### 2. **Portfolio Optimization (Markowitz Model)**:
   The Markowitz model helps in selecting the optimal portfolio by maximizing returns for a given level of risk or minimizing risk for a given level of returns.

   **Key Formulas**:
   - Portfolio Expected Return:
     $$E(R_p) = \sum_{i=1}^n w_i E(R_i)$$
     Where \(w_i\) is the weight of asset \(i\) in the portfolio and \(E(R_i)\) is its expected return.

   - Portfolio Variance:
     $$\sigma_p^2 = \sum_{i=1}^n \sum_{j=1}^n w_i w_j \sigma_{ij}$$
     Where \(\sigma_{ij}\) is the covariance between assets \(i\) and \(j\).

   **Implementation** (Pseudocode):
   ```python
   import numpy as np

   # Covariance matrix and expected returns
   cov_matrix = np.array([[0.04, 0.02], [0.02, 0.03]])
   expected_returns = np.array([0.10, 0.12])

   # Portfolio weights
   weights = np.array([0.6, 0.4])

   # Expected return
   portfolio_return = np.dot(weights, expected_returns)

   # Portfolio variance
   portfolio_variance = np.dot(weights.T, np.dot(cov_matrix, weights))
   ```

#### 3. **Alpha and Beta**:
   - **Beta**: Measures the sensitivity of a stock’s returns to market returns.
     
     $$\beta = \frac{\text{Cov}(R_i, R_m)}{\text{Var}(R_m)}$$
   - **Alpha**: Represents the excess return of an asset or portfolio above its expected return based on beta.
     
     $$\alpha = R_i - \left(\beta \cdot R_m + \text{Risk-Free Rate}\right)$$

   **Implementation**:
   ```python
   def calculate_beta(stock_returns, market_returns):
       covariance = np.cov(stock_returns, market_returns)[0, 1]
       variance_market = np.var(market_returns)
       return covariance / variance_market

   def calculate_alpha(actual_return, beta, market_return, risk_free_rate):
       expected_return = beta * market_return + risk_free_rate
       return actual_return - expected_return
   ```

#### 4. **Value at Risk (VaR)**:
   VaR estimates the maximum potential loss of a portfolio over a specified time period with a given confidence level.

   **Formula**:
   $$\text{VaR} = - \left( \mu + z \cdot \sigma \right)$$
   Where \(z\) is the critical value corresponding to the confidence level.

   **Implementation**:
   ```python
   from scipy.stats import norm

   def calculate_var(portfolio_mean, portfolio_std, confidence_level):
       z = norm.ppf(confidence_level)
       return -(portfolio_mean + z * portfolio_std)
   ```

#### 5. **Conditional Value at Risk (CVaR)** or **Expected Shortfall**:
   CVaR calculates the average loss beyond the VaR threshold.

   **Formula**:
   $$\text{CVaR} = \frac{1}{1-\alpha} \int_{\alpha}^{1} \text{VaR}(p) dp$$

   **Implementation**:
   ```python
   def calculate_cvar(losses, var):
       return np.mean([loss for loss in losses if loss > var])
   ```

#### 6. **Sharpe Ratio**:
   Measures the risk-adjusted return of a portfolio.
   $$\text{Sharpe Ratio} = \frac{R_p - R_f}{\sigma_p}$$

   **Implementation**:
   ```python
   def calculate_sharpe_ratio(portfolio_return, risk_free_rate, portfolio_std):
       return (portfolio_return - risk_free_rate) / portfolio_std
   ```

#### 7. **Sortino Ratio**:
   A variation of the Sharpe Ratio that considers only downside risk.
   $$\text{Sortino Ratio} = \frac{R_p - R_f}{\sigma_{\text{downside}}}$$

#### 8. **Expected Shortfall (ES)**:
   Expected Shortfall provides a more comprehensive risk measure by capturing the average loss in the tail distribution of losses.

   **Implementation**:
   ```python
   def calculate_expected_shortfall(losses, alpha):
       sorted_losses = sorted(losses)
       threshold_index = int(len(losses) * alpha)
       return np.mean(sorted_losses[:threshold_index])
   ```

---

## **Backend Workflow**

1. **Data Ingestion**:
   - Financial data (price history, volume, fundamentals) is collected from external APIs (e.g., Refinitiv, Bloomberg).
   - Data is ingested into a PostgreSQL database.

2. **Data Processing**:
   - Data is cleaned, normalized, and aggregated.
   - Financial metrics and risk measures are computed.

3. **API Exposure**:
   - Results are served through RESTful endpoints for use by the NeuralFin-Frontend.

---

## **Contributing**

1. Fork the repository.
2. Create a branch for your feature or fix.
3. Submit a pull request.

---

## **License**

This project is licensed under the MIT License.

---

NeuralFin-Backend serves as the analytical powerhouse for NeuralFin, enabling robust and scalable analysis of financial data. Its comprehensive metric calculations and RESTful APIs facilitate the integration of advanced financial analytics with user-friendly front-end interfaces.
