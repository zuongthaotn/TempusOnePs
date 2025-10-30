from core.base_service import BasePluginService


class ExampleExecutionService(BasePluginService):
    async def setup(self):
        self.bus.subscribe("signal.new", self.on_signal)

    async def on_signal(self, signal):
        order = {"symbol": signal["symbol"], "side": signal["action"], "from": signal["plugin"]}
        print(f"[{self.name}] executed order: {order}")
        await self.bus.publish("order.new", order)
