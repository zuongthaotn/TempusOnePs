import os
import time
from datetime import date
from datetime import timedelta
from datetime import datetime
import pandas as pd
from core.service.base_service import BaseServicePlugin
from lib.stockHistory import get_vn30f1m_ohcl_history_data


class DataReplayServiceExample(BaseServicePlugin):
    def __init__(self, name, config=None, log_queue=None, mode='live'):
        self.to_row = 0
        self.df = None
        super().__init__(name, config=config, log_queue=log_queue, mode=mode)

    def setup(self):
        self.df = self.get_stock_data()

    def run(self):
        if self.df is not None:
            if not self.to_row:
                self.to_row = len(self.df) - 152
            else:
                self.to_row = self.to_row + 1
            if self.to_row < len(self.df):
                df = self.df.iloc[: self.to_row]
                self.trigger_after(df, "mix")
                return df
            else:
                exit()
        return None
            

    def get_stock_data(self):
        # 1 month ago (approx 30 days)
        one_month_ago_ts = int((datetime.now() - timedelta(days=30)).timestamp())
        try:
            data = get_vn30f1m_ohcl_history_data(ticker="VN30F1M", resolution=5,
                                                    from_=one_month_ago_ts, broker="DNSE")
            return data
        except Exception as e:
            return None