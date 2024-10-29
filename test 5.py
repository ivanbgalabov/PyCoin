import http.client
import json
import pandas as pd

# Establish the connection
conn = http.client.HTTPSConnection("api.exchange.coinbase.com")

# Prepare headers
payload = ''
headers = {
  'Content-Type': 'application/json',
  'User-Agent': 'PythonClient/1.0'
}

# Make the GET request to get all products (trading pairs)
conn.request("GET", "/products", payload, headers)
res = conn.getresponse()
data = res.read()

# Decode and parse the JSON response
products = json.loads(data.decode("utf-8"))

# Convert the JSON data into a Pandas DataFrame
df = pd.DataFrame(products)

# Print the DataFrame
print(df)

# Optionally, filter and display only specific columns
print(df[['id', 'base_currency', 'quote_currency', 'status']])