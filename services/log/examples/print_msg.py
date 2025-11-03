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
    async def do_trigger(msg):
        cur_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(msg, str):
            print(f"{cur_time} Log msg: {msg}")
        else:
            if msg['event_name'] == EventName.DATA_NEW:
                if len(msg['df']):
                    print(f"{cur_time} Log msg: [{msg['service_name']}] [{msg['event_name']}] Get new dataframe")
                    print(f"{cur_time} Log msg: [{msg['service_name']}] "
                          f"[{msg['event_name']}] Last date is {msg['df'].index[-1]}")
                else:
                    print(f"{cur_time} Log msg: [{msg['service_name']}] "
                          f"[{msg['event_name']}] Got issue when getting new data")
            elif msg['event_name'] == EventName.SIGNAL_GENERATED:
                print(f"{cur_time} Log msg: [{msg['service_name']}] [{msg['event_name']}] dispatched. "
                      f"Symbol: {msg['symbol']}. Signal: {msg['signal']}")
            elif msg['event_name'] == EventName.ORDER_NEW:
                print(f"{cur_time} Log msg: [{msg['service_name']}] [{msg['event_name']}] dispatched. "
                      f"call API & created new order")
