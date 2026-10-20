# TrendLens | Fashion Trend Analytics

**An interactive fashion analytics dashboard for exploring style momentum, product demand, pricing, and color trends.**

[**Live Demo**](https://trendlensgit-c3ehlyxbfcg9mktjxspueu.streamlit.app/) · [GitHub Repository](https://github.com/harini2024S/TrendLens)

TrendLens is a Python-based dashboard built with Streamlit, pandas, and Plotly. It allows users to filter a fashion product catalog, compare product and category metrics, explore visual patterns, and generate a buyer's brief based on selected filters.

> **Data transparency:** The included 500-row dataset contains synthetic demo data. It is not sourced from retailers and does not represent actual consumer behavior or current fashion trends. Dashboard results demonstrate the application's functionality, not validated market research.

## Features

- **Interactive filtering:** Explore products by category, season, price, and minimum demand score.
- **Style momentum ranking:** Compare styles using a transparent, weighted trend score.
- **Search interest vs. demand:** Visualize the relationship between two synthetic metrics.
- **Category analysis:** Compare demand and pricing across product categories.
- **Color mix visualization:** Explore the distribution of product colors in the filtered catalog.
- **Buyer's brief:** Generate a concise summary based on the current selection.
- **Data export:** Download filtered catalog data for further analysis.
- **Shopping-trend references:** Explore separately presented fashion coverage and external sources, where available.

## Tech Stack

- **Language:** Python
- **Data analysis:** pandas
- **Visualization:** Plotly
- **Dashboard:** Streamlit
- **Data format:** CSV

## Run Locally

Python 3.10 or newer is recommended.

### 1. Clone the repository

```powershell
git clone https://github.com/harini2024S/TrendLens.git
cd TrendLens
```

### 2. Create and activate a virtual environment

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks environment activation, use the virtual environment's Python executable directly in the following steps.

### 3. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 4. Start the dashboard

```powershell
python -m streamlit run app.py
```

Open the local URL printed in the terminal. To stop the application, press `Ctrl+C`.

If activation did not work, run these commands instead:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```

## Trend Scoring Method

TrendLens uses a simple weighted score to rank styles in the demo:

```text
Trend Score = (0.55 × Average Search Interest)
            + (0.45 × Average Demand Score)
```

The score gives search interest a 55% weight and demand score a 45% weight. It is a descriptive ranking formula, not a trained forecasting model. Because the underlying data is synthetic, the rankings should not be interpreted as actual market predictions.

## Dataset

The included CSV contains 500 synthetic product records with the following fields:

| Field | Description |
|---|---|
| `product_id` | Demo product identifier |
| `category` | Product category |
| `style` | Style label |
| `color` | Product color |
| `season` | Associated season |
| `month` | Associated month |
| `price_usd` | Illustrative product price in USD |
| `search_interest` | Synthetic attention index from 0–100 |
| `demand_score` | Synthetic demand score from 0–100 |
| `sales_index` | Synthetic relative sales index |
| `sustainability_score` | Synthetic score from 0–100 |

## Limitations and Future Improvements

The current version is designed to demonstrate interactive analytics and dashboard development. Its synthetic dataset cannot establish real-world fashion trends or consumer demand.

Potential extensions include:
- Integrating a responsibly sourced, licensed fashion dataset.
- Comparing trends over time using validated historical data.
- Adding documented data-quality checks and more detailed analytical metrics.
- Evaluating whether alternative scoring weights produce meaningfully different rankings.

## Project Summary

**TrendLens | Fashion Trend Analytics Dashboard**

Built an interactive dashboard using Python, pandas, Plotly, and Streamlit to explore fashion product attributes, compare synthetic demand and search-interest metrics, rank styles with a transparent scoring method, and export filtered data. Designed the project to run locally or through Streamlit Community Cloud, with explicit documentation of data limitations.
