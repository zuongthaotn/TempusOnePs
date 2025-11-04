from datetime import datetime
from services.base_service import BaseServicePlugin
from core.event_bus import EventName


DEFAULT_SIGNAL_PAYLOAD = {
    "signal": None,
    "Close": None,
    "Open": None,
    "High": None,
    "Low": None
}


class SignalConfig:
    BUY_SIGNAL = "buy"
    SELL_SIGNAL = "sell"
    CLOSE_SIGNAL = "close"
    CLOSE_BUY_SIGNAL = "close.buy"
    CLOSE_SELL_SIGNAL = "close.sell"
    SWITCH_TO_BUY_SIGNAL = "switch.to.buy"
    SWITCH_TO_SELL_SIGNAL = "switch.to.sell"


class BaseSignalPlugin(BaseServicePlugin):
    async def setup(self):
        await self.bus.publish(EventName.LOG_ADD,
                               f"Signal plugin [{self.name}] initialized and subscribe {EventName.DATA_NEW}")
        self.bus.subscribe(EventName.DATA_NEW, self.find_signal)

    async def find_signal(self, market_data):
        pass

    def build_data(self, **kwargs):
        payload = kwargs.get("payload", None)
        if payload is not None:
            payload = DEFAULT_SIGNAL_PAYLOAD | payload
        return {
            "timestamp": datetime.now().isoformat(),
            "service_name": self.name,
            "event_name": EventName.SIGNAL_GENERATED,
            "symbol": kwargs.get("symbol"),
            "algo_version": kwargs.get("algo_version"),
            "payload": payload
        }
