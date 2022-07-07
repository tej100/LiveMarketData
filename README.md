## Live Market Data
Class that scalps web content from yahoo finance to scrape real-time information on market price, change, volume, etc. Organized and structured in data frame and CSV file. Updates based on user-input time-interval and can be fed into other libraries to generate technical indicators and ML models or analyze patterns with ease. Works with US Equities, Crpyto Currencies, and Futures
### Important notes
- Input ticker-symbol must be same as appears on yahoo finance
- Time-Interval for streaming data is in minutes and streaming is recommended for shorter time intervals (intraday, or at most, 1440 minutes which is 1 day)
- Class is not accurate on anything shorter than 5-min chart since yahoo finance does not update quick enough for M1 chart
- Python script will run indefinitely while streaming until user turns it off
### Setup
- Make sure you have all the libraries that need to be imported for the LiveMarketData class file. If not, run the following in your terminal:
- `pip3 install time`
- `pip3 install bs4`
- `pip3 install requests`
- `pip3 install pandas`
- `pip3 install datetime`
- Also, for the html parser, you may need to `pip3 install lxml` if there is an error

### How to use
- Open a new file and at the top of the file, type:
- `from LiveMarketData import *` 
- Then, create a class object with the two required parameters, ticker symbol and asset_type; for example: 
- `aapl = CurrentMarket("AAPL", "STOCK")` 
- From here, you can do a couple of things: 
- `aapl.Price()` will give you the current price of the object 
- By the same token, `aapl.Volume()`, `aapl.PreviousClose()`, etc. output similar information.
- `aapl.OHLC(interval='15m')` will return a dataframe with the Open, High, Low, and Close for the previous 15 min candlestick
- The stream method will allow you to get a livestream of selected data based on the input time interval and selected parameters: 
- `aapl.stream(interval=15, show_volume=True)` will display the price (default True) and volume like an M15 chart. 
- `aapl.stream(interval=10, market_hours=True)` will display the price every 10 minutes only during US market hours (9:30 - 4:00)
