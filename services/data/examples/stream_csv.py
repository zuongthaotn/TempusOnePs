import os
import pandas as pd
from services.base_service import BaseServicePlugin
from core.event_bus import EventName


class DataServiceExampleCsv(BaseServicePlugin):
    def __init__(self, name, event_bus, config=None):
        self.start_from = 0
        self.csv_file = "VN30F1M_5m.csv"
        self.df = None
        super(DataServiceExampleCsv, self).__init__(name, event_bus, config=config)

    async def setup(self):
        await self.bus.publish(EventName.LOG_ADD, f"[{self.name}] Data plugin initialized.")
        current_folder = os.path.dirname(os.path.abspath(__file__))
        csv_file = current_folder + "/" + self.csv_file
        is_file = os.path.isfile(csv_file)
        if is_file:
            self.df = pd.read_csv(csv_file, index_col='Date', parse_dates=True)
        else:
            self.df = pd.read_csv(
                "https://raw.githubusercontent.com/zuongthaotn/vn-stock-data/main/VN30ps/VN30F1M_5minutes.csv",
                index_col='Date', parse_dates=True)
        await self.bus.publish(EventName.LOG_ADD, f"[{self.name}] Start steaming data from csv({len(self.df)} rows)")

    async def run(self):
        start_row = self.start_from
        to_row = start_row + 50
        if to_row < len(self.df):
            subset = self.df.iloc[start_row: to_row]
            market_data = {"symbol": "VN30F1M", "df": subset}
            await self.bus.publish(EventName.LOG_ADD, f"[{self.name}] Get new dataframe")
            await self.bus.publish(EventName.LOG_ADD, f"[{self.name}] {subset.index[-1]}")
            await self.bus.publish(EventName.DATA_NEW, market_data)
