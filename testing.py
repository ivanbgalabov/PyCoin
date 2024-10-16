import requests
import time
import pandas as pd
from datetime import datetime, timedelta, date

def get_historical_data_block(product_id, start_time, end_time, granularity = 60):
	url = f"https://api.exchange.coinbase.com/products/{product_id}/candles"

	params = {
		'start': start_time.isoformat(),
		'end' : end_time.isoformat(),
		"granularity": granularity
	}

	response = requests.get(url, params = params, headers = {"content-type":"application/json"})

	if response.status_code == 200:
		data = response.json()
		data_df = pd.DataFrame(data, columns = ['time', 'low','high','open','close','volume'] )
		data_df 
		print("returned data frame")
		return data_df

	else:
		raise Exception(f"Error: {response.status_code}, {response.text}")

product_id = 'BTC-USD'
start_date = datetime(2024,10,10)
end_date = datetime(2024,10,11)

data = get_historical_data_block(product_id, start_date, end_date, granularity = 3600)


print(data_df)