class InstructionStep:
    """Clase que representa un paso a seguir de la instrucción"""

    ingredients = []
    equipment = []

    def __init__(self, ingredients, equipment):
        self.ingredients = ingredients
        self.equipment = equipment