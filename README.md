# TrendLens — Fashion Trend Analytics

A compact, interactive fashion intelligence dashboard built with Python, pandas, Plotly, and Streamlit.

## What it does
- Filters a catalog by category, season, price, and minimum demand score.
- Ranks styles using a transparent trend score.
- Compares search interest and demand, category-level demand/pricing, and color mix.
- Produces a short buyer's brief from the current filters.
- Lets users inspect and download filtered data.

## Important data note
The included 500-row dataset is **synthetic demo data** created to make the project run immediately. It is not scraped from a retailer, and it does not represent real consumer behavior or current fashion trends. Do not present the demo findings as actual market research.

## Run locally
Python 3.10+ recommended.

### Windows (PowerShell)
```powershell
cd TrendLens
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

If PowerShell blocks activation, use:
```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```

The app opens in your browser. Stop it with `Ctrl+C` in the terminal.

## Trend score
For the demo, the trend score is:

`0.55 × average search_interest + 0.45 × average demand_score`

It is a descriptive ranking formula, not a trained forecasting model. The dashboard states this explicitly.

## Dataset fields
| Field | Meaning |
|---|---|
| `product_id` | Demo product identifier |
| `category`, `style`, `color`, `season`, `month` | Product descriptors |
| `price_usd` | Illustrative listed price |
| `search_interest` | Synthetic 0–100 attention index |
| `demand_score` | Synthetic 0–100 demand score |
| `sales_index` | Synthetic relative sales index |
| `sustainability_score` | Synthetic 0–100 score |

## Next step (only if you want to extend it)
Replace the demo CSV with a responsibly sourced, licensed dataset that uses the same columns. Keep the data-source and limitations documented.

## Portfolio description
**TrendLens | Fashion Trend Analytics Dashboard**  
Built an interactive Python dashboard to explore style momentum, category demand, price positioning, and color mix. Developed a transparent trend-scoring method, filterable visual analytics, and downloadable data views using pandas, Plotly, and Streamlit. Used clearly labeled synthetic data to make the product runnable without relying on unauthorized scraping or unsupported market claims.
