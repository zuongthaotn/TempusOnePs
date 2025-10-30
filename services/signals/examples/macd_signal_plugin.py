from services.base_service import BaseServicePlugin
from core.event_bus import EventName
import pandas as pd
import pandas_ta as ta


class MacdSignalPlugin(BaseServicePlugin):
    async def setup(self):
        await self.bus.publish(EventName.LOG_ADD,
                               f"Signal plugin [{self.name}] initialized and subscribe {EventName.DATA_NEW}")
        self.bus.subscribe(EventName.DATA_NEW, self.find_signal)

    async def find_signal(self, market_data):
        # await self.bus.publish(EventName.LOG_ADD, f"[{self.name}] Finding MACD signal for {market_data['symbol']}")
        data = market_data['df']
        macd = ta.macd(data["Close"], fast=12, slow=26, signal=9)
        data = pd.concat([data, macd], axis=1)
        data.rename(columns={"MACD_12_26_9": "MACD", "MACDh_12_26_9": "MACDh", "MACDs_12_26_9": "MACDs"}, inplace=True)
        # MACD logic
        data["MACD_prev"] = data["MACD"].shift(1)
        data["Signal_prev"] = data["MACDs"].shift(1)
        data["Buy_Signal"] = (data["MACD_prev"] < data["Signal_prev"]) & (data["MACD"] > data["MACDs"])
        data["Sell_Signal"] = (data["MACD_prev"] > data["Signal_prev"]) & (data["MACD"] < data["MACDs"])
        last_data = data.iloc[-1]
        signal = {"service_name": self.name, "event_name": EventName.SIGNAL_GENERATED,
                  "symbol": market_data["symbol"], "signal": None}
        if last_data["Buy_Signal"]:
            signal["signal"] = "BUY"
        elif last_data["Sell_Signal"] > 70:
            signal["signal"] = "SELL"
        await self.bus.publish(EventName.SIGNAL_GENERATED, signal)
        # await self.bus.publish(EventName.LOG_ADD, f"Signal plugin [{self.name}] dispatched")
