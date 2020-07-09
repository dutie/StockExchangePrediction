
# Main Packages
from pandas_datareader import data
import matplotlib.pyplot as plt
import pandas as pd

# Setting up the project

# Getting to know the tools
# Define the instruments to download. We would like to see Apple, Microsoft and the S&P500 index.
tickers = ['KO', 'T', 'WFC','KHC','BMY','NOK','BMW.DE','PROX.BR']

# We would like all available data from 01/01/2000 until 12/31/2016.
start_date = '2015-01-01'
end_date = '2020-08-05'

# User pandas_reader.data.DataReader to load the desired data. As simple as that.

df = pd.concat([data.DataReader(ticker,'yahoo', start_date, end_date) for ticker in tickers]).reset_index()

print(df.head(9))

# Getting just the adjusted closing prices. This will return a Pandas DataFrame
# The index in this DataFrame is the major index of the df.
close = df['Close']

# Getting all weekdays between 01/01/2000 and 12/31/2016
all_weekdays = pd.date_range(start=start_date, end=end_date, freq='B')

# How do we align the existing prices in adj_close with our new set of dates?
# All we need to do is reindex close using all_weekdays as the new index
close = close.reindex(all_weekdays)

# Reindexing will insert missing values (NaN) for the dates that were not present
# in the original set. To cope with this, we can fill the missing by replacing them
# with the latest available price for each instrument.
close = close.fillna(method='ffill')

print(all_weekdays)

close.head(10)

close.describe()


# Get the MSFT timeseries. This now returns a Pandas Series object indexed by date.
msft = close[['Close','type']]
msft.index = close.Date
print(msft.head(10))
msft = msft[msft['type']=='KO'].Close
print(msft.head(10))
short_rolling_msft = msft.rolling(window=20).mean()
long_rolling_msft = msft.rolling(window=100).mean()

# Plot everything by leveraging the very powerful matplotlib package
fig, ax = plt.subplots(figsize=(16,9))

ax.plot(msft.index, msft, label='KO')
ax.plot(short_rolling_msft.index, short_rolling_msft, label='20 days rolling')
ax.plot(long_rolling_msft.index, long_rolling_msft, label='100 days rolling')

ax.set_xlabel('Date')
ax.set_ylabel('Adjusted closing price ($)')
ax.legend()

for ticker in tickers:
  df= close[close['type']==ticker]
  df.plot(x="Date", y="Close")