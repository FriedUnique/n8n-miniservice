from fastapi import FastAPI, HTTPException
import requests
import time
import pandas as pd
import yfinance as yf

from responceGenerator import ResponceGenerator
from sections.technicalSection import Technicals
from sections.alternativeSection import Alternative
from sections.generalSection import General
from sections.macroSection import Macro
from section import StockData

app = FastAPI(title="Hyperliquid Analysis API")

@app.get("/")
def read_root():
    return {"status": "Bot is awake and running!"}

def get_hyperliquid_candles(coin, interval, months=3):
    url = "https://api.hyperliquid.xyz/info"
    
    end_time = int(time.time() * 1000)
    start_time = end_time - (months * 30 * 24 * 60 * 60 * 1000)
    
    payload = {
        "type": "candleSnapshot",
        "req": {
            "coin": coin,
            "interval": interval,
            "startTime": start_time,
            "endTime": end_time
        }
    }
    
    response = requests.post(url, json=payload)
    
    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data)
        df['datetime'] = pd.to_datetime(df['t'], unit='ms')
        df = df[['datetime', 'o', 'h', 'l', 'c', 'v']].rename(columns={
            'o': 'Open', 'h': 'High', 'l': 'Low', 'c': 'Close', 'v': 'Volume'
        })
        return df[['Open', 'High', "Low", "Close", "Volume"]].astype(float)
    else:
        return None

@app.get("/quote/{ticker}")
def get_quote(ticker: str):
    data = get_hyperliquid_candles(ticker, "4h", months=3)
    
    if data is None or data.empty:
        raise HTTPException(status_code=404, detail=f"No data found for ticker '{ticker}' on Hyperliquid.")

    ticker_yf = yf.Ticker(ticker.replace("cash:", ""))
    asset_context = ticker_yf.info

    dataContainer = StockData(data, {"Calls": pd.DataFrame(), "Puts": pd.DataFrame()}, asset_context, pd.DataFrame())

    rg = ResponceGenerator()
    general = General("asset_context")
    tech = Technicals("technicals")
    alt = Alternative("alternative")
    macro = Macro("macro_context")

    rg.addSection(general)
    rg.addSection(tech)
    rg.addSection(macro)

    rg.calculate(dataContainer)

    return rg.produceJson()