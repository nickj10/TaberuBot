class Metric:
    """Class that represents a metric"""
    amount = ""
    unitShort = ""

    def __init__(self, amount, unitShort):
        self.amount = amount
        self.unitShort = unitShort