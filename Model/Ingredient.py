class Ingredient:
    """Clase que representa una receta"""
    name = ""
    quantity = ""
    unit = ""

    def __init__(self, name, quantity, unit):
        self.name = name
        self.quantity = quantity
        self.unit = unit

