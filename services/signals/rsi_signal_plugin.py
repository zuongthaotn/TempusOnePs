from core.base_service import BasePluginService


class RsiSignalPlugin(BasePluginService):
    async def setup(self):
        self.bus.subscribe("bar.new", self.on_bar)

    async def on_bar(self, bar):
        # Giả lập RSI logic
        if bar["price"] < 120:
            signal = {"plugin": self.name, "symbol": bar["symbol"], "action": "BUY"}
            print(f"[{self.name}] signal: {signal}")
            await self.bus.publish("signal.new", signal)
