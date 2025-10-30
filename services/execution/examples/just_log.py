from services.base_service import BaseServicePlugin
from core.event_bus import EventName


class ExampleExecutionService(BaseServicePlugin):
    async def setup(self):
        await self.bus.publish(EventName.LOG_ADD,
                               f"Execution plugin [{self.name}] initialized and subscribe {EventName.SIGNAL_GENERATED}")
        self.bus.subscribe(EventName.SIGNAL_GENERATED, self.on_signal)

    async def on_signal(self, signal_data):
        if signal_data["signal"]:
            order = {"service_name": self.name, "event_name": EventName.ORDER_NEW,
                     "symbol": signal_data["symbol"], "signal": signal_data["signal"]}
            await self.bus.publish(EventName.ORDER_NEW, order)
        # await self.bus.publish(EventName.LOG_ADD, f"[{self.name}]: call API & created new order")
