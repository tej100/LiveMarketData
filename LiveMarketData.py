import time
from bs4 import BeautifulSoup
import requests
import pandas as pd
import datetime as dt


# Grabs content from specific path on yahoo finance and parses data
def web_content_div(web_content, class_path, value):
    web_content_div = web_content.find_all('div', {'class': class_path})
    try:
        if value != 'None':
            spans = web_content_div[0].find_all(value)
            texts = [span.get_text() for span in spans]
        else:
            texts = web_content_div[0].get_text('|', strip=True)
            texts = texts.split("|")
    except IndexError:
        texts = ''
    return texts


class CurrentMarket:
    def __init__(self, ticker, asset_type):
        """
        Given an input ticker symbol, scrapes real-time html data
        from yahoo finance and outputs the selected variables
        :param str ticker: ticker symbol of input asset
        :param str asset_type: type of asset, accepts "STOCK", "CRPYTO", "FUTURE"
        """
        self.ticker = ticker.upper()
        self.asset_type = asset_type
        self.Error = 0
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0'}
        self.url_summary = "https://finance.yahoo.com/quote/" + self.ticker + "?p=" + self.ticker + "&.tsrc=fin-srch"
        self.web_content = BeautifulSoup(requests.get(self.url_summary, headers=self.headers).text, 'lxml')
        self.url_chart = f'https://query1.finance.yahoo.com/v8/finance/chart/{self.ticker}?symbol={self.ticker}'

    def Price(self):
        """
        Outputs current price
        """
        try:
            texts = web_content_div(self.web_content, "D(ib) Mend(20px)", "fin-streamer")

            if texts:
                price = float(texts[0]
                              .replace(',', '')
                              .replace("(", "")
                              .replace(")", "")
                              .replace("%", ""))
            else:
                price = ''

        except ConnectionError:
            price = ''
            self.Error = 1
            print('Connection Error')

        return price

    def Change(self):
        """
        Outputs current change in price from previous price
        """
        try:
            texts = web_content_div(self.web_content, "D(ib) Mend(20px)", "fin-streamer")
            if texts:
                change = float(texts[1]
                               .replace(',', '')
                               .replace("(", "")
                               .replace(")", "")
                               .replace("%", ""))
            else:
                change = ''

        except ConnectionError:
            change = ''
            self.Error = 1
            print('Connection Error')

        return change

    def OHLC(self, interval) -> pd.DataFrame:
        """
        Outputs current OHLC data
        :param str interval: Ex: '15m', the time-period candlestick do you want OHLC data from
        """
        params = {
            'range': interval,
            'interval': interval,
            'includePrePost': 'true',
            'events': 'div|split|earn'
        }
        OHLC_content = requests.get(self.url_chart, params=params, headers=self.headers).json()

        df = pd.DataFrame(data=[],
                          columns=['Open', 'High', 'Low', 'Close'],
                          index=pd.to_datetime([]))
        df['Datetime'] = pd.to_datetime(OHLC_content['chart']['result'][0]['timestamp'], unit='s')
        df.set_index('Datetime', inplace=True)
        df.index.name = None

        df['Open'] = OHLC_content['chart']['result'][0]['indicators']['quote'][0]['open']
        df['High'] = OHLC_content['chart']['result'][0]['indicators']['quote'][0]['high']
        df['Low'] = OHLC_content['chart']['result'][0]['indicators']['quote'][0]['low']
        df['Close'] = OHLC_content['chart']['result'][0]['indicators']['quote'][0]['close']
        df = round(df, 2)
        return df[-2:-1]

    def Volume(self):
        """
        Outputs current trading volume
        """
        try:
            if self.asset_type == "CRYPTO" or self.asset_type == "FUTURE":
                texts = web_content_div(self.web_content,
                                        "D(ib) W(1/2) Bxz(bb) Pstart(12px) Va(t) ie-7_D(i) ie-7_Pos(a) smartphone_D(b) smartphone_W(100%) smartphone_Pstart(0px) smartphone_BdB smartphone_Bdc($seperatorColor)",
                                        "fin-streamer")
            else:
                texts = web_content_div(self.web_content,
                                        "D(ib) W(1/2) Bxz(bb) Pend(12px) Va(t) ie-7_D(i) smartphone_D(b) smartphone_W(100%) smartphone_Pend(0px) smartphone_BdY smartphone_Bdc($seperatorColor)",
                                        "fin-streamer")

            if texts:
                volume = int(texts[0]
                             .replace(',', '')
                             .replace("(", "")
                             .replace(")", "")
                             .replace("%", ""))
            else:
                volume = ''

        except ConnectionError:
            volume = ''
            self.Error = 1
            print('Connection Error')

        return volume

    def PreviousClose(self):
        """
        Outputs previous close
        """
        try:
            if self.asset_type == "FUTURE":
                texts = ''
            else:
                texts = web_content_div(self.web_content,
                                        'D(ib) W(1/2) Bxz(bb) Pend(12px) Va(t) ie-7_D(i) smartphone_D(b) smartphone_W(100%) smartphone_Pend(0px) smartphone_BdY smartphone_Bdc($seperatorColor)',
                                        'None')
            if texts:
                previous_close = float(texts[1]
                                       .replace(',', '')
                                       .replace("(", "")
                                       .replace(")", "")
                                       .replace("%", ""))
            else:
                previous_close = ''

        except ConnectionError:
            previous_close = ''
            self.Error = 1
            print('Connection Error')

        return previous_close

    def OneYearTarget(self):
        """
        Outputs the current estimate for the one-year target price
        """
        try:
            if self.asset_type == "STOCK":
                texts = web_content_div(self.web_content,
                                        'D(ib) W(1/2) Bxz(bb) Pstart(12px) Va(t) ie-7_D(i) ie-7_Pos(a) smartphone_D(b) smartphone_W(100%) smartphone_Pstart(0px) smartphone_BdB smartphone_Bdc($seperatorColor)',
                                        'None')
            else:
                texts = ""
            if texts:
                one_year_target = float(texts[-1]
                                        .replace(',', '')
                                        .replace("(", "")
                                        .replace(")", "")
                                        .replace("%", ""))
            else:
                one_year_target = ''

        except ConnectionError:
            one_year_target = ''
            self.Error = 1
            print('Connection Error')

        return one_year_target

    def Stream(self, interval, *, market_hours=False, show_price=True, show_OHLC=False, show_change=False,
               show_volume=False, show_previous_close=False, show_one_year_target=False, folder=''):
        """
        Prints real time data on an N-minute chart and stores in a csv file for asset
        Set show_one_year_target to false if checking crpytos or futures
        :param int interval: Indicate time interval (in minutes) for which you want the data to stream
        :param bool market_hours: Default False, indicate True if you would like to stream only during market hours
        :param bool show_price: Default True, indicate False if you do not want market price
        :param bool show_OHLC: Indicate True to generate Open, High, Low, Close data for the previous period
        :param bool show_change: Indicate True if you want to get the current change
        :param bool show_volume: Indicate True if you want to get the trading volume
        :param bool show_previous_close: Indicate True if you want to get the previous close
        :param bool show_one_year_target: Indicate True if you want to show the one-year target estimate
        :param str folder: Indicate specific path to store Stream CSV data (by default stores in same folder as LiveMarketData.py)
        (Not fully supported for Cryptos and Futures)
        """
        # Initialize dataframe to store market data
        current_data = pd.DataFrame(data=[], columns=[], index=pd.to_datetime([]))
        if show_price:
            current_data['Price'] = pd.Series(dtype='float')
        if show_OHLC:
            current_data['Open'] = pd.Series(dtype='float')
            current_data['High'] = pd.Series(dtype='float')
            current_data['Low'] = pd.Series(dtype='float')
            current_data['Close'] = pd.Series(dtype='float')
        if show_change:
            current_data['Change'] = pd.Series(dtype='float')
        if show_volume:
            current_data['Volume'] = pd.Series(dtype='int')
        if show_previous_close:
            current_data['PreviousClose'] = pd.Series(dtype='float')
        if show_one_year_target:
            current_data['OneYearTarget'] = pd.Series(dtype='float')

        # Set up initial CSV file path to append all data

        path = folder + self.ticker + '_stock_data.csv'
        current_data.to_csv(path, mode='a', header=True)

        # Initialize hours of operation for stream
        if market_hours:
            market_open = '0930'
            market_close = '1600'
        else:
            market_open = '0000'
            market_close = '2359'

        # Begin stream loop
        while True:
            currentDT = dt.datetime.now()
            time_stamp = currentDT.strftime("%Y-%m-%d %H:%M:%S")
            now = currentDT.strftime("%H%M")

            if currentDT.minute % interval == 0 and currentDT.second == 0 and market_open <= now <= market_close:
                data_now = pd.Series([], [], dtype='float64')
                if show_price:
                    data_now['Price'] = self.Price()
                if show_OHLC:
                    data_now['Open'] = self.OHLC(str(interval)+'m')['Open']
                    data_now['High'] = self.OHLC(str(interval)+'m')['High']
                    data_now['Low'] = self.OHLC(str(interval)+'m')['Low']
                    data_now['Close'] = self.OHLC(str(interval)+'m')['Close']
                if show_change:
                    data_now['Change'] = self.Change()
                if show_volume:
                    data_now['Volume'] = self.Volume()
                if show_previous_close:
                    data_now['PrevClose'] = self.PreviousClose()
                if show_one_year_target:
                    data_now['OneYearTarg'] = self.OneYearTarget()
                current_data.loc[time_stamp] = data_now

                # If there is an error or network connection while scalping the data, break program
                if self.Error != 0:
                    break

                # Display data and add to CSV file
                print(current_data.tail(1))
                current_data.tail(1).to_csv(path, mode='a', header=False)

                time.sleep(5)
