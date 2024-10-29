from datetime import datetime, timedelta, date, time
import pandas as pd
import requests
import matplotlib.pyplot as plt
import plotly.graph_objects as go

def fetch_historical_data_block(product_id, start_time, end_time, granularity = 300):
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
		
		data_df["date"] = pd.to_datetime(data_df['time'], unit = 's')

		data_df.set_index('date', inplace = True)
		
		return data_df

	else:
		raise Exception(f"Error: {response.status_code}, {response.text}")


def product_data_for_date(product_id,indate):

	#Define Variables
	product = product_id
	currentdatetime = datetime.now()

	inputdate = datetime.strptime(indate, "%Y-%m-%d").date()
	
	timepair_list = [(time(0,0,0,),time(3,59,0)),
	(time(4,0,0),time(7,59,0)),
	(time(8,0,0),time(11,59,0)),
	(time(12,0,0),time(15,59,0)),
	(time(16,0,0),time(19,59,0)),
	(time(20,0,0),time(23,59,0))]

	datetimepair_list = []
	dataframes_list = []
	
	#Combine inputdate with Datetimepair list to create datetimepair list
	for starttime,endtime in timepair_list:
		datetimepair_list.append((datetime.combine(inputdate,starttime),datetime.combine(inputdate,endtime)))

	#Returns datetime pairs up to currentdatetime.now
	for entry in datetimepair_list:
		start, end = entry
		
		if start < datetime.now():

			if end < datetime.now():
				df = fetch_historical_data_block(product,start,end)
				reversed_rows_df = df.iloc[::-1].reset_index(drop=False)
				dataframes_list.append(reversed_rows_df)
				
			else:
				end = datetime.now()
				df = fetch_historical_data_block(product,start,end)
				reversed_rows_df = df.iloc[::-1].reset_index(drop=False)
				dataframes_list.append(reversed_rows_df)

	combined_df = pd.concat(dataframes_list, ignore_index=True)

	return combined_df





		# if end > datetime.now() :
		# 	print(f"get historical data {start}, {end} )")
		# else:
		# 	print(f" now {start}, {currentdatetime}")


data = blocks("BTC-USD","2024-10-29")

print(data)
#data.plot( x = 'date', y='open')
#plt.show()

fig = go.Figure(data=[go.Candlestick(
	x=data['date'],
	open=data['open'],
	high=data['high'],
	low=data['low'],
	close=data['close'],
	increasing_line_color='green',
	decreasing_line_color='red')])

fig.show()