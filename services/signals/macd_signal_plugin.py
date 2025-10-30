from core.base_service import BasePluginService


class MacdSignalPlugin(BasePluginService):
    async def setup(self):
        self.bus.subscribe("bar.new", self.on_bar)

    async def on_bar(self, bar):
        # Giả lập MACD logic
        if bar["price"] > 180:
            signal = {"plugin": self.name, "symbol": bar["symbol"], "action": "SELL"}
            print(f"[{self.name}] signal: {signal}")
            await self.bus.publish("signal.new", signal)
