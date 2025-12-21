<<<<<<< HEAD
from .vehicle import Vehicle
=======
from transport import Vehicle
>>>>>>> parent of b05519b (add modules in gui)

class Truck(Vehicle):
    def __init__(self, capacity, color):
        self.color = str(color)
        super().__init__(capacity)