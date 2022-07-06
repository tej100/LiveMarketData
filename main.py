from LiveMarketData import *

# Initialize CurrentMarket objects

aapl_live = CurrentMarket("AAPL", "STOCK")
ethusd_live = CurrentMarket("eth-usd", "CRPYTO")

# Print current data for objects

print(
  aapl_live.ticker, aapl_live.asset_type,
  f"\nprice: {aapl_live.Price()}"
  f"\nchange: {aapl_live.Change()}"
  f"\nvolume: {aapl_live.Volume()}"
  f"\nprevious close: {aapl_live.PreviousClose()}"
  f"\none-year target: {aapl_live.OneYearTarget()}"
)

print(
  ethusd_live.ticker, ethusd_live.asset_type,
  f"\nprice: {ethusd_live.Price()}"
  f"\nchange: {ethusd_live.Change()}"
  f"\nvolume: {ethusd_live.Volume()}"
  f"\nprevious close: {ethusd_live.PreviousClose()}"
  f"\none-year target: {ethusd_live.OneYearTarget()}"  # Cryptos do not have one-year targets
)

# Start streaming data for objects

aapl_live.Stream(interval=60, market_hours=True, show_change=True, show_one_year_target=True, folder="LiveDataCSV")
# This object will stream data for AAPL's market price (default True), change in price, and one-year-target estimate, every hour only during market hours
# and store the stream data in the folder "LiveDataCSV" (this is also the name of the default folder)

# Warning: Only 1 object can be streamed at once. Stream the following object in a different script if you want to run simultaneous streams
ethusd_live.Stream(interval=15, show_volume=True, show_previous_close=True, folder="LiveDataCSV")
# This object will stream data for BTC-USD's market price (default True), trading volume, and previous close, every 15 minutes during all hours (default)
# and store the stream data in the folder "LiveDataCSV" (this is also the name of the default folder)
