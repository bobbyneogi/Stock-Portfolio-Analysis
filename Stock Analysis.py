import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime

tesla = pd.read_csv('TESLA 5 years.csv')
tesla['Date'] = tesla['Date'].apply(pd.to_datetime)
tesla.set_index('Date',inplace=True)
gm = pd.read_csv('GM 5 years.csv')
gm['Date'] = gm['Date'].apply(pd.to_datetime)
gm.set_index('Date',inplace=True)
toyota = pd.read_csv('Toyota 5 years.csv')
toyota['Date'] = toyota['Date'].apply(pd.to_datetime)
toyota.set_index('Date',inplace=True)

#sorting the index
toyota.sort_index(inplace=True)
gm.sort_index(inplace=True)
tesla.sort_index(inplace=True)

#converting the volume column to float
def value_to_float(x):
    if type(x) == float or type(x) == int:
        return x
    if 'K' in x:
        if len(x) > 1:
            return float(x.replace('K', '')) * 1000
        return 1000.0
    if 'M' in x:
        if len(x) > 1:
            return float(x.replace('M', '')) * 1000000
        return 1000000.0
    if 'B' in x:
        return float(x.replace('B', '')) * 1000000000
    return 0.0

tesla['Vol.'] = tesla['Vol.'].apply(value_to_float)
gm['Vol.'] = gm['Vol.'].apply(value_to_float)
toyota['Vol.'] = toyota['Vol.'].apply(value_to_float)

#linear plot of all the stocks' Open price
tesla['Open'].plot(label='Tesla',figsize=(16,8),title='Opening Prices')
gm['Open'].plot(label='GM')
toyota['Open'].plot(label='Toyota')
plt.legend()

#Plot out the MA50 and MA200
toyota['MA50']=gm['Open'].rolling(50).mean()
toyota['MA200']=gm['Open'].rolling(200).mean()
toyota[['Open','MA50','MA200']].plot(figsize=(16,8),title='Toyota Moving Average')

tesla['MA50']=tesla['Open'].rolling(50).mean()
tesla['MA200']=tesla['Open'].rolling(200).mean()
tesla[['Open','MA50','MA200']].plot(figsize=(16,8),title='Tesla Moving Average')

#to see if there is a relationship between these stocks using scatter matrix plot
from pandas.plotting import scatter_matrix
car_comp= pd.concat([tesla['Open'],gm['Open'],toyota['Open']],axis=1)
car_comp.columns=['Tesla Open','GM open','Toyota Open']
car_comp.head()
scatter_matrix(car_comp,figsize=(8,8),alpha=0.2,hist_kwds={'bins':50});

#Daily percent change

tesla['returns']=(tesla['Price']/tesla['Price'].shift(1))-1
gm['returns']=(gm['Price']/gm['Price'].shift(1))-1
toyota['returns']=(toyota['Price']/toyota['Price'].shift(1))-1
tesla['returns'].hist(bins=100,label='Tesla',figsize=(12,10),alpha=0.5)
gm['returns'].hist(bins=100,label='GM',alpha=0.5)
toyota['returns'].hist(bins=100,label='Toyota',alpha=0.5)
plt.legend()

boxdf = pd.concat([tesla['returns'],gm['returns'],toyota['returns']],axis=1)
boxdf.columns = ['Tesla Ret','GM ret','Toyota ret']
scatter_matrix(boxdf,figsize=(12,10),alpha=0.2,hist_kwds={'bins':100});


#cumulative returns

tesla['Cumulative Return']=(1+tesla['returns']).cumprod()
gm['Cumulative Return']=(1+gm['returns']).cumprod()
toyota['Cumulative Return']=(1+toyota['returns']).cumprod()

tesla['Cumulative Return'].plot(label='Tesla',figsize=(16,8),title='Cumulative Return')
gm['Cumulative Return'].plot(label='gm')
toyota['Cumulative Return'].plot(label='toyota')
plt.legend()

plt.show()