import time
import threading
from Database.Account.account import *
from Database.Account.transactions import *


class DataWriterBot:
    def __init__(self, model):
        self.model = model
        self.req_queue = None
        self.running = False
        self.frequency = 10
        self.thread = None
        self.lock = threading.Lock()
        self.data_to_process = None

        self.transactions_db = None
        self.account_balance_db = None

    def start(self):

        self.running = True
        self.req_queue = self.model.req_queue

        self.transactions_db = Transactions(self.model.db_tradingbot)
        self.account_balance_db = AccountBalance(self.model.db_tradingbot)

        self.thread = threading.Thread(target=self.update)
        self.thread.start()

    def execute_all(self):
        time.sleep(.5)
        item = self.req_queue.get()
        while (item is not None):
            self.process_data(item)
            item = self.req_queue.get()

    def stop(self):
        self.running = False
        self.req_queue.put(None) #require 2 cause the first get ignored, look into it.
        self.req_queue.put(None)
        time.sleep(0.1)
        self.execute_all()
        try:
            self.thread.join()
            print("Thread destroyed")

        except Exception as e:
            return None

    def update(self):
        while self.running:
            self.lock.acquire()
            self.data_to_process = self.req_queue.get(block=True)

            if self.data_to_process is None:
                return

            self.process_data(self.data_to_process)
            self.lock.release()

            time.sleep(self.frequency)

    def process_data(self, data_to_process):

        if data_to_process is None:
            return

        if data_to_process['func'] == "update_balance":
            try:
                balance_data = data_to_process['data']

                self.account_balance_db.update(balance_data.coin, balance_data.available_balance, balance_data.locked_balance, balance_data.btc_value)

            except sqlite3.OperationalError as e:
                print(e)

            return

        if data_to_process['func'] == "update_transaction":
            try:
                self.transactions_db.update(data_to_process['data'])

            except sqlite3.OperationalError as e:
                print(e)