
import streamlit as st
import pandas as pd
import yfinance as yf
import datetime
from utils import calculate_indicators, get_session_info, get_forexfactory_news

st.set_page_config(page_title="RedtoGreen Screener", page_icon="📈", layout="wide")

st.markdown("""<style>
    .main {background-color: #0e1117; color: white;}
    footer {visibility: visible;}
</style>""", unsafe_allow_html=True)

# Header
st.title("🚦 RedtoGreen Screener")
st.caption("Trade with clarity. React with confidence. Grow with RedtoGreen.")

# Sidebar filters
asset_class = st.sidebar.selectbox("Select Asset Class", ["Forex", "Crypto", "Stocks"])
session = st.sidebar.selectbox("Session Filter", ["All", "Asia", "London", "New York"])

# Asset list (sample)
assets = {
    "Forex": ["EURUSD=X", "GBPUSD=X", "USDJPY=X"],
    "Crypto": ["BTC-USD", "ETH-USD"],
    "Stocks": ["AAPL", "TSLA", "MSFT"]
}

symbols = assets.get(asset_class, [])

# Display each symbol's analysis
for symbol in symbols:
    try:
        data = yf.download(symbol, period="7d", interval="15m")
        df = calculate_indicators(data)
        session_data = get_session_info(df, session)

        st.subheader(f"{symbol} 📊")
        st.line_chart(df['Close'])
        st.write(session_data)

    except Exception as e:
        st.error(f"Failed to load data for {symbol}: {e}")

# News Section
st.markdown("### 📰 Market News (ForexFactory)")
news_df = get_forexfactory_news()
st.dataframe(news_df)

# Footer with About Page
st.markdown("""
---
🔗 [About RedtoGreen Screener](https://redtogreen.app/about)
""")
