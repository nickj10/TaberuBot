class Ingredient:
    """Clase que representa una receta"""
    name = ""
    amount = ""
    unit = ""

    def __init__(self, name, quantity, unit):
        self.name = name
        self.quantity = quantity
        self.unit = unit

