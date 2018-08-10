import time
import threading

from Database.Account.transactions import *


class DataWriterBot:
    def __init__(self, req_queue):
        self.req_queue = req_queue
        self.running = False
        self.frequency = 1
        self.thread = None
        self.lock = threading.Lock()
        self.data_to_process = None

        self.transactions_db = Transactions()

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self.update)
        self.thread.start()

    def execute_all(self):
        time.sleep(.5)
        item = self.req_queue.get()
        while (item is not None):
            print("Execute All")
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
            self.transactions_db.close()
            print("Writer Thread destroyed")

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

        if data_to_process is None or data_to_process == "STOP":
            print("No data to process")
            return

        if data_to_process['func'] == "update_transaction":
            print("Process transaction")
            print("Writing tom db")
            self.transactions_db.insert_transaction(data_to_process['data']) #temprorary solution to make sure data exist.
            self.transactions_db.update_transaction(data_to_process['data'])
            print("Finish writing to db")

