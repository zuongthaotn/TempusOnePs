from services.base_service import BaseServicePlugin
from core.event_bus import EventName


class ExampleExecutionService(BaseServicePlugin):
    async def setup(self):
        await self.bus.publish(EventName.LOG_ADD,
                               f"Execution plugin [{self.name}] initialized and subscribe {EventName.SIGNAL_GENERATED}")
        self.bus.subscribe(EventName.SIGNAL_GENERATED, self.on_signal)

    async def on_signal(self, signal):
        order = {"symbol": signal["symbol"], "signal": signal["signal"], "from": signal["plugin"]}
        await self.bus.publish(EventName.ORDER_NEW, order)
        await self.bus.publish(EventName.LOG_ADD,
                               f"Execution plugin [{self.name}]: call API & created new order")
