from fastapi import FastAPI, HTTPException
import requests
import time
import pandas as pd
import uvicorn

# Your existing custom imports
from responceGenerator import ResponceGenerator
from sections.technicalSection import Technicals
from sections.alternativeSection import Alternative
from sections.generalSection import General
from sections.macroSection import Macro
from section import StockData

# Initialize the FastAPI app
app = FastAPI(title="Hyperliquid Analysis API")

@app.get("/")
def read_root():
    return {"status": "Bot is awake and running!"}

def get_hyperliquid_candles(coin, interval, months=3):
    url = "https://api.hyperliquid.xyz/info"
    
    # Calculate timestamps in milliseconds
    end_time = int(time.time() * 1000)
    start_time = end_time - (months * 30 * 24 * 60 * 60 * 1000)
    
# userRateLimit

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
        # Columns: T=CloseTime, c=Close, h=High, i=Interval, l=Low, n=NumTrades, o=Open, s=Symbol, t=StartTime, v=Volume
        df = pd.DataFrame(data)
        df['datetime'] = pd.to_datetime(df['t'], unit='ms')
        df = df[['datetime', 'o', 'h', 'l', 'c', 'v']].rename(columns={
            'o': 'Open', 'h': 'High', 'l': 'Low', 'c': 'Close', 'v': 'Volume'
        })
        return df[['Open', 'High', "Low", "Close", "Volume"]].astype(float)
    else:
        print(f"Error: {response.status_code}")
        return None

@app.get("/quote/{ticker}")
def get_quote(ticker: str):
    # 1. Fetch 1 month (30 days) of 1h interval data from Hyperliquid
    data = get_hyperliquid_candles("cash:TSLA", "4h", months=3)

    print(data["Close"])
    
    if data.empty:
        raise HTTPException(status_code=404, detail=f"No data found for ticker '{ticker}' on Hyperliquid.")

    # 2. Fetch current asset context (replaces yfinance 'info')

    # 4. Instantiate your container
    dataContainer = StockData(data, {"Calls": pd.DataFrame(), "Puts": pd.DataFrame()}, {}, pd.DataFrame())

    # 5. Run your custom analysis sections
    rg = ResponceGenerator()
    general = General("asset_context")
    tech = Technicals("techincals")
    alt = Alternative("alternative")
    macro = Macro("macro_context")

    rg.addSection(general)
    rg.addSection(tech)
    # rg.addSection(alt)
    rg.addSection(macro)

    rg.calculate(dataContainer)

    return rg.produceJson()

# Run the server using uvicorn if executed directly
if __name__ == "__main__":
    print(get_quote("cash:TSLA"))
    # uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)