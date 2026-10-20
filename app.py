
import pandas as pd
import plotly.express as px
import streamlit as st
from pathlib import Path

st.set_page_config(
    page_title="TrendLens | Fashion Intelligence",
    page_icon="✦",
    layout="wide"
)

ROOT = Path(__file__).parent
DATA_PATH = ROOT / "data" / "fashion_products.csv"

# --------------------------------------------------
# Styling: readable cards, metrics, and text
# --------------------------------------------------

st.markdown("""
<style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    h1, h2, h3 {
        letter-spacing: -0.03em;
    }

    /* Metric cards */
    [data-testid="stMetric"] {
        background-color: #f7f4ef !important;
        color: #222222 !important;
        padding: 16px 18px;
        border-radius: 12px;
        border: 1px solid #e5ded3;
    }

    [data-testid="stMetric"] label,
    [data-testid="stMetric"] [data-testid="stMetricValue"],
    [data-testid="stMetric"] [data-testid="stMetricDelta"] {
        color: #222222 !important;
    }

    /* Streamlit bordered containers */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #ffffff !important;
        border: 1px solid #e5e7eb !important;
        border-radius: 12px;
    }

    [data-testid="stVerticalBlockBorderWrapper"] p,
    [data-testid="stVerticalBlockBorderWrapper"] li,
    [data-testid="stVerticalBlockBorderWrapper"] label,
    [data-testid="stVerticalBlockBorderWrapper"] h1,
    [data-testid="stVerticalBlockBorderWrapper"] h2,
    [data-testid="stVerticalBlockBorderWrapper"] h3,
    [data-testid="stVerticalBlockBorderWrapper"] h4 {
        color: #222222 !important;
    }

    .small-note {
        color: #666666;
        font-size: 0.9rem;
    }

    /* Cards for real-world shopping signals */
    .trend-card {
        background-color: #ffffff;
        color: #222222;
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 14px;
        min-height: 235px;
    }

    .trend-card h4 {
        color: #222222 !important;
        margin-top: 10px;
        margin-bottom: 10px;
    }

    .trend-card p {
        color: #444444 !important;
        line-height: 1.55;
    }

    .trend-tag {
        display: inline-block;
        background-color: #f2e8dc;
        color: #603d28 !important;
        padding: 5px 10px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
    }

    .trend-card a {
        color: #795548 !important;
        font-weight: 600;
        text-decoration: underline;
    }

    /* Sidebar contrast */
    [data-testid="stSidebar"] {
        background-color: #f7f4ef;
    }

    /* Improve general text readability */
    .stMarkdown p,
    .stMarkdown li {
        line-height: 1.55;
    }
</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# Load dataset
# --------------------------------------------------

@st.cache_data
def load_data():
    data = pd.read_csv(DATA_PATH)

    required = {
        "category",
        "style",
        "color",
        "season",
        "month",
        "price_usd",
        "search_interest",
        "demand_score",
        "sales_index",
        "sustainability_score"
    }

    missing = required - set(data.columns)

    if missing:
        raise ValueError(
            f"Dataset is missing required columns: "
            f"{', '.join(sorted(missing))}"
        )

    return data


try:
    df = load_data()
except FileNotFoundError:
    st.error(
        "Could not find the dataset. Make sure "
        "'fashion_products.csv' is inside the data folder."
    )
    st.stop()
except Exception as error:
    st.error(f"Could not load the dataset: {error}")
    st.stop()


# --------------------------------------------------
# Header
# --------------------------------------------------

st.title("✦ TrendLens")
st.caption("Fashion trend intelligence, made visual.")

st.markdown(
    "Explore which styles are gaining attention, where demand appears "
    "strongest, and how price and sustainability vary across a fashion catalog."
)

st.info(
    "Demo mode: the included dataset is synthetic sample data, not live "
    "consumer or sales data. Use the analytics as a product demonstration, "
    "not as evidence of actual market demand."
)


# --------------------------------------------------
# Sidebar filters
# --------------------------------------------------

with st.sidebar:
    st.header("Explore the catalog")

    categories = sorted(df["category"].dropna().unique())
    seasons = sorted(df["season"].dropna().unique())

    selected_categories = st.multiselect(
        "Categories",
        categories,
        default=categories
    )

    selected_seasons = st.multiselect(
        "Seasons",
        seasons,
        default=seasons
    )

    max_price = max(10, int(df["price_usd"].max() + 10))

    price_range = st.slider(
        "Price range (USD)",
        min_value=0,
        max_value=max_price,
        value=(0, max_price),
        step=5
    )

    min_demand = st.slider(
        "Minimum demand score",
        min_value=0,
        max_value=100,
        value=0,
        step=5
    )

    st.caption("Filters update the demo analytics below.")


# --------------------------------------------------
# Filter data
# --------------------------------------------------

filtered = df[
    df["category"].isin(selected_categories)
    & df["season"].isin(selected_seasons)
    & df["price_usd"].between(price_range[0], price_range[1])
    & (df["demand_score"] >= min_demand)
].copy()

if filtered.empty:
    st.warning(
        "No products match those filters. Select more categories or seasons, "
        "widen your price range, or lower the minimum demand score."
    )
    st.stop()


# --------------------------------------------------
# Calculate style scores
# --------------------------------------------------

trend_table = filtered.groupby("style", as_index=False).agg(
    avg_search_interest=("search_interest", "mean"),
    avg_demand=("demand_score", "mean"),
    products=("product_id", "count"),
    avg_sales_index=("sales_index", "mean")
)

trend_table["trend_score"] = (
    0.55 * trend_table["avg_search_interest"]
    + 0.45 * trend_table["avg_demand"]
).round(1)

trend_table = trend_table.sort_values(
    "trend_score",
    ascending=False
)


# --------------------------------------------------
# Summary metrics
# --------------------------------------------------

st.subheader("Your catalog at a glance")

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Products analyzed",
    f"{len(filtered):,}"
)

c2.metric(
    "Top style",
    str(trend_table.iloc[0]["style"])
)

c3.metric(
    "Average demand score",
    f"{filtered['demand_score'].mean():.1f}/100"
)

c4.metric(
    "Average listed price",
    f"${filtered['price_usd'].mean():.0f}"
)


# --------------------------------------------------
# Chart 1: Style momentum
# Chart 2: Search interest versus demand
# --------------------------------------------------

st.divider()

left, right = st.columns([1.15, 1])

with left:
    st.subheader("Style momentum")

    fig = px.bar(
        trend_table.sort_values("trend_score"),
        x="trend_score",
        y="style",
        orientation="h",
        color="trend_score",
        color_continuous_scale="Sunset",
        labels={
            "trend_score": "Trend score",
            "style": "Style"
        },
        hover_data={
            "avg_search_interest": ":.1f",
            "avg_demand": ":.1f",
            "products": True
        }
    )

    fig.update_layout(
        coloraxis_showscale=False,
        margin=dict(l=8, r=8, t=10, b=8),
        height=420,
        paper_bgcolor="white",
        plot_bgcolor="white",
        font_color="#222222"
    )

    st.plotly_chart(fig, use_container_width=True)

with right:
    st.subheader("What is driving attention?")

    fig2 = px.scatter(
        filtered,
        x="search_interest",
        y="demand_score",
        color="category",
        size="sales_index",
        hover_name="product_id",
        hover_data=[
            "style",
            "color",
            "price_usd",
            "season"
        ],
        labels={
            "search_interest": "Search interest index",
            "demand_score": "Demand score"
        }
    )

    fig2.update_layout(
        margin=dict(l=8, r=8, t=10, b=8),
        height=420,
        paper_bgcolor="white",
        plot_bgcolor="white",
        font_color="#222222"
    )

    st.plotly_chart(fig2, use_container_width=True)


# --------------------------------------------------
# Chart 3: Category landscape
# Chart 4: Color mix
# --------------------------------------------------

left2, right2 = st.columns(2)

with left2:
    st.subheader("Category landscape")

    cat = filtered.groupby("category", as_index=False).agg(
        products=("product_id", "count"),
        avg_price=("price_usd", "mean"),
        avg_demand=("demand_score", "mean"),
        avg_sustainability=("sustainability_score", "mean")
    )

    fig3 = px.bar(
        cat.sort_values("avg_demand"),
        x="category",
        y="avg_demand",
        color="avg_price",
        color_continuous_scale="Teal",
        hover_data=[
            "products",
            "avg_sustainability"
        ],
        labels={
            "avg_demand": "Average demand",
            "category": "",
            "avg_price": "Average price ($)"
        }
    )

    fig3.update_layout(
        margin=dict(l=8, r=8, t=10, b=8),
        height=350,
        paper_bgcolor="white",
        plot_bgcolor="white",
        font_color="#222222"
    )

    st.plotly_chart(fig3, use_container_width=True)

with right2:
    st.subheader("Color mix")

    color_counts = (
        filtered["color"]
        .value_counts()
        .rename_axis("color")
        .reset_index(name="products")
    )

    fig4 = px.pie(
        color_counts,
        names="color",
        values="products",
        hole=0.55,
        color_discrete_sequence=px.colors.qualitative.Pastel
    )

    fig4.update_layout(
        margin=dict(l=8, r=8, t=10, b=8),
        height=350,
        legend_title_text="",
        paper_bgcolor="white",
        font_color="#222222"
    )

    st.plotly_chart(fig4, use_container_width=True)


# --------------------------------------------------
# Buyer's brief
# --------------------------------------------------

st.divider()
st.subheader("A quick buyer's brief")

top = trend_table.iloc[0]

top_category = (
    filtered.groupby("category")["demand_score"]
    .mean()
    .sort_values(ascending=False)
)

top_color = filtered["color"].value_counts()

sustainability_avg = filtered["sustainability_score"].mean()

st.markdown(
    f"- **Style to investigate:** {top['style']} has the highest "
    f"combined trend score in this filtered sample "
    f"(**{top['trend_score']:.1f}/100**).\n"
    f"- **Category to investigate:** {top_category.index[0]} has the "
    f"highest average demo demand score "
    f"(**{top_category.iloc[0]:.1f}/100**).\n"
    f"- **Most common color:** {top_color.index[0]} appears most often "
    f"in the filtered catalog.\n"
    f"- **Sustainability snapshot:** the average sustainability score "
    f"is **{sustainability_avg:.1f}/100**."
)

st.caption(
    "Trend score = 55% average search-interest index + 45% average "
    "demand score. These are illustrative demo metrics, not validated forecasts."
)


# --------------------------------------------------
# Real-world shopping signals
# --------------------------------------------------

st.divider()

st.header("What shoppers are buying now")

st.markdown(
    "A separate look at reported shopping activity and current fashion "
    "coverage. These external sources are not calculated from the synthetic "
    "catalog above."
)

st.caption(
    "Research snapshot: October 2026. Evidence varies by source: "
    "some report purchases or spending, while others identify editorial trends."
)

trend_col1, trend_col2 = st.columns(2)

with trend_col1:
    st.markdown("""
    <div class="trend-card">
        <span class="trend-tag">Reported purchases</span>
        <h4>Retro sneakers and ballet-style flats</h4>
        <p>
        Who What Wear's reader shopping analysis for August 1 through
        September 25, 2026, identified Adidas Samba OG sneakers as its
        most-purchased item. Other popular items included Adidas Tokyo
        sneakers and ballet-inspired footwear.
        </p>
        <p>
        <b>What to track:</b> sneaker silhouettes, flat shoes, brand,
        price, and product availability.
        </p>
        <p>
        <a href="https://www.whowhatwear.com/fashion/shopping/best-selling-who-what-wear-items-fall-2026"
        target="_blank" rel="noopener noreferrer">
        Read the shopping analysis ↗
        </a>
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="trend-card">
        <span class="trend-tag">Reported purchases</span>
        <h4>Wearable wardrobe staples</h4>
        <p>
        The same shopping report featured cardigans, perfect-fit T-shirts,
        rollneck tops, and satin wide-leg pull-on pants among popular items.
        </p>
        <p>
        <b>What to track:</b> everyday versatility, price points, repeat
        purchases, and how basics compare with statement pieces.
        </p>
        <p>
        <a href="https://www.whowhatwear.com/fashion/shopping/best-selling-who-what-wear-items-fall-2026"
        target="_blank" rel="noopener noreferrer">
        Explore the reported bestsellers ↗
        </a>
        </p>
    </div>
    """, unsafe_allow_html=True)

with trend_col2:
    st.markdown("""
    <div class="trend-card">
        <span class="trend-tag">Spending data</span>
        <h4>Secondhand and resale fashion</h4>
        <p>
        Consumer Edge reported that U.S. consignment and thrift spending
        in apparel and accessories grew 24.1% year over year in Q3 2026
        in its card-spending dataset.
        </p>
        <p>
        <b>What to track:</b> resale categories, secondhand pricing,
        brand resale value, and sustainability-related shopping signals.
        </p>
        <p>
        <a href="https://www.consumeredge.com/resources/insight-flash/consumer-spending-trends-heading-into-the-holiday-season/"
        target="_blank" rel="noopener noreferrer">
        Read the spending report ↗
        </a>
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="trend-card">
        <span class="trend-tag">Current trend coverage</span>
        <h4>Fall outerwear and updated silhouettes</h4>
        <p>
        Recent fall fashion coverage highlights funnel-neck jackets,
        barrel-cut jeans, half-zip knits, bowler bags, and rich oxblood
        shades as styles to watch.
        </p>
        <p>
        <b>Evidence type:</b> editorial trend coverage. These styles
        should not be treated as verified sales leaders without
        independent sales data.
        </p>
        <p>
        <a href="https://www.instyle.com/nyc-fall-fashion-trends-amazon-october-2026-12174039"
        target="_blank" rel="noopener noreferrer">
        Read the fall trend roundup ↗
        </a>
        </p>
    </div>
    """, unsafe_allow_html=True)

st.info(
    "Research limitation: the sources above cover specific readers, "
    "spending datasets, or editorial observations. They do not represent "
    "every shopper or the entire global fashion market. This section is "
    "a manually curated research snapshot, not a live sales feed."
)


# --------------------------------------------------
# View and download filtered data
# --------------------------------------------------

with st.expander("View and download the filtered data"):
    st.dataframe(
        filtered,
        use_container_width=True,
        hide_index=True
    )

    st.download_button(
        "Download filtered CSV",
        filtered.to_csv(index=False).encode("utf-8"),
        file_name="trendlens_filtered_products.csv",
        mime="text/csv"
    )


# --------------------------------------------------
# Footer
# --------------------------------------------------

st.markdown("---")

st.caption(
    "TrendLens | Fashion Intelligence Portfolio MVP | "
    "Built with Python, pandas, Plotly, and Streamlit"
)
