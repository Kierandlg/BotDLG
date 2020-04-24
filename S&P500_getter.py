#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 15:32:56 2020

@author: kieran
"""

import bs4 as bs
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import os
import pandas as pd
import pandas_datareader.data as web
import pickle
import requests
import numpy as np

style.use('ggplot')


def save_sp500_tickers():
	resp = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
	soup = bs.BeautifulSoup(resp.text)
	table = soup.find('table', {'id': 'constituents'})
	tickers = []
	for row in table.findAll('tr')[1:25]:
		ticker = row.find('td').text.replace('\n','')
		#ticker = row.find_all('td') [0].text.replace('\n','')
		tickers.append(ticker)

	with open("sp500tickers.pickle", "wb") as f:
		pickle.dump(tickers, f)

	print(tickers)

	return  

#save_sp500_tickers()

### suite pour baptiste


def get_data_from_yahoo(reload_sp500=False):
	#vérifie si le fichier a déjà été chargé
	if reload_sp500:
		#stock le fichier dans une variable
		tickers = save_sp500_tickers()
	else:
		with open("sp500tickers.pickle", "rb") as f:
			#stock le fichier dans une variable
			tickers = pickle.load(f)

	#vérifie que le fichier d'accès existe dans l'actuel file
	if not os.path.exists('stock_dfs'):
		os.makedirs('stock_dfs')


	start = dt.datetime(2015,1,1)
	end = dt.datetime.today()

	#charge les données dans la fourchette temporelle, et ne les télécharge pas si déjà fait
	for ticker in tickers[:25]:
		print(ticker)
		if not os.path.exists('stock_dfs/{}.csv'.format(ticker)):
			df = web.DataReader(ticker.replace('.','-'), 'yahoo', start, end)
			df.to_csv('stock_dfs/{}.csv'.format(ticker.replace('.','-')))
		else:
			print('Already have {}'.format(ticker))

#get_data_from_yahoo()

def compile_data():
	with open("sp500tickers.pickle", "rb") as f:
		tickers = pickle.load(f)

	main_df = pd.DataFrame()

	for count, ticker in enumerate (tickers):
		df = pd.read_csv('stock_dfs/{}.csv'.format(ticker.replace('.','-')))
		df.set_index('Date', inplace=True)

		df.rename(columns = {'Adj Close':ticker}, inplace = True)       
		df.drop(['High','Low','Open','Close','Volume'], axis = 1, inplace=True)

		if main_df.empty:
			main_df = df
		else:
			main_df = main_df.join(df, how='outer')
		if count % 10 == 0:
			print(count)

	print(main_df.head())
	main_df.to_csv('sp500_joined_closes.csv')
#compile_data()

def visualize_data():
    df = pd.read_csv('sp500_joined_closes.csv')
    ##df['AAP'].plot()
    ##plt.show()
    df_corr = df.corr()
    print(df_corr)
    
    data = df_corr.values
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    
    heatmap = ax.pcolor(data, cmap=plt.cm.RdYlGn)
    fig.colorbar(heatmap)
    ax.set_xticks(np.arange(data.shape[0]) + 0.5, minor=False)
    ax.set_yticks(np.arange(data.shape[1]) + 0.5, minor=False)
    ax.invert_yaxis()
    ax.xaxis.tick_top()
    
    column_labels = df_corr.columns
    row_labels = df_corr.index

    ax.set_xtickslabels(column_labels)
    ax.set_ytickslabels(row_labels)
    plt.xticks(rotation=90)
    heatmap.set_clim(-1,1)
    plt.tight_layout()
    plt.show()
    

    
visualize_data()
