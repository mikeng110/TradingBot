import time
import threading


class FetcherBot:
    def __init__(self, model, exchange):
        self.model = model
        self.exchange = exchange
        self.running = False
        self.frequency = 0.1
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
            exchange = "Binance"
            symbol = self.model.target_currency + "/" + self.model.base_currency

            data = self.exchange.fetch_price_info(exchange, symbol)

            if exchange not in self.model.price_info:
                self.model.price_info[exchange] = {symbol: data}
            else:
                self.model.price_info[exchange][symbol] = data

            self.model.target_price = self.exchange.get_price(exchange, symbol)
            self.model.account_balance = self.exchange.get_balance(self.model.base_currency)

            self.model.update_func("account_balance")
            self.model.update_func("target_price")
            self.lock.release()

            time.sleep(self.frequency)

    #





