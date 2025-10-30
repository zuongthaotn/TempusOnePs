import pandas as pd
import numpy as np
from services.base_service import BaseServicePlugin
from core.event_bus import EventName


def random_ohlc_df(
        start="2025-01-01",
        periods=100,
        freq="1min",
        start_price=1000,
        volatility=0.002
):
    dates = pd.date_range(start=start, periods=periods, freq=freq)

    # random price
    returns = np.random.normal(0, volatility, size=periods)
    prices = start_price * np.exp(np.cumsum(returns))

    # create OHLC dataframe
    df = pd.DataFrame(index=dates)
    df["Open"] = prices
    df["High"] = df["Open"] * (1 + np.random.uniform(0, 0.003, size=periods))
    df["Low"] = df["Open"] * (1 - np.random.uniform(0, 0.003, size=periods))
    df["Close"] = df["Low"] + (df["High"] - df["Low"]) * np.random.rand(periods)
    df["Volume"] = np.random.randint(100, 2000, size=periods)
    return df


class DataServiceExampleRandom(BaseServicePlugin):
    async def setup(self):
        print(f"[{self.name}] Data plugin initialized")

    async def run(self):
        df = random_ohlc_df(periods=50, freq="5min")
        data = {"service_name": self.name, "event_name": EventName.DATA_NEW, "symbol": "BTCUSDT", "df": df}
        print(f"[{self.name}] generated new dataframe")
        await self.bus.publish(EventName.DATA_NEW, data)
