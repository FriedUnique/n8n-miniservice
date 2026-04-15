from talib import SMA, RSI, MACD, BBANDS, ATR, EMA
import pandas as pd

def addTechnicalPreprocess(historyData: pd.DataFrame):
    historyData = historyData.copy()

    historyData["SMA-5"] = SMA(historyData["Close"], 5)
    historyData["SMA-20"] = SMA(historyData["Close"], 20)

    historyData["RSI"] = RSI(historyData["Close"])
    
    historyData["MACD"], historyData["MACD_signal"], historyData["MACD_hist"] = MACD(historyData["Close"])
    historyData["BB_upper"], historyData["BB_middle"], historyData["BB_lower"] = BBANDS(historyData["Close"])
    historyData["ATR"] = ATR(historyData["High"], historyData["Low"], historyData["Close"])
    
    return historyData


def putItIntoWords(data: pd.DataFrame):
    try:
        columns = data.columns.to_list()
        required_cols = ["RSI", "SMA-5", "SMA-20", "MACD_hist", "BB_upper", "BB_lower", "ATR"]
        for col in required_cols:
            assert col in columns, f"Missing {col} in dataframe"
    except AssertionError as e:
        print(f"Assertion went wrong: {e}")
        return {}
    
    latest = data.iloc[-1]

    parsedData = {
        "current_price": round(latest["Close"], 2),
        "price_above_SMA-20": bool(latest["Close"] > latest["SMA-20"]),
        "price_above_SMA-5": bool(latest["Close"] > latest["SMA-5"]),
        "sma_crossover_status": calculateCrossover(data),
        "rsi_state": getRSIState(latest["RSI"]),
        "macd_momentum": "bullish_expansion" if latest["MACD_hist"] > 0 else "bearish_contraction",
        "bbands_state": getBBandsState(latest["Close"], latest["BB_upper"], latest["BB_lower"]),
        "daily_volatility_atr": round(latest["ATR"], 2) if not pd.isna(latest["ATR"]) else None
    }

    return parsedData

def calculateCrossover(series1: pd.Series, series2: pd.Series):
    if series1.iloc[-2] <= series2.iloc[-2] and series1.iloc[-1] > series2.iloc[-1]:
        return "bullish_crossover"
    elif series1.iloc[-2] >= series2.iloc[-2] and series1.iloc[-1] < series2.iloc[-1]:
        return "bearish_crossover"
    
    return "none"


def calculateCrossover(data: pd.DataFrame) -> str:
    prev_fast = data["SMA-5"].iloc[-2]
    prev_slow = data["SMA-20"].iloc[-2]
    curr_fast = data["SMA-5"].iloc[-1]
    curr_slow = data["SMA-20"].iloc[-1]

    if prev_fast <= prev_slow and curr_fast > curr_slow:
        return "bullish_crossover"
    elif prev_fast >= prev_slow and curr_fast < curr_slow:
        return "bearish_crossover"
    
    return "none"


def getRSIState(rsi_val: float) -> str:
    if pd.isna(rsi_val):
        return "unknown"
    if rsi_val >= 70:
        return "overbought"
    elif rsi_val <= 30:
        return "oversold"
    
    return "normal"


def getBBandsState(price: float, upper: float, lower: float) -> str:
    if price > upper:
        return "breaking_upper_band"
    elif price < lower:
        return "breaking_lower_band"
    return "within_bands"