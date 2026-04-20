import pandas as pd
from section import Section, StockData
import numpy as np

class Alternative(Section): # Inherit your (Section) here
    def __init__(self, name: str = "fundamentals_valuation"):
        super().__init__(name)

    def calculate(self, data: StockData):
        infoData = self._assertRequiredKeysDict(data.info, ["shortPercentOfFloat", "beta", "floatShares", "sharesOutstanding"])
        self._indicators = {}

        self._marketStructre(infoData)
        


    def _PutCallRatio(self, data:pd.DataFrame):
        total_put_vol = data['Puts']["volume"].fillna(0).sum()
        total_call_vol = data['Calls']["volume"].fillna(0).sum()
        
        # Calculate ratio, protecting against division by zero
        if total_call_vol > 0:
            self._indicators['put_call_ratio_vol'] = round(total_put_vol / total_call_vol, self._ACCURACY)
        else:
            self._indicators['put_call_ratio_vol'] = np.nan

    def _marketStructre(self, infoData):
        self._indicators['short_percent_of_float'] = round(infoData.get('shortPercentOfFloat', np.nan), self._ACCURACY)
        self._indicators['beta'] = round(infoData.get('beta', np.nan), self._ACCURACY)
        self._indicators['float_shares'] = round(infoData.get('floatShares', np.nan), self._ACCURACY)
        self._indicators['shares_outstanding'] = round(infoData.get('sharesOutstanding', np.nan), self._ACCURACY)


