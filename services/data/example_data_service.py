import random
from core.base_service import BasePluginService


class ExampleDataService(BasePluginService):
    async def setup(self):
        print(f"[{self.name}] Data plugin initialized")

    async def run(self):
        price = random.uniform(100, 200)
        bar = {"symbol": "BTCUSDT", "price": price}
        print(f"[{self.name}] emitted bar: {bar}")
        await self.bus.publish("bar.new", bar)
