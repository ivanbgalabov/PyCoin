#MODULES

import os
import requests
import pandas as pd
from datetime import datetime, date, timedelta, time
#filename = f"{asset}_{date}"

#GLOBAL VARIABLES

currentdate = date.today()
currentdatetime = datetime.now()
archivepath = "Archive"

#GLOBAL FUNCTIONS

# def get_coinbase_product_list():
# 	url = 'https://api.exchange.com/products'
# 	response = requests.get(url)
# 	if response.status_code == 200:

# 		products = response.json()
# 		return products
# 	else:
# 		print(F"Error fetching products: {response.status_code}")

# products = get_coinbase_product_list()
# print(products)

def check_path(path='Archive'):

	if os.path.exists(path):
		print("Path exists")

	else:
		print('Path does not exists')

def create_and_laod_data(asset, date, folder_path='Archive'):

	filename = f"{asset}_{date}.csv"
	filepath = os.path.join(folder_path, asset, filename)

	

create_and_laod_data('btc', '2023-01-01')

exactdate = date(2024, 10, 3)
#exactdate2 = date.strpdate('2023-01-01', "%Y-%m-%d")



def get_asset_data(asset, date = currentdate):
	
	coin = asset
	startdate = date
	year = date.strftime("%Y")
	month = date.strftime("%m")

	filename = f"{asset}_{date}"
	folder_path = os.path.join(archivepath, asset, year, month)
	filepath = os.path.join(folder_path, filename)
	if type(currentdate):
		pass

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
		df = #get_historical_data(coin, date, date2)
		#start_time = startdate.datetime()
		print(startdate)


def get_historical_data_block(product_id, start_time = currentdate, end_time = currentdatetime, granularity = 60):

	start = start_time
	end = end_time

	url = f"https://api.exchange.coinbase.com/products/{product_id}/candles"
	params = {
	 	'start' : start_time.isoformat(),
	 	'end' : end_time.isoformat(),
	 	'granularity' : granularity
	 }
	response = requests.get(url, params = params, headers = {"content-type":"appplication/json"})
	if response.status_code == 200:
		print("Response = True")
		return   response.json()
	else:
	 	raise Exception(f"Error: {response.status_code}, {response.text}")



# def get_data(ticker, date):
	
# 	asset = ticker
# 	iso_date = date
# 	datetime_object_atzero = datetime.fromisoformat(iso_date)
# 	data_blocks_list = []
# 	timeblock_pairs = [("00:00:00","04:00:00"),
# 	("04:00:00","08:00:00"),
# 	("08:00:00","12:00:00"),
# 	("12:00:00","16:00:00"),
# 	("16:00:00","20:00:00"),
# 	("20:00:00","23:59:00")]
	
# 	print(iso_date)
# 	print(asset)
# 	print(datetime_object_atzero)

# 	for (start,end) in timeblock_pairs:

# 		start_datetime_iso = f"{iso_date} {start}" 
# 		start_datetime_obj = datetime.fromisoformat(start_datetime_iso)

# 		end_datetime_iso = f"{iso_date} {end}" 
# 		end_datetime_obj = datetime.fromisoformat(end_datetime_iso)

# 		data_block = get_historical_data_block(product_id= asset, start_time = start_datetime_obj, end_time = end_datetime_obj)

# 		data_blocks_list.add(data_block)



# 		print(data_blocks_list)


iso_date_string  = "2024-10-15"
date_object = datetime.fromisoformat(iso_date_string)

#get_data("BTC_USD", "2024-10-15")

print(type(exactdate))