class Utils:
    def __int__(self):
        pass

    def bool_to_int(self, b):
        if b:
            return 1
        else:
            return 0

    def str_to_float(self, str):
        precision = 10
        if str == "" or str is None or str == "None":
            return round(0.0, precision)
        try:
            return float(self.format_float(str, precision))
        except ValueError:
            print("invalid format, expected decimal.")

    def format_float(self, value, precision):
        value = float(value)
        format_str = "{0:." + str(precision) + "f}"
        return format_str.format(value)


    #Utils for Exchanges

    def nestled_key_exist(self, data, sub_val=()):
        try:
            for key in sub_val:
                if type(data[key]) is dict:
                    data = data[key]
                else:
                    return True

        except KeyError:
            return False

    def parse_market_entry(self, entry):
        temp = {}
        temp["symbol"] = entry["symbol"]
        temp["base_currency"] = entry["quote"]
        temp["target_currency"] = entry["base"]
        temp["amount_min"] = entry["limits"]["amount"]["min"]
        temp["amount_max"] = entry["limits"]["amount"]["max"]
        temp["precision_price"] = entry["precision"]["price"]
        temp["precision_amount"] = entry["precision"]["amount"]
        temp["precision_base_currency"] = entry["precision"]["quote"] if self.nestled_key_exist(entry, ["precision",
                                                                                                        "quote"]) and \
                                                                         entry["precision"]["quote"] is not None else 8

        temp["precision_target_currency"] = entry["precision"]["base"] if self.nestled_key_exist(entry, ["precision",
                                                                                                         "base"]) and \
                                                                          entry["precision"]["base"] is not None else 8
        return temp
