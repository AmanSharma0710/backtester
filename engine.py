#Required imports
from multiprocessing import Process, Queue
import numpy as np
import pandas as pd
import datetime as dt
import logging
#TODO:Import strategy class and Utils

class DataStream:
    '''
    Class that stores the data the backtesting is to be done on and return the next datapoint through function next_data
    '''
    def __init__(self, tickers=['AAPL'], start_time=dt.datetime(2011, 1, 1), end_time=dt.datetime.today()):
        self.tickers = tickers
        #Add way to get data from the database and store in a pandas dataframe
        self.index = 0

    def next_data(self, from_time=None):
        #Run a loop to do this for all tickers and return a list of dictionaries with added time and ticker

        #If no from time is provided, return the data at the current index and increment the index
        if (from_time==None):
            self.index += 1
            if(self.data.shape[0]>=self.index):
                return 'END'
            return {'Open':self.data['Open'][self.index-1], 'High':self.data['High'][self.index-1], 'Low':self.data['Low'][self.index-1], 
                        'Close':self.data['Close'][self.index-1], 'Volume':self.data['Volume'][self.index-1]}

        #Otherwise binary search through the data to find the datapoint containing from time and make that the index and return
        else:
            pass

    @classmethod
    def process(cls, queue, data_source=None):
        '''
        Process that adds new datapoints to the queue
        '''
        data_source = cls() if data_source is None else data_source
        while True:
            data = data_source.next_data()
            queue.put(data)
            if data == 'END':
                break

class Interface(object):
    '''
    Class that handles the interaction between the strategy and the data stream
    '''
    def __init__(self, strategy=None):
        self.strategy = BaseStrategy() if strategy is None else strategy
    
    @classmethod
    def backtest(cls, queue, interface = None):
        interface = cls() if interface is None else interface
        try:
            while True:
                if not queue.empty():
                    o = queue.get()

                    if o == 'END':
                        break

                    timestamp = o['timestamp']
                    ticker = o['ticker']
                    open_price = o['Open']
                    high_price = o['High']
                    low_price = o['Low']
                    close_price = o['Close']
                    volume = o['Volume']

                    # Send pricing updates to the strategy and see what it wants to do

                    # Generate Orders

                    # Process orders
                    if len(orders) > 0:
                        # Randomize the order execution
                        #Execute the orders
                        pass

        except Exception as e:
            print(e)


class Backtester(object):
    def __init__(self, strategy, starting_capital=100000):  #need to update this
        self.strategy = strategy
        self.starting_capital = starting_capital
        self.current_capital = starting_capital
        self.positions = dict()
        self.trades = list()
        self._settings = {}
        self._default_settings = {
            'Tickers': ['AAPL'],
            'Start_Time': dt.datetime(2011, 1, 1),
            'End_Time': dt.datetime.today(),
        }
    
    def set_tickers(self, tickers):
        self._settings['Tickers'] = tickers

    def set_start_date(self, date):
        self._settings['Start_Time'] = date

    def set_end_date(self, date):
        self._settings['End_Time'] = date

    def get_setting(self, setting):
        return self._settings[setting] if setting in self._settings else self._default_settings[setting]

    def backtest(self):
        q = Queue()
        ds = DataStream(
            tickers=self.get_setting('Tickers'),
            start_time=self.get_setting('Start_Time'),
            end_time=self.get_setting('End_Time')
        )
        p = Process(target=DataStream.process, args=(q, ds))
        
        
