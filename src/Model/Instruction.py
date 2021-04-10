class Instruction:
    """Clase que representa una instrución"""

    name = ""
    steps = []

    def __init__(self, name, steps):
        self.name = name
        self.steps = steps