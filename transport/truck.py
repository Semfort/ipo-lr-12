from .vehicle import Vehicle

class Truck(Vehicle):
    def __init__(self, capacity, color):
        self.color = str(color)
        super().__init__(capacity)