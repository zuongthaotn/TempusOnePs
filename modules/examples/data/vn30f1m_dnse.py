import time
from datetime import date
from datetime import timedelta
from datetime import datetime
from core.service.base_service import BaseServicePlugin
from lib.stockHistory import get_vn30f1m_ohcl_history_data


class DataServiceDNSE(BaseServicePlugin):
    def run(self):
        df = self.get_stock_data()
        self.trigger_after(df, "mix")
        return df

    def get_stock_data(self):
        # 1 year ago (approx 365 days)
        one_year_ago_ts = int((datetime.now() - timedelta(days=365)).timestamp())
        for i in range(0, 15):
            try:
                data = get_vn30f1m_ohcl_history_data(ticker="VN30F1M", resolution=5,
                                                     from_=one_year_ago_ts, broker="DNSE")
                return data
            except Exception as e:
                time.sleep(2)
        return None
