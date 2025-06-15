import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import ta

@st.cache_data
def load_data(symbol, start, end, interval):
    df = yf.download(symbol, start=start, end=end, interval=interval)
    # Fix timezone issue
    if df.index.tz is None:
        df.index = df.index.tz_localize('UTC').tz_convert('Europe/London')
    else:
        df.index = df.index.tz_convert('Europe/London')
    return df

st.title("Forex Chart Test")

symbol = st.text_input("Symbol", value="EURUSD=X")
start_date = st.date_input("Start Date", value=pd.to_datetime("2024-06-10"))
end_date = st.date_input("End Date", value=pd.to_datetime("2024-06-15"))
interval = st.selectbox("Interval", options=["1h", "4h"], index=0)

if start_date >= end_date:
    st.error("Start date must be before end date.")
else:
    df = load_data(symbol, start_date, end_date, interval)

    if df.empty:
        st.warning("No data loaded for the selected symbol and date range.")
    else:
        df['EMA_50'] = ta.trend.ema_indicator(df['Close'], window=50)
        df['EMA_200'] = ta.trend.ema_indicator(df['Close'], window=200)

        fig = go.Figure()
        fig.add_trace(go.Candlestick(
            x=df.index, open=df['Open'], high=df['High'],
            low=df['Low'], close=df['Close'], name='Candles'))
        fig.add_trace(go.Scatter(x=df.index, y=df['EMA_50'], name='EMA 50', line=dict(color='blue')))
        fig.add_trace(go.Scatter(x=df.index, y=df['EMA_200'], name='EMA 200', line=dict(color='orange')))

        st.plotly_chart(fig, use_container_width=True)
