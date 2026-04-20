from section import Section, StockData
import pandas as pd
from helper import percent
from talib import SMA, EMA

class General(Section):
    def __init__(self, name: str):
        super().__init__(name)

    def calculate(self, data: StockData):
        priceData = self._assertRequiredColumns(data.ohlc, ["Volume", "Close", "High", "Low"])
        self._indicators = {}

        # can not calculate anything
        if priceData.empty:
            print("hey")
            return
        
        sma20 = SMA(priceData["Close"], 20).iloc[-1]
        ema21 = EMA(priceData["Close"], 21).iloc[-1]
        ema55 = EMA(priceData["Close"], 55).iloc[-1]
        
        print(type(priceData["Close"].iloc[-1]))


        self._indicators = {
            "price": round(priceData["Close"].iloc[-1], self._ACCURACY),
            "SMA-20": round(sma20,self._ACCURACY),
            "EMA-21": round(ema21, self.ACCURACY),
            "EMA-55": round(ema55, self.ACCURACY),
            "1_week_return_pct": round((priceData["Close"].iloc[-1]*100/priceData["Close"].iloc[(-13)*5])-100,self._ACCURACY)
        }
        

    
    
