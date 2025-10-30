from services.base_service import BaseServicePlugin
from core.event_bus import EventName


class ExampleLogService(BaseServicePlugin):
    async def setup(self):
        for ev in ["bar.new", "signal.new", "order.new"]:
            self.bus.subscribe(ev, self.log_event)

    async def log_event(self, data):
        print(f"[{self.name}] log event: {data}")
