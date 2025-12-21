<<<<<<< HEAD
from .vehicle import Vehicle
=======
from transport import Vehicle

>>>>>>> parent of b05519b (add modules in gui)

class Ship(Vehicle):
    def __init__(self, capacity, name):
        super().__init__(capacity)
        
        self.name = name