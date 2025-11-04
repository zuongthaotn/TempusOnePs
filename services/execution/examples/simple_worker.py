from datetime import datetime
from services.execution.base_execution import BaseExecutionServicePlugin
from core.event_bus import EventName

BUY_SIGNAL = 'long'
SELL_SIGNAL = 'short'
CLOSE_SIGNAL = 'close'
LONG_DEAL_TYPE = "NB"
SHORT_DEAL_TYPE = "NS"
TRADING_FEE = 0.7


class Broker:
    def __init__(self):
        self.symbol = ""
        self.entry_price = 0
        self.exit_price = 0
        self.entry_time = ''
        self.exit_time = ''
        self.is_long_open = False
        self.is_short_open = False
        self.mode = 'dev'
        self.qty = 0
        self.stoploss = 0
        self.trailing_sl = 0
        self.take_profit = 0
        self.deal_id = 0

    def set_qty(self, new_qty):
        self.qty = new_qty

    def set_symbol(self, symbol):
        self.qty = symbol

    def set_stoploss(self, price):
        self.stoploss = price

    def set_trailing_sl(self, price):
        self.trailing_sl = price

    def set_take_profit(self, price):
        self.take_profit = price

    def pull_deal_data(self):
        # Call API
        pass

    def has_opened_deal(self):
        return True if (self.is_short_open or self.is_long_open) else False

    def trigger_before(self):
        pass

    def trigger_after(self):
        pass

    def open_long_deal(self, price):
        self.trigger_before()
        deal_type = LONG_DEAL_TYPE
        self.open_deal(deal_type, price)
        self.trigger_after()

    def open_short_deal(self, price):
        self.trigger_before()
        deal_type = SHORT_DEAL_TYPE
        self.open_deal(deal_type, price)
        self.trigger_after()

    def open_deal(self, deal_type, price):
        cur_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if deal_type == LONG_DEAL_TYPE:
            self.entry_time = cur_time
            self.is_long_open = True
            self.entry_price = price
        elif deal_type == SHORT_DEAL_TYPE:
            self.entry_time = cur_time
            self.is_short_open = True
            self.entry_price = price

    def close_all_open_deal(self, current_price):
        self.trigger_before()
        if self.is_long_open:
            self.close_long_deal(current_price)
        elif self.is_short_open:
            self.close_short_deal(current_price)
        self.trigger_after()

    def close_long_deal(self, price):
        cur_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.trigger_before()
        self.entry_time = ''
        self.qty = 0
        self.exit_price = price
        self.exit_time = cur_time
        self.is_long_open = False
        self.trigger_after()

    def close_short_deal(self, price):
        cur_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.trigger_before()
        self.entry_time = ''
        self.qty = 0
        self.exit_price = price
        self.exit_time = cur_time
        self.is_short_open = False
        self.trigger_after()


class SimpleWorkerExecutionService(BaseExecutionServicePlugin):
    def __init__(self, name, event_bus, config=None):
        self.broker = None
        super(SimpleWorkerExecutionService, self).__init__(name, event_bus, config=config)

    async def with_signal(self, signal_data):
        if signal_data["payload"] is not None:
            if signal_data["payload"]["signal"] is not None and signal_data["payload"]["signal"] != "":
                signal = signal_data["payload"]["signal"]
                current_price = signal_data["payload"]["Close"]
                payload = None
                if current_price:
                    if signal == BUY_SIGNAL:
                        self.broker.open_long_deal(current_price)
                        payload = {"price": current_price, "signal": signal, "order_side": LONG_DEAL_TYPE}
                    elif signal == SELL_SIGNAL:
                        self.broker.open_short_deal(current_price)
                        payload = {"price": current_price, "signal": signal, "order_side": SHORT_DEAL_TYPE}
                    if signal == CLOSE_SIGNAL:
                        if self.broker.has_opened_deal():
                            self.broker.close_all_open_deal()
                            payload = {"price": current_price, "signal": signal}
                    order_data = self.build_data(symbol=signal_data["symbol"], payload=payload)
                    await self.bus.publish(EventName.ORDER_NEW, order_data)
