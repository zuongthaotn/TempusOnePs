from datetime import datetime
import pandas as pd


class BaseServicePlugin:
    def __init__(self, name, config=None, log_queue=None, mode='live'):
        self.name = name
        self.mode = mode
        self.config = config or {}
        self.log_queue = log_queue

    def setup(self):
        pass

    def run(self, data=None):
        pass

    def teardown(self):
        pass

    def trigger_before(self, data=None, strategy_name=""):
        self.trigger(data=data, strategy_name=strategy_name, trigger_name_postfix="before")

    def trigger_after(self, data=None, strategy_name=""):
        self.trigger(data=data, strategy_name=strategy_name, trigger_name_postfix="after")

    def trigger(self, data=None, strategy_name="", trigger_name_postfix=""):
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
            "service_name": self.name,
            "trigger_name": self.name + ".trigger_" + trigger_name_postfix,
            "strategy_name": strategy_name,
            "payload": payload
        }
        self.log_queue.log(log_data)