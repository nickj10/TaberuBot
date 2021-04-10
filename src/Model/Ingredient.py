class Ingredient:
    """Clase que representa una receta"""
    name = ""
    amount = ""
    unit = ""

    def __init__(self, name, amount, unit):
        self.name = name
        self.amount = amount
        self.unit = unit

