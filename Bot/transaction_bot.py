import time
import threading


class TransactionBot:
    def __init__(self, model, exchange):
        self.model = model
        self.exchange = exchange
        self.running = False
        self.frequency = 0.5
        self.thread = None
        self.lock = threading.Lock()

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

        if not item.active:
            if price <= item.buy_in:
                print("Buy Item")
                item.active = True
        else:
            if price >= item.target or price <= item.stop_limit: #to do implement trailing target, and trailing stop loss.
                print("Sell")
                item.closed = True


