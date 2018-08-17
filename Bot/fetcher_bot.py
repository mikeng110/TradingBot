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

    def update(self): #Next step, write so you can fetich price of multiple exchanges.

        while self.running:
            self.lock.acquire()
            exchange = self.model.current_exchange
            symbol = self.model.current_asset_info.symbol

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





