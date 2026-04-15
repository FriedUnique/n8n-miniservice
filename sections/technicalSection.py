from section import Section, StockData
from helper import percent
import pandas as pd
from talib import SMA, ROC, ATR, BBANDS

class Technicals(Section):
    def __init__(self, name: str):
        super().__init__(name)

    def calculate(self, data: StockData):
        priceData = self._assertRequiredColumns(data.ohlc, ["Volume", "Close", "High", "Low"])
        self._indicators = {}

        # can not calculate anything
        if priceData.empty:
            print("hey")
            return
        
        self._VWAP(priceData)
        self._RVOL(priceData)

        # To calculate position sizing. 
        # If the ATR is high, the position size must be reduced to keep the total portfolio Value at Risk (VaR) stable.
        atr = ATR(priceData["High"],priceData["Low"],priceData["Close"])
        self._indicators["average_true_range_atr"] = round(atr.iloc[-1], self._ACCURACY)

        self._DistanceFrom(priceData["Close"], SMA(priceData["Close"], 30), "price_vs_sma30_pct")
        self._BBAND_width(priceData)
        self._CMF(priceData)

        
    def _VWAP(self, data: pd.DataFrame):
        vol = data["Volume"]
        price = data["Close"]

        vwap = sum(vol.copy()*price.copy())/sum(vol)
        self._indicators["VWAP"] = round(vwap, self._ACCURACY)
        self._indicators["VWAP_vs_price_pct"] = percent((price.iloc[-1]*100/vwap))

    def _RVOL(self, data: pd.DataFrame):
        vol = data["Volume"]
        volSMA = SMA(vol, 30)

        self._indicators["relative_volume_rvol_pct"] = percent((vol*100/volSMA).iloc[-1])

    def _DistanceFrom(self, seriesUp: pd.Series, seriesDown: pd.Series, name: str, days = 1):
        distancePct = sum(seriesUp.tail(days)/seriesDown.tail(days))/days

        self._indicators[name] = percent(distancePct*100) 

    def _BBAND_width(self, data: pd.DataFrame):
        upper, middle, lower = BBANDS(data["Close"], 20, 2)
        bandwidth = ((upper-lower)/middle)

        self._indicators["bbands_bandwidth"] = round(bandwidth.iloc[-1], self._ACCURACY)
        self._indicators["bbands_bandwidth_trend_pct"] = bandwidth.iloc[-1]/SMA(bandwidth).iloc[-1]

    def _MFM(self, data: pd.DataFrame) -> pd.DataFrame:
        mfm = (2*data["Close"]-data["Low"]-data["High"])/(data["High"]-data["Low"])
        mfm = mfm * data["Volume"]

        return mfm
    
    def _CMF(self, data: pd.DataFrame):
        cmf = round(sum(self._MFM(data))/sum(data["Volume"]), self._ACCURACY)
        self._indicators["chaikin_money_flow"] = round(cmf, self._ACCURACY)

