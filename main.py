import yfinance as yf
import pandas as pd

from responceGenerator import ResponceGenerator
from sections.technicalSection import Technicals
from sections.alternativeSection import Alternative
from sections.generalSection import General
from sections.macroSection import Macro
from section import StockData

def read_root():
    return {"status": "Bot is awake and running!"}

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
        return {"Error": str(e)}
    

    
import requests

url = "https://gwmbot.app.n8n.cloud/webhook-test/079724dc-004c-4453-a152-01a61acd2f81"

universe = ["AAPL", "NVDA"]

for ticker in universe:
    requests.post(url, json=get_quote(ticker))
