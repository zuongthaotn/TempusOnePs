from services.base_service import BaseServicePlugin
from core.event_bus import EventName
import pandas_ta as ta


class RsiSignalPlugin(BaseServicePlugin):
    async def setup(self):
        print(f"Signal plugin [{self.name}] initialized and subscribe {EventName.DATA_NEW}")
        self.bus.subscribe(EventName.DATA_NEW, self.find_signal)

    async def find_signal(self, market_data):
        print(f"Finding RSI signal for {market_data['symbol']}")
        df = market_data['df']
        df["RSI_14"] = ta.rsi(df["Close"], length=14)
        last_row = df.iloc[-1]
        signal = {"plugin": self.name, "symbol": market_data["symbol"], "signal": ""}
        # RSI logic
        if last_row["RSI_14"] < 30:
            signal = {"plugin": self.name, "symbol": market_data["symbol"], "signal": "BUY"}
        elif last_row["RSI_14"] > 70:
            signal = {"plugin": self.name, "symbol": market_data["symbol"], "signal": "SELL"}
        await self.bus.publish(EventName.SIGNAL_GENERATED, signal)

