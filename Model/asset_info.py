class AssetInfo:
    def __init__(self, exchange, dict_data):
        self.exchange = exchange
        self.base_currency = None
        self.target_currency = None
        self.amount_min = None
        self.amount_max = None
        self.precision_price = None
        self.precision_amount = None
        self.precision_base_currency = None
        self.precision_target_currency = None

        self.unpack_data(dict_data)

    def unpack_data(self, dict_data):
        self.base_currency = dict_data['base_currency']
        self.target_currency = dict_data['target_currency']
        self.amount_min = float(dict_data['amount_min'])
        self.amount_max = float(dict_data['amount_max'])
        self.precision_price = float(dict_data['precision_price'])
        self.precision_amount = float(dict_data['precision_amount'])
        self.precision_base_currency = float(dict_data['precision_base_currency'])
        self.precision_target_currency = float(dict_data['precision_target_currency'])




