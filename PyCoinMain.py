import http.client
import json
import pandas as pd
import customtkinter as ctk
from datetime import datetime, timedelta, timezone, time, date
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import requests
import os
import websocket
import threading

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

# Fetch product data for date from archive/web
def get_product_data(asset, indate=None):
    # Set default date to today if not provided
    if indate is None:
        date = datetime.now().date()
    elif isinstance(indate, str):
        date = datetime.strptime(indate, '%Y-%m-%d').date()
    else:
        date = indate

    archivepath = 'Archive'
    product = asset
    startdate = date

    year = date.strftime("%Y")
    month = date.strftime("%m")

    filename = f"{asset}_{date}.csv"
    folder_path = os.path.join(archivepath, asset, year, month)
    filepath = os.path.join(folder_path, filename)
    
    # Check if folder exists
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Created folder: {folder_path}")

    if os.path.exists(filepath):
        # If the date is today, fetch new data and overwrite the existing file
        if date == datetime.now().date():
            df = product_data_for_date(product, startdate.strftime('%Y-%m-%d'))
            if not df.empty:
                df.to_csv(filepath, index=False)
                print(f"Updated data for today and saved to: {filepath}")
            return df
        else:
            # Load the CSV file into a DataFrame if it exists
            print(f"Loaded existing file: {filepath}")
            df = pd.read_csv(filepath)
            return df
    else:
        # Fetch new data and save it
        df = product_data_for_date(product, startdate.strftime('%Y-%m-%d'))
        if not df.empty:
            df.to_csv(filepath, index=False)
            print(f"Saved new data to: {filepath}")
        return df

# Function to fetch data between start and end dates
def get_product_data_range(asset, startdate, enddate):
    current_date = startdate
    monthly_dataframes = []
    combined_dataframes = []
    current_month = startdate.month

    while current_date <= enddate:
        df = get_product_data(asset, current_date.strftime('%Y-%m-%d'))
        if not df.empty:
            combined_dataframes.append(df)

        # Check if we have reached the end of the current month or the end date
        if current_date.month != current_month or current_date == enddate:
            if combined_dataframes:
                monthly_df = pd.concat(combined_dataframes, ignore_index=True)
                monthly_dataframes.append(monthly_df)
                combined_dataframes = []
            current_month = current_date.month

        current_date += timedelta(days=1)

    final_combined_df = pd.concat(monthly_dataframes, ignore_index=True) if monthly_dataframes else pd.DataFrame()
    return final_combined_df

# Real-time data streaming via WebSocket
def on_message(ws, message):
    data = json.loads(message)
    if 'type' in data and data['type'] == 'ticker':
        product_id = data['product_id']
        price = float(data['price'])
        time_stamp = pd.to_datetime(data['time'])
        
        # Update the dataframe for the current date
        global products_df
        if product_id in products_df['id'].values:
            new_data = {'time': time_stamp.timestamp(), 'price': price}
            if product_id in real_time_data:
                real_time_data[product_id].append(new_data)
            else:
                real_time_data[product_id] = [new_data]
            print(f"Updated {product_id} with price: {price} at {time_stamp}")

real_time_data = {}

# Start WebSocket streaming
def start_websocket():
    ws_url = "wss://ws-feed.exchange.coinbase.com"
    ws = websocket.WebSocketApp(ws_url, on_message=on_message)
    ws.run_forever()

# Run WebSocket in a separate thread
websocket_thread = threading.Thread(target=start_websocket)
websocket_thread.daemon = True
websocket_thread.start()

# Print a single product example before extracting relevant columns
print(products_df.iloc[0])

# Fetch yesterday's data for BTC-USD using product_data_for_date function
btc_usd_candles = get_product_data('BTC-USD', date(2024, 10, 28).strftime('%Y-%m-%d'))

start_date = datetime(2024, 10, 1).date()
end_date = datetime(2024, 10, 31).date()

btc_usd_monthly_data = get_product_data_range('BTC-USD', start_date, end_date)

# Function to create a tkinter window to display BTC-USD candle data
def create_candles_window(candles_data):
    def on_closing():
        root.quit()
        root.destroy()
    # Create the main tkinter window
    root = ctk.CTk()
    root.title("BTC-USD Real-Time Candlestick Chart")

    # Extract initial candle data
    times = pd.to_datetime(candles_data['time'], unit='s')
    opens = candles_data['open']
    highs = candles_data['high']
    lows = candles_data['low']
    closes = candles_data['close']

    # Create a Matplotlib figure for the candlestick chart
    fig, ax = plt.subplots(figsize=(10, 5))
    line_open, = ax.plot(times, opens, label='Open', color='blue')
    line_high, = ax.plot(times, highs, label='High', color='green')
    line_low, = ax.plot(times, lows, label='Low', color='red')
    line_close, = ax.plot(times, closes, label='Close', color='black')
    ax.set_title("BTC-USD Real-Time Candlestick Data")
    ax.set_xlabel("Time")
    fig.autofmt_xdate()
    ax.set_ylabel("Price (USD)")
    ax.legend()
    ax.grid(True)

    # Embed the plot in the tkinter window
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=ctk.BOTH, expand=True)

    def update_plot():
        print("Updating plot with new real-time data...")
        # Get the latest data from the WebSocket feed
        if 'BTC-USD' in real_time_data and real_time_data['BTC-USD']:
            latest_data = pd.DataFrame(real_time_data['BTC-USD'])
            latest_data['time'] = pd.to_datetime(latest_data['time'], unit='s')

            # Update plot data
            line_open.set_xdata(latest_data['time'])
            line_open.set_ydata(latest_data['price'])
            line_high.set_xdata(latest_data['time'])
            line_high.set_ydata(latest_data['price'])
            line_low.set_xdata(latest_data['time'])
            line_low.set_ydata(latest_data['price'])
            line_close.set_xdata(latest_data['time'])
            line_close.set_ydata(latest_data['price'])

            # Rescale axes
            ax.relim()
            ax.autoscale_view()

            # Redraw canvas
            canvas.draw()

        # Schedule the next update
        root.after(5000, update_plot)  # Update every 5 seconds

    # Start the periodic update
    root.after(5000, update_plot)

    # Run the tkinter main loop
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

# Create and display the tkinter window with the BTC-USD candle data
create_candles_window(btc_usd_monthly_data)
