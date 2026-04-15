from section import Section, StockData
from helper import percent
import pandas as pd



class Macro(Section):
    def __init__(self, name: str):
        super().__init__(name)

    def calculate(self, data: StockData):
        priceData = self._assertRequiredColumns(data.ohlc, ["Volume", "Close", "High", "Low"])
        info = self._assertRequiredKeysDict(data.info, [])
        self._indicators = {}

        # can not calculate anything
        if priceData.empty:
            print("hey")
            return
        

    def _ATR(self, data):
        pass

    def _impliedVolatility(self):
        pass


    
    
