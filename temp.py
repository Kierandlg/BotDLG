# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
#pour faire tourner téléchargez bien datareader papa et chloé
import pandas_datareader.data as web

style.use('ggplot')

"""

start = dt.datetime(2000,1,1)
end = dt.datetime(2020,3,19)


#df = dataframe
df = web.DataReader('DAX','yahoo', start, end)

#juste pour print
print(df)

#pour download en csv
df.to_csv('data.csv')

"""


#lecture csv existant en console
df = pd.read_csv('data.csv', parse_dates = True, index_col = 0)
#print(df.head())
df.plot()
#pour afficher un param précis, juste écrire: df[high].plot()    ou autre
print(df[['Open','High']])





plt.show()