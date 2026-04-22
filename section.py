import pandas as pd
from dataclasses import dataclass

@dataclass
class StockData:
    ticker: str
    ohlc: pd.DataFrame
    options: dict[str, pd.DataFrame]
    info: dict
    financials: pd.DataFrame

class Section:
    ACCURACY = 3
    def __init__(self, name: str):
        self._ACCURACY = 3

        self.name = name
        self._indicators: dict = {}

    def _assertRequiredColumns(self, data: pd.DataFrame, requiredCols: list):
        try:
            columns = data.columns.to_list()
            for col in requiredCols:
                assert col in columns, f"Missing {col} in dataframe"
        except AssertionError as e:
            print(f"Assertion went wrong: {e}")
            return pd.DataFrame()
        
        return data
    
    def _assertRequiredKeysDict(self, data: dict[str, any], requiredKeys: list[str]):
        returnData = {}
        for key in requiredKeys:
            assert key in data, f"Missing required key: '{key}'"
            returnData[key] = data[key]
        
        return returnData
        



    def calculate(self, data: StockData):
        pass

    def getData(self) -> dict:
        return self._indicators