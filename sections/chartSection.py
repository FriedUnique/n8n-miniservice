from section import Section, StockData
import pandas as pd
from talib import RSI, MACD, BBANDS
import io
import base64

import matplotlib
matplotlib.use('Agg') # not ineractive backend
import matplotlib.pyplot as plt

class Chart(Section):
    def __init__(self, name: str):
        super().__init__(name)

    def calculate(self, data: StockData):
        priceData = self._assertRequiredColumns(data.ohlc, ["Volume", "Close", "High", "Low"])
        self._indicators = {}

        if priceData.empty:
            return

        close = priceData['Close']

        # --- 1. Calculate Indicators ---
        # Bollinger Bands
        upper, middle, lower = BBANDS(close, timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)
        
        # RSI
        rsi = RSI(close, timeperiod=14)
        
        # MACD
        macd, macdsignal, macdhist = MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)

        # --- 2. Create a Vision-Friendly Multi-Pane Chart ---
        # We use a constrained layout so the LLM doesn't get confused by overlapping text
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 12), gridspec_kw={'height_ratios': [3, 1, 1]})
        fig.tight_layout(pad=4.0)

        # Top Pane: Price & Bollinger Bands
        ax1.plot(priceData.index, close, label='Close Price', color='black', linewidth=1.5)
        ax1.plot(priceData.index, upper, label='Upper BB', color='red', linestyle='--', alpha=0.6)
        ax1.plot(priceData.index, lower, label='Lower BB', color='green', linestyle='--', alpha=0.6)
        ax1.fill_between(priceData.index, lower, upper, color='gray', alpha=0.1)
        ax1.set_title("Price Action & Volatility (Bollinger Bands)")
        ax1.legend(loc='upper left')
        ax1.grid(True, alpha=0.3)

        # Middle Pane: RSI
        ax2.plot(priceData.index, rsi, color='purple', label='RSI (14)')
        ax2.axhline(70, color='red', linestyle='--', alpha=0.5) # Overbought line
        ax2.axhline(30, color='green', linestyle='--', alpha=0.5) # Oversold line
        ax2.fill_between(priceData.index, rsi, 70, where=(rsi >= 70), facecolor='red', alpha=0.3)
        ax2.fill_between(priceData.index, rsi, 30, where=(rsi <= 30), facecolor='green', alpha=0.3)
        ax2.set_title("Momentum (RSI)")
        ax2.set_ylim(0, 100)
        ax2.legend(loc='upper left')
        ax2.grid(True, alpha=0.3)

        # Bottom Pane: MACD
        ax3.plot(priceData.index, macd, label='MACD', color='blue')
        ax3.plot(priceData.index, macdsignal, label='Signal', color='orange')
        ax3.bar(priceData.index, macdhist, label='Histogram', color=['green' if val > 0 else 'red' for val in macdhist], alpha=0.5)
        ax3.set_title("Trend & Divergence (MACD)")
        ax3.legend(loc='upper left')
        ax3.grid(True, alpha=0.3)

        # --- 3. Save and Encode ---
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        buf.seek(0)
        
        img_str = base64.b64encode(buf.read()).decode('utf-8')
        plt.close(fig)

        self._indicators["chart"] = img_str