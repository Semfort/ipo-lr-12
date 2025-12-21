from vehicle import Vehicle


class Ship(Vehicle):
    def __init__(self, capacity, name):
        super().__init__(capacity)
        
        self.name = name