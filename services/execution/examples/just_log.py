from services.execution.base_execution import BaseExecutionServicePlugin
from core.event_bus import EventName


class ExampleExecutionService(BaseExecutionServicePlugin):
    async def with_signal(self, signal_data):
        if signal_data["payload"] is not None:
            if signal_data["payload"]["signal"] is not None and signal_data["payload"]["signal"] != "":
                order_data = self.build_data(symbol=signal_data["symbol"], payload=signal_data["payload"])
                await self.bus.publish(EventName.ORDER_NEW, order_data)
