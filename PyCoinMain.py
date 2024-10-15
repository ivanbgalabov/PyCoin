#Variables:

# list_of_tradable_assets
# account_balance

import os
import pandas as pd
from datetime import datetime, date, timedelta
#filename = f"{asset}_{date}"

currentdate = date.today()
currentdatetime = datetime.now()

archivepath = "Archive"

if os.path.exists(archivepath):
	print("path exists")

else:
	print('path does not exists')

def create_and_laod_data(asset, date, folder_path='Archive'):

	filename = f"{asset}_{date}.csv"
	filepath = os.path.join(folder_path, asset, filename)

	

create_and_laod_data('btc', '2023-01-01')

exactdate = date(2024, 10, 3)
#exactdate2 = date.strpdate('2023-01-01', "%Y-%m-%d")



def get_asset_data(asset, date = currentdate):
	
	coin = asset
	startdate = date.strftime("%Y-%m-%d")
	date2 = date + timedelta(hours = 4)
	year = date.strftime("%Y")
	month = date.strftime("%m")

	filename = f"{asset}_{date}"
	folder_path = os.path.join(archivepath, asset, year, month)
	filepath = os.path.join(folder_path, filename)

	#1 check if folder exists
	if not os.path.exists(folder_path):
		os.makedirs(folder_path)
		print(f"Created folder: {folder_path}")

	if os.path.exists(filepath):

		# Load the CSV file into a DataFrame if it exists
		df = pd.read_csv(filepath)
		return df
		print(f"Loaded existing file: {filepath}")

	else:
		#get_historical_data(coin, date, date2)
		#start_time = startdate.datetime()
		print(startdate)


# def get_historical_data(product_id, start_time, end_time, granularity = 60):
# 	url = f"https://api.exchange.coinbase.com/products/{product_id}/candles"
# 	params = {
# 		'start' : start_time.isoformat()
# 		'end' : end_time.isoformat()
# 		'granularity' : granularity
# 	}
# 	response = request.get(url, params = params, headers = {"content-type":"appplication/json"})
# 	if response.status_code == 200:
# 		return response.json()
# 	else:
# 		raise Exception(f"Error: {response.status_code}, {response.text}")


print(get_asset_data(asset = "btc"))