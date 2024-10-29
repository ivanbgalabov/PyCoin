import http.client
import json
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go

# Establish a connection
conn = http.client.HTTPSConnection("api.exchange.coinbase.com")

# Prepare headers, including User-Agent
payload = ''
headers = {
    'Content-Type': 'application/json',
    'User-Agent': 'PythonClient/1.0'  # You can specify any User-Agent string here
}

# Define the endpoint URL
product_id = "BTC-USD"
granularity = 900  # 600 seconds = 10 minutes
start = "2024-10-29T00:00:00Z"  # Start in ISO 8601 format
end = "2024-10-29T01:00:00Z"  # End in ISO 8601 format
endpoint = f"/products/{product_id}/candles?granularity={granularity}&start={start}&end={end}"

# Make the GET request
conn.request("GET", endpoint, payload, headers)

# Get the response
res = conn.getresponse()
data = res.read()
# Decode and parse the JSON response
candles = json.loads(data)

# Convert the parsed data to a DataFrame
columns = ['date', 'low', 'high', 'open', 'close', 'volume']
df = pd.DataFrame(candles, columns=columns)

# Convert the timestamp from Unix to a readable datetime format
df['date'] = pd.to_datetime(df['date'], unit='s')

#df.set_index('date', inplace = True)

# Print the DataFrame
print(df)
data = df

fig = go.Figure(data=[go.Candlestick(
  x=data['date'],
  open=data['open'],
  high=data['high'],
  low=data['low'],
  close=data['close'],
  increasing_line_color='green',
  decreasing_line_color='red')])

fig.show()