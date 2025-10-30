from services.base_service import BaseServicePlugin
from core.event_bus import EventName


class ExampleExecutionService(BaseServicePlugin):
    async def setup(self):
        print(f"Signal plugin [{self.name}] initialized and subscribe {EventName.SIGNAL_GENERATED}")
        self.bus.subscribe(EventName.SIGNAL_GENERATED, self.on_signal)

    async def on_signal(self, signal):
        order = {"symbol": signal["symbol"], "signal": signal["signal"], "from": signal["plugin"]}
        print(f"[{self.name}] executed order: {order}")
        await self.bus.publish("order.new", order)
