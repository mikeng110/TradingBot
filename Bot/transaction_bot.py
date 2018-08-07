import time
import threading
from Controllers.transaction_ctrl import *


class TransactionBot:
    def __init__(self, model, exchange):
        self.model = model
        self.exchange = exchange
        self.running = False
        self.frequency = 0.5
        self.thread = None
        self.lock = threading.Lock()
        self.tc = TransactionCtrl(model, exchange)
        self.margin_of_error = 0.0001

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self.update)
        self.thread.start()

    def stop(self):
        self.running = False

        try:
            self.thread.join()
            print("Thread destroyed")

        except Exception as e:
            return None

    def update(self):

        while self.running:
            self.lock.acquire()
            for item in self.model.transactions:
                if item.closed:
                    continue
                self.process_item(item)

            self.lock.release()

            time.sleep(self.frequency)

    def process_item(self, item):
        price = self.exchange.get_price(item.target_currency + item.base_currency)
        price = float(price)

        #print("This item is an " + item.asset_info.exchange + " item")

        if not item.active:
            if price >= (item.buy_in - item.buy_in * self.margin_of_error) and price <= (item.buy_in + item.buy_in * self.margin_of_error) :
                self.buy(item)

        else:
            if price >= item.target or price <= item.stop_limit: #todo: implement trailing target, and trailing stop loss.
                self.sell(item)

    def buy(self, item):
        if item.paper_trade:
            self.tc.paper_buy(item)
        else:
            print("Real Buy: -> " + item.__str__())

    def sell(self, item):
        if item.paper_trade:
            self.tc.paper_sell(item)
        else:
            print("Real Sell -> " + item.__str__())


