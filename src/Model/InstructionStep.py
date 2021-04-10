class InstructionStep:
    """Clase que representa un paso a seguir de la instrucción"""

    step = ""
    ingredients = []
    equipment = []

    def __init__(self, step, ingredients, equipment):
        self.step = step
        self.ingredients = ingredients
        self.equipment = equipment