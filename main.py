from fastapi import FastAPI, HTTPException
import yfinance as yf
import pandas as pd

from responceGenerator import ResponceGenerator
from sections.technicalSection import Technicals
from sections.alternativeSection import Alternative
from sections.generalSection import General
from sections.macroSection import Macro
from section import StockData


app = FastAPI()

@app.get("/")
def read_root():
    return {"status": "Bot is awake and running!"}

@app.get("/quote/{ticker}")
def get_quote(ticker: str):
    try:
        stock = yf.Ticker(ticker)
        data = stock.history(interval="1h", period="1mo")
        opt = stock.option_chain(stock.options[0])

        dataContainer = StockData(data, {"Calls": opt.calls, "Puts": opt.puts}, stock.info, stock.financials)

        rg = ResponceGenerator()
        general = General("asset_context")
        tech = Technicals("techincals")
        alt = Alternative("alternative")
        macro = Macro("macro_context")

        rg.addSection(general)
        rg.addSection(tech)
        rg.addSection(alt)
        rg.addSection(macro)

        rg.calculate(dataContainer)

        return rg.produceJson()

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@app.get("/test")
def test():
        return {
        "EXAMPLE": "NOT REAL",
        "asset_context": {
            "ticker": "AAPL",
            "sector": "Technology",
            "price": 270.185,
            "SMA-20": 267.987,
            "1_week_return_pct": 4.894
        },
        "techincals": {
            "VWAP": 255.045,
            "VWAP_vs_price_pct": "5.936 %",
            "relative_volume_rvol_pct": "61.069 %",
            "average_true_range_atr": 1.223,
            "price_vs_sma30_pct": "1.34 %",
            "bbands_bandwidth": 0.049,
            "bbands_bandwidth_trend_pct": 1.2618551454414242,
            "chaikin_money_flow": 0.0
        },
        "alternative": {
            "put_call_ratio_vol": 0.39,
            "short_percent_of_float": 0.009,
            "beta": 1.109,
            "float_shares": 14656035251,
            "shares_outstanding": 14681140000
        },
        "macro_context": {}
    }
    
@app.get("/headlines/{ticker}")
def get_news(ticker: str):
    try:
        return {"status": "Not yet implemented"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# print(json.dumps([item["content"]["summary"] for item in get_news("AAPL")], indent=4))