from datetime import datetime
from services.base_service import BaseServicePlugin
from core.event_bus import EventName


class BaseDataServicePlugin(BaseServicePlugin):
    async def setup(self):
        await self.bus.publish(EventName.LOG_ADD, f"Data plugin [{self.name}] initialized.")

    async def run(self):
        pass

    def build_data(self, **kwargs):
        return {
            "timestamp": datetime.now().isoformat(),
            "service_name": self.name,
            "event_name": EventName.DATA_NEW,
            "symbol": kwargs.get("symbol"),
            "df": kwargs.get("df", None)
        }
