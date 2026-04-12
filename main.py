from fastapi import FastAPI, HTTPException
import yfinance as yf

app = FastAPI()

@app.get("/")
def read_root():
    return {"status": "Bot is awake and running!"}

@app.get("/quote/{ticker}")
def get_quote(ticker: str):
    try:
        # stock = yf.Ticker(ticker)
        # hist = stock.history(period="1d")
        
        # if hist.empty:
        #     raise HTTPException(status_code=404, detail="Ticker not found or no data")

        # Package the exact JSON format n8n wants
        payload = [
                {
                    "asset": "BTC-USD",
                    "asset_class": "crypto",
                    "history": [
                    { "timestamp": "2026-04-12T00:00:00Z", "close": 84100.50, "volume": 1250, "rsi": 60, "sma10": 83000 },
                    { "timestamp": "2026-04-12T01:00:00Z", "close": 84250.00, "volume": 1400, "rsi": 60, "sma10": 83000 },
                    { "timestamp": "2026-04-12T02:00:00Z", "close": 83900.25, "volume": 1850, "rsi": 60, "sma10": 83000 },
                    { "timestamp": "2026-04-12T03:00:00Z", "close": 83750.00, "volume": 2100, "rsi": 60, "sma10": 83000 },
                    { "timestamp": "2026-04-12T04:00:00Z", "close": 83800.00, "volume": 900 , "rsi": 60, "sma10": 83000 },
                    { "timestamp": "2026-04-12T05:00:00Z", "close": 84150.50, "volume": 1100, "rsi": 60, "sma10": 83000 },
                    { "timestamp": "2026-04-12T06:00:00Z", "close": 84400.00, "volume": 1600, "rsi": 60, "sma10": 83000 },
                    { "timestamp": "2026-04-12T07:00:00Z", "close": 84650.75, "volume": 2200, "rsi": 60, "sma10": 83000 },
                    { "timestamp": "2026-04-12T08:00:00Z", "close": 84900.00, "volume": 3100, "rsi": 60, "sma10": 83000 },
                    { "timestamp": "2026-04-12T09:00:00Z", "close": 85100.25, "volume": 3500, "rsi": 60, "sma10": 83000 },
                    { "timestamp": "2026-04-12T10:00:00Z", "close": 84850.00, "volume": 2800, "rsi": 60, "sma10": 83000 },
                    { "timestamp": "2026-04-12T11:00:00Z", "close": 84700.50, "volume": 1900, "rsi": 60, "sma10": 83000 },
                    { "timestamp": "2026-04-12T12:00:00Z", "close": 84750.00, "volume": 1500, "rsi": 60, "sma10": 83000 },
                    { "timestamp": "2026-04-12T13:00:00Z", "close": 84950.25, "volume": 1750, "rsi": 60, "sma10": 83000 },
                    { "timestamp": "2026-04-12T14:00:00Z", "close": 85300.00, "volume": 4200, "rsi": 60, "sma10": 83000 },
                    { "timestamp": "2026-04-12T15:00:00Z", "close": 85600.50, "volume": 5100, "rsi": 60, "sma10": 83000 },
                    { "timestamp": "2026-04-12T16:00:00Z", "close": 85450.00, "volume": 3900, "rsi": 60, "sma10": 83000 },
                    { "timestamp": "2026-04-12T17:00:00Z", "close": 85200.75, "volume": 2600, "rsi": 60, "sma10": 83000 },
                    { "timestamp": "2026-04-12T18:00:00Z", "close": 85350.00, "volume": 2100, "rsi": 60, "sma10": 83000 },
                    { "timestamp": "2026-04-12T19:00:00Z", "close": 85500.25, "volume": 1800, "rsi": 60, "sma10": 83000 },
                    { "timestamp": "2026-04-12T20:00:00Z", "close": 85750.00, "volume": 3300, "rsi": 60, "sma10": 83000 },
                    { "timestamp": "2026-04-12T21:00:00Z", "close": 86000.50, "volume": 4800, "rsi": 60, "sma10": 83000 },
                    { "timestamp": "2026-04-12T22:00:00Z", "close": 85850.00, "volume": 2900, "rsi": 60, "sma10": 83000 },
                    { "timestamp": "2026-04-12T23:00:00Z", "close": 85900.25, "volume": 1450, "rsi": 60, "sma10": 83000 }
                    ]
                }
            ];

        return payload

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))