from section import Section, StockData
import pandas as pd
from helper import percent
from talib import SMA

class General(Section):
    def __init__(self, name: str):
        super().__init__(name)

    def calculate(self, data: StockData):
        priceData = self._assertRequiredColumns(data.ohlc, ["Volume", "Close", "High", "Low"])
        info = self._assertRequiredKeysDict(data.info, ["symbol", "sector"])
        self._indicators = {}

        # can not calculate anything
        if priceData.empty:
            print("hey")
            return
        
        sma20 = SMA(priceData["Close"], 20).iloc[-1]
        
        self._indicators = {
            "ticker": info.get("symbol", "na."),
            "sector": info.get("sector", "na."),
            "price": round(priceData["Close"].iloc[-1], self._ACCURACY),
            "SMA-20": round(sma20,self._ACCURACY),
            "1_week_return_pct": round((priceData["Close"].iloc[-1]*100/priceData["Close"].iloc[(-13)*5])-100,self._ACCURACY)
        }
        

    
    
