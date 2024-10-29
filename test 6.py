import http.client
import json
import pandas as pd
import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta, timezone, time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import requests

# Function to fetch trading pairs from Coinbase API
def fetch_trading_pairs():
    conn = http.client.HTTPSConnection("api.exchange.coinbase.com")
    payload = ''
    headers = {
      'Content-Type': 'application/json',
      'User-Agent': 'PythonClient/1.0'
    }
    conn.request("GET", "/products", payload, headers)
    res = conn.getresponse()
    data = res.read()

    # Parse JSON data
    products = json.loads(data.decode("utf-8"))
    df = pd.DataFrame(products)

    # Extract relevant columns and filter only tradable pairs (status is 'online')
    df = df[['id', 'base_currency', 'quote_currency', 'status']]
    df = df[df['status'] == 'online']
    return df

# Fetch historical data block
def fetch_historical_data_block(product_id, start_time, end_time, granularity=300):
    url = f"https://api.exchange.coinbase.com/products/{product_id}/candles"

    params = {
        'start': start_time.isoformat(),
        'end': end_time.isoformat(),
        "granularity": granularity
    }

    response = requests.get(url, params=params, headers={"content-type": "application/json"})

    if response.status_code == 200:
        data = response.json()
        data_df = pd.DataFrame(data, columns=['time', 'low', 'high', 'open', 'close', 'volume'])
        data_df["date"] = pd.to_datetime(data_df['time'], unit='s')
        data_df.set_index('date', inplace=True)
        return data_df
    else:
        print(f"Error fetching data for {product_id}: {response.status_code}")
        return pd.DataFrame()

# Fetch trading pairs
products_df = fetch_trading_pairs()

# Fetch data for date
def product_data_for_date(product_id, indate):
    # Define Variables
    product = product_id
    current_datetime = datetime.now()

    input_date = datetime.strptime(indate, "%Y-%m-%d").date()
    
    timepair_list = [
        (time(0, 0, 0), time(3, 59, 0)),
        (time(4, 0, 0), time(7, 59, 0)),
        (time(8, 0, 0), time(11, 59, 0)),
        (time(12, 0, 0), time(15, 59, 0)),
        (time(16, 0, 0), time(19, 59, 0)),
        (time(20, 0, 0), time(23, 59, 0))
    ]

    datetimepair_list = []
    dataframes_list = []
    
    # Combine input_date with timepair_list to create datetimepair_list
    for start_time, end_time in timepair_list:
        datetimepair_list.append((datetime.combine(input_date, start_time), datetime.combine(input_date, end_time)))

    # Returns datetime pairs up to current_datetime
    current_datetime = datetime.now()
    for start, end in datetimepair_list:
        if start < current_datetime:
            if end > current_datetime:
                end = current_datetime
            df = fetch_historical_data_block(product, start, end)
            if not df.empty:
                reversed_rows_df = df.iloc[::-1].reset_index(drop=False)
                dataframes_list.append(reversed_rows_df)

    combined_df = pd.concat(dataframes_list, ignore_index=True) if dataframes_list else pd.DataFrame()

    return combined_df

# Print a single product example before extracting relevant columns
print(products_df.iloc[0])

# Fetch yesterday's data for BTC-USD using product_data_for_date function
btc_usd_candles = product_data_for_date('BTC-USD', (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d'))

# Function to create a tkinter window to display BTC-USD candle data
def create_candles_window(candles_data):
    # Create the main tkinter window
    root = tk.Tk()
    root.title("BTC-USD 24-Hour Candlestick Chart")

    # Extract candle data
    times = candles_data.index
    opens = candles_data['open']
    highs = candles_data['high']
    lows = candles_data['low']
    closes = candles_data['close']

    # Create a Matplotlib figure for the candlestick chart
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(times, opens, label='Open', color='blue')
    ax.plot(times, highs, label='High', color='green')
    ax.plot(times, lows, label='Low', color='red')
    ax.plot(times, closes, label='Close', color='black')
    ax.set_title("BTC-USD 24-Hour Candlestick Data")
    ax.set_xlabel("Time")
    ax.set_ylabel("Price (USD)")
    ax.legend()
    ax.grid(True)

    # Embed the plot in the tkinter window
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    # Run the tkinter main loop
    root.mainloop()

# Create and display the tkinter window with the BTC-USD candle data
create_candles_window(btc_usd_candles)
s