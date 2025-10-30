import asyncio
from collections import defaultdict


class EventName:
    DATA_NEW = "data.new"
    SIGNAL_GENERATED = "signal.generated"
    ORDER_FILLED = "order.filled"
    LOG_ADD = "log.add"


class EventBus:
    def __init__(self):
        self.subscribers = defaultdict(list)

    def subscribe(self, event_name, callback):
        self.subscribers[event_name].append(callback)

    async def publish(self, event_name, data=None):
        if event_name not in self.subscribers:
            return
        for callback in self.subscribers[event_name]:
            await callback(data)


event_bus = EventBus()
