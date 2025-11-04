from datetime import datetime
from services.base_service import BaseServicePlugin
from core.event_bus import EventName


DEFAULT_EXECUTION_PAYLOAD = {
    "order_type": "MTL",
    "qty": 1,
    "price": 1200,
    "signal": None,
    "order_side": None
}


class BaseExecutionServicePlugin(BaseServicePlugin):
    async def setup(self):
        await self.bus.publish(EventName.LOG_ADD,
                               f"Execution plugin [{self.name}] initialized and subscribe {EventName.SIGNAL_GENERATED}")
        self.bus.subscribe(EventName.SIGNAL_GENERATED, self.with_signal)

    async def with_signal(self, signal_data):
        pass

    def build_data(self, **kwargs):
        payload = kwargs.get("payload", None)
        if payload is not None:
            payload = DEFAULT_EXECUTION_PAYLOAD | payload
        return {
            "timestamp": datetime.now().isoformat(),
            "service_name": self.name,
            "event_name": EventName.ORDER_NEW,
            "symbol": kwargs.get("symbol"),
            "payload": payload
        }
