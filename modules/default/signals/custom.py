from services.base_service import BaseServicePlugin
from core.event_bus import EventName


class CustomSignalPlugin(BaseServicePlugin):
    async def setup(self):
        self.bus.subscribe(EventName.DATA_NEW, self.find_signal)

    async def find_signal(self, event_data):
        signal = {"service_name": self.name, "event_name": EventName.SIGNAL_GENERATED,
                  "symbol": event_data["symbol"], "signal": None}
        await self.bus.publish(EventName.SIGNAL_GENERATED, signal)
