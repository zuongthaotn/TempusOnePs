import os
import aiofiles
from datetime import datetime
from services.base_service import BaseServicePlugin
from core.event_bus import EventName
from core.forfun import banner


class ExampleLogFileService(BaseServicePlugin):
    def __init__(self, name, event_bus, config=None):
        self.log_file = None
        super(ExampleLogFileService, self).__init__(name, event_bus, config=config)

    async def setup(self):
        current_folder = os.path.dirname(os.path.abspath(__file__))
        log_file = current_folder + "/example.log"
        self.log_file = await aiofiles.open(log_file, "a", encoding="utf-8")
        await self.write_log("\n" + banner + "\n")
        await self.write_log("[SYSTEM] 🚀 Starting TempusOne Engine...")
        events = []
        for name in dir(EventName):
            if not name.startswith("__"):
                event = getattr(EventName, name)
                events.append(event)
        for ev in events:
            self.bus.subscribe(ev, self.do_trigger)
        await self.write_log(f"Log plugin [{self.name}] initialized and subscribe: {events}")

    async def do_trigger(self, msg):
        if isinstance(msg, str):
            await self.write_log(f"Log msg: {msg}")
        else:
            if msg['event_name'] == EventName.DATA_NEW:
                if len(msg['df']):
                    last_row = msg['df'].iloc[-1]
                    await self.write_log(f"[{msg['service_name']}] "
                                         f"[{msg['event_name']}] Get new dataframe")
                    await self.write_log(f"[{msg['service_name']}] "
                                         f"[{msg['event_name']}] Last data: \nTime: {msg['df'].index[-1]}, "
                                         f"Open: {last_row['Open']}, Close: {last_row['Close']}, "
                                         f"High: {last_row['High']}, Low: {last_row['Low']}")
                else:
                    await self.write_log(f"[{msg['service_name']}] "
                                         f"[{msg['event_name']}] Got issue when getting new data")
            elif msg['event_name'] == EventName.SIGNAL_GENERATED:
                await self.write_log(f"[{msg['service_name']}] [{msg['event_name']}] dispatched. "
                                     f"Symbol: {msg['symbol']}. Signal: {msg['signal']}")
            elif msg['event_name'] == EventName.ORDER_NEW:
                await self.write_log(f"[{msg['service_name']}] [{msg['event_name']}] dispatched. "
                                     f"call API & created new order")

    async def write_log(self, msg):
        cur_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        await self.log_file.write(cur_time + " " + msg + "\n")
        await self.log_file.flush()

    async def teardown(self):
        print(f"Done!")
        await self.log_file.close()
