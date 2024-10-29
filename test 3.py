from datetime import datetime, timedelta, date, time
import os
import pandas as pd


currentdate = date.today()
currentdatetime = datetime.now()
archivepath = "Archive"

def get_asset_data(asset, date1 = currentdate):
	
	asset = asset
	startdate = date1

	if isinstance(startdate, date):

		print("date1 is a date object")

	else:

		print("date1 is not a date object")

		startdate = datetime.strptime(startdate, "%Y-%m-%d").date()

	year = startdate.strftime("%Y")
	month = startdate.strftime("%m")

	filename = f"{asset}_{startdate}"
	folder_path = os.path.join(archivepath, asset, year, month)
	filepath = os.path.join(folder_path, filename)

	print(filename)
	print(folder_path)
	print(filepath)

	if not os.path.exists(folder_path):
		os.makedirs(folder_path)
		print(f"Created folder: {folder_path}")

	if os.path.exists(filepath):

		# Load the CSV file into a DataFrame if it exists
		df = pd.read_csv(filepath)
		return df
		print(f"Loaded existing file: {filepath}")

	else:
		pass
		# Load data for date from web
		#df = #get_historical_data(coin, date, date2)
		#return df


# def create_and_laod_data(asset, date, folder_path='Archive'):

# 	filename = f"{asset}_{date}.csv"
# 	filepath = os.path.join(folder_path, asset, filename)



get_asset_data('BTC', '2023-10-03')