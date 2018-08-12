


class DatabaseHandlerModel:
    def __init__(self, req_queue):
        self.data_queue = req_queue

    def get_data(self):
        return self.data_queue.get()

    def update_transaction(self, transaction):
        self.data_queue.put({'func': 'update_transaction', 'data': transaction})

    def update_balance(self, balance_item):
        self.data_queue.put({'func': 'update_balance', 'data': balance_item})

    def ping(self):
        print("Ping")
        self.data_queue.put({'func': "update_transaction", 'data': 0})
        self.data_queue.put({'func': "update_transaction", 'data': 0})
        self.data_queue.put({'func': "update_transaction", 'data': 0})
        self.data_queue.put({'func': "update_transaction", 'data': 0})
        self.data_queue.put({'func': "update_transaction", 'data': 0})
        self.data_queue.put({'func': "update_transaction", 'data': 0})






