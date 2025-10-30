from datetime import date
from datetime import timedelta
from services.base_service import BaseServicePlugin
from core.event_bus import EventName
from lib.stockHistory import getVN30HistoryDataByMinute


class DataServiceDNSE(BaseServicePlugin):
    async def setup(self):
        await self.bus.publish(EventName.LOG_ADD, f"Data plugin [{self.name}] initialized.")

    async def run(self):
        data = getVN30HistoryDataByMinute(ticker="VN30F1M", resolution=5, broker="DNSE")
        last_expire_date = date.today() - timedelta(days=180)
        last_expire_date = last_expire_date.strftime("%Y-%m-%d 00:00:00")
        df = data[data.index > last_expire_date]
        data = {"service_name": self.name, "event_name": EventName.DATA_NEW,
                "symbol": "VN30F1M", "df": df}
        await self.bus.publish(EventName.DATA_NEW, data)
