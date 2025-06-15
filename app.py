import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import ta

# === Parameters ===
symbol = 'EURUSD=X'
start_date = '2024-06-10'
end_date = '2024-06-15'
interval = '1h'

# === Load & Localize Data ===
df = yf.download(symbol, start=start_date, end=end_date, interval=interval)
df.dropna(inplace=True)
df.index = df.index.tz_localize('UTC').tz_convert('Europe/London')

# === Indicators ===
df['EMA_50'] = ta.trend.ema_indicator(df['Close'], window=50)
df['EMA_200'] = ta.trend.ema_indicator(df['Close'], window=200)

# === Session Assignment ===
df['Hour'] = df.index.hour
df['Date'] = df.index.date
df['Session'] = pd.cut(
    df['Hour'], bins=[0, 7, 14, 21, 24],
    labels=['Asian', 'London', 'NY', 'Asian'], right=False
)

# === Auto Fib per Session ===
fib_shapes = []
fib_annotations = []

fib_colors = {
    'Asian': 'cyan',
    'London': 'yellow',
    'NY': 'magenta'
}

fib_ratios = {
    '0.0%': 0.0,
    '23.6%': 0.236,
    '38.2%': 0.382,
    '50.0%': 0.5,
    '61.8%': 0.618,
    '78.6%': 0.786,
    '100.0%': 1.0
}

# Only recent day(s) — adjust range if needed
last_dates = df['Date'].unique()[-2:]  # e.g., last 2 days

for date in last_dates:
    day_data = df[df['Date'] == date]
    for session in ['Asian', 'London', 'NY']:
        session_data = day_data[day_data['Session'] == session]
        if not session_data.empty:
            session_high = session_data['High'].max()
            session_low = session_data['Low'].min()
            color = fib_colors[session]
            for label, ratio in fib_ratios.items():
                level = session_low + (session_high - session_low) * ratio
                fib_shapes.append(dict(
                    type='line',
                    xref='x', yref='y',
                    x0=session_data.index[0],
                    x1=session_data.index[-1],
                    y0=level, y1=level,
                    line=dict(dash='dot', color=color, width=1),
                ))
                fib_annotations.append(dict(
                    x=session_data.index[-1],
                    y=level,
                    xref='x', yref='y',
                    text=f"{session} {label}",
                    showarrow=False,
                    font=dict(color=color, size=9)
                ))

# === EMA Cross ===
df['EMA_Cross'] = df['EMA_50'] - df['EMA_200']
cross_up = df[(df['EMA_Cross'] > 0) & (df['EMA_Cross'].shift(1) < 0)]
cross_down = df[(df['EMA_Cross'] < 0) & (df['EMA_Cross'].shift(1) > 0)]

# === Plot ===
fig = go.Figure()

fig.add_trace(go.Candlestick(x=df.index, open=df['Open'], high=df['High'],
                             low=df['Low'], close=df['Close'], name='Candles'))

fig.add_trace(go.Scatter(x=df.index, y=df['EMA_50'], name='EMA 50', line=dict(color='blue')))
fig.add_trace(go.Scatter(x=df.index, y=df['EMA_200'], name='EMA 200', line=dict(color='orange')))

fig.add_trace(go.Scatter(
    x=cross_up.index, y=cross_up['Close'],
    mode='markers', marker=dict(symbol='triangle-up', size=10, color='lime'),
    name='Bullish Cross'
))
fig.add_trace(go.Scatter(
    x=cross_down.index, y=cross_down['Close'],
    mode='markers', marker=dict(symbol='triangle-down', size=10, color='red'),
    name='Bearish Cross'
))

# === Layout ===
fig.update_layout(
    title=f"{symbol} Forex Chart with Auto Fib Levels per Session",
    xaxis_title="Time",
    yaxis_title="Price",
    template='plotly_dark',
    height=800,
    shapes=fib_shapes,
    annotations=fib_annotations,
    legend=dict(orientation='h', y=-0.2)
)

fig.show()
