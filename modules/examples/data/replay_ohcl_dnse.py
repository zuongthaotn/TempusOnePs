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
        self.start_from = 0
        self.df = None
        super().__init__(name, config=config, log_queue=log_queue, mode=mode)

    def setup(self):
        self.df = self.get_stock_data().tail(370)

    def run(self):
        if self.df is not None:
            start_row = self.start_from
            to_row = start_row + 350
            if to_row < len(self.df):
                self.start_from = self.start_from + 1
                df = self.df.iloc[: to_row]
                self.trigger_after(df, "ema_cross")
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