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
