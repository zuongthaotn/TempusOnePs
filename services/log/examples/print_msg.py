from services.base_service import BaseServicePlugin
from core.event_bus import EventName


class ExampleLogPrintService(BaseServicePlugin):
    async def setup(self):
        events = []
        for name in dir(EventName):
            if not name.startswith("__"):
                event = getattr(EventName, name)
                # if event != EventName.DATA_NEW:
                events.append(getattr(EventName, name))
        print(f"Log msg: Log plugin [{self.name}] initialized and subscribe {events}")
        for ev in events:
            self.bus.subscribe(ev, self.show_log)

    @staticmethod
    async def show_log(message):
        print(f"Log msg: {message}")
