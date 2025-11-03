from services.base_service import BaseServicePlugin
from core.event_bus import EventName
from datetime import datetime
from core.forfun import banner


class ExampleLogPrintService(BaseServicePlugin):
    async def setup(self):
        print(banner + "\n")
        print("[SYSTEM] 🚀 Starting TempusOne Engine...")
        events = []
        for name in dir(EventName):
            if not name.startswith("__"):
                event = getattr(EventName, name)
                events.append(event)
        print(f"Log msg: Log plugin [{self.name}] initialized and subscribe: {events}")
        for ev in events:
            self.bus.subscribe(ev, self.do_trigger)

    @staticmethod
    async def do_trigger(data):
        if isinstance(data, str):
            cur_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"{cur_time} Log msg: {data}")
        else:
            print(str(data))
