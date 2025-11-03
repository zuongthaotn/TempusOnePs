from datetime import datetime
from services.base_service import BaseServicePlugin
from core.event_bus import EventName


class BaseExecutionServicePlugin(BaseServicePlugin):
    async def setup(self):
        await self.bus.publish(EventName.LOG_ADD,
                               f"Execution plugin [{self.name}] initialized and subscribe {EventName.SIGNAL_GENERATED}")
        self.bus.subscribe(EventName.SIGNAL_GENERATED, self.with_signal)

    async def with_signal(self, signal_data):
        pass

    def build_data(self, **kwargs):
        return {
            "timestamp": datetime.now().isoformat(),
            "service_name": self.name,
            "event_name": EventName.ORDER_NEW,
            "symbol": kwargs.get("symbol"),
            "payload": kwargs.get("payload", None)
        }
