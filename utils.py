
import pandas as pd
import datetime
import requests

def calculate_indicators(df):
    df['EMA_20'] = df['Close'].ewm(span=20, adjust=False).mean()
    df['EMA_50'] = df['Close'].ewm(span=50, adjust=False).mean()
    df['RSI'] = 100 - (100 / (1 + df['Close'].pct_change().rolling(14).mean()))
    df['MACD'] = df['Close'].ewm(span=12, adjust=False).mean() - df['Close'].ewm(span=26, adjust=False).mean()
    df['MACD_Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
    return df

def get_session_info(df, session_filter):
    latest = df.iloc[-1]
    price = latest['Close']
    status = "Neutral"
    if session_filter == "London":
        session_high = df.between_time("08:00", "16:00")['High'].max()
        session_low = df.between_time("08:00", "16:00")['Low'].min()
        if price > session_high:
            status = "Above London High 🚀"
        elif price < session_low:
            status = "Below London Low 🔻"
    return {"Last Price": price, "Session Status": status}

def get_forexfactory_news():
    return pd.DataFrame({
        "Time": ["14:00", "15:30"],
        "Event": ["CPI m/m", "Fed Chair Speech"],
        "Impact": ["High", "Medium"]
    })
