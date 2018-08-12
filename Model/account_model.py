
class BalanceItem:
    def __init__(self,data):
        self.coin = None
        self.available_balance = None
        self.locked_balance = None
        self.btc_value = None

        self.load_data(data)

    def load_data(self, data):
        self.coin = data['coin']
        self.available_balance = data['available_balance']
        self.locked_balance = data['locked_balance']
        self.btc_value = data['btc_value']


class Balance:

    def __init__(self, data=None):
        self.balances = {}
        if data is None:
            data = [{'coin': 'BTC', 'available_balance':99, 'locked_balance':0, 'btc_value':0}]
        self.load_data(data)

    def load_data(self, data):
        for item in data:
            self.balances[item['coin']] = BalanceItem(item)


