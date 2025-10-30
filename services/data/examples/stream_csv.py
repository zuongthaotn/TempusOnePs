import os
import pandas as pd
from services.base_service import BaseServicePlugin
from core.event_bus import EventName


class DataServiceExampleCsv(BaseServicePlugin):
    def __init__(self, name, event_bus, config=None):
        self.start_from = 0
        self.csv_file = "VN30F1M_5m.csv"
        self.df = None
        super(DataServiceExampleCsv, self).__init__(name, event_bus, config=None)

    async def setup(self):
        print(f"[{self.name}] Data plugin initialized.")
        current_folder = os.path.dirname(os.path.abspath(__file__))
        self.df = pd.read_csv(current_folder + "/" + self.csv_file)
        print(f"[{self.name}] Start steaming data from csv({len(self.df)} rows)")

    async def run(self):
        start_row = self.start_from
        to_row = start_row + 50
        if to_row < len(self.df):
            subset = self.df.iloc[start_row: to_row]
            market_data = {"symbol": "VN30F1M", "df": subset}
            print(f"[{self.name}] Get new dataframe")
            print(f"{self.name}] {subset.iloc[-1].index}")
            await self.bus.publish(EventName.DATA_NEW, market_data)
