from services.base_service import BaseServicePlugin
from core.event_bus import EventName


class ExampleLogPrintService(BaseServicePlugin):
    async def setup(self):
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
        if isinstance(msg, str):
            print(f"Log msg: {msg}")
        else:
            if msg['event_name'] == EventName.DATA_NEW:
                print(f"Log msg: [{msg['service_name']}] [{msg['event_name']}] Get new dataframe")
                print(f"Log msg: [{msg['service_name']}] [{msg['event_name']}] Last date is {msg['df'].index[-1]}")
            elif msg['event_name'] == EventName.SIGNAL_GENERATED:
                print(f"Log msg: [{msg['service_name']}] [{msg['event_name']}] dispatched. "
                      f"Symbol: {msg['symbol']}. Signal: {msg['signal']}")
            elif msg['event_name'] == EventName.ORDER_NEW:
                print(f"Log msg: [{msg['service_name']}] [{msg['event_name']}] dispatched. "
                      f"call API & created new order")
