import multiprocessing as mp
from core.service.base_service import BaseServicePlugin
from datetime import datetime
import pandas as pd


DEFAULT_SIGNAL_PAYLOAD = {
    "signal": None,
    "Close": None,
    "Open": None,
    "High": None,
    "Low": None
}


class SignalConfig:
    NO_SIGNAL = ""
    BUY_SIGNAL = "buy"
    SELL_SIGNAL = "sell"
    CLOSE_SIGNAL = "close"
    CLOSE_BUY_SIGNAL = "close.buy"
    CLOSE_SELL_SIGNAL = "close.sell"
    SWITCH_TO_BUY_SIGNAL = "switch.to.buy"
    SWITCH_TO_SELL_SIGNAL = "switch.to.sell"


class BaseSignalPlugin(BaseServicePlugin):
    def run(self, data):
        return data


class TempusOnePsSignal:
    def __init__(self, signal_classes, data, log_queue):
        self.signal_classes = signal_classes
        self.df = data
        self.log_queue = log_queue

    def run(self):
        self.add_log_queue(self.df, "signal_run", "before")
        """
        run all signal functions as multiprocessing
        """
        cpu_num = len(self.signal_classes)
        with mp.Pool(processes=cpu_num) as pool:
            results = pool.map(
                self.run_single_signal_module,
                [(cfg, self.df) for cfg in self.signal_classes]
            )

        #
        df_merged = self.df
        for r in results:
            df_merged = df_merged.merge(r["data"], left_index=True, right_index=True, how='inner')
            self.add_log_queue(r["data"], r["meta_data"]["service_name"], "result")
        #
        return df_merged

    @staticmethod
    def run_single_signal_module(args):
        """
        args = (signal_cfg, df)
        """
        signal_cfg, df = args
        return signal_cfg.run(df.copy())

    def add_log_queue(self, data=None, service_name="", step="after"):
        if isinstance(data, pd.DataFrame):
            last = data.iloc[-1]
            payload = {
                "index": last.name.isoformat(),
                "values": last.to_dict()
            }
        else:
            payload = data
        log_data = {
            "timestamp": datetime.now().isoformat(),
            "service_name": service_name,
            "trigger_name": service_name + ".trigger_" + step,
            "payload": payload
        }
        self.log_queue.log(log_data)
