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
    
@app.get("/headlines/{ticker}")
def get_news(ticker: str):
    try:
        return {"status": "Not yet implemented"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# print(json.dumps([item["content"]["summary"] for item in get_news("AAPL")], indent=4))