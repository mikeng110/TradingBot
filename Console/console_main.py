import time
import threading


class ConsoleMain:
    def __init__(self, model, main_ctrl):
        self.model = model
        self.main_ctrl = main_ctrl

        self.running = False
        self.frequency = 1
        self.thread = None
        self.lock = threading.Lock()
        self.main_ctrl.paper_login()
        self.start()
        print("Console View")

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
        #item = TransactionItem(self.model.transaction_amount, self.model.transaction_buy_in,
                               #self.model.transaction_target, self.model.transaction_stop_limit,
                             # self.model.base_currency, self.model.target_currency)
        #item.paper_trade = self.model.paper_trade_status
        self.model.transaction_amount = 100
        self.model.transaction_buy_in = 0.056504
        self.model.transaction_target = 0.056593
        self.model.transaction_stop_limit = 0.056439
        self.model.paper_trade_status = True
        self.main_ctrl.execute_order()

        while self.running:
            self.lock.acquire()
            print(self.model.target_price)
            self.lock.release()
            time.sleep(self.frequency)


