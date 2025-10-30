from services.base_service import BaseServicePlugin
from core.event_bus import EventName
import pandas_ta as ta


class RsiSignalPlugin(BaseServicePlugin):
    async def setup(self):
        await self.bus.publish(EventName.LOG_ADD,
                               f"Signal plugin [{self.name}] initialized and subscribe {EventName.DATA_NEW}")
        self.bus.subscribe(EventName.DATA_NEW, self.find_signal)

    async def find_signal(self, market_data):
        # await self.bus.publish(EventName.LOG_ADD, f"[{self.name}] Finding RSI signal for {market_data['symbol']}")
        df = market_data['df']
        df["RSI_14"] = ta.rsi(df["Close"], length=14)
        last_row = df.iloc[-1]
        signal = {"service_name": self.name, "event_name": EventName.SIGNAL_GENERATED,
                  "symbol": market_data["symbol"], "signal": None}
        # RSI logic
        if last_row["RSI_14"] < 30:
            signal["signal"] = "BUY"
        elif last_row["RSI_14"] > 70:
            signal["signal"] = "SELL"
        await self.bus.publish(EventName.SIGNAL_GENERATED, signal)
        # await self.bus.publish(EventName.LOG_ADD,
        #                        f"Signal plugin [{self.name}] dispatched")
