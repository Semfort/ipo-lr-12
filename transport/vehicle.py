import uuid
from transport import Client

class Vehicle:
    def __init__(self, capacity):
        self.vehicle_id = str(uuid.uuid4())
        self.capacity = capacity
        self.current_load = 0.0
        self.clients_list = []

    def load_cargo(self, client):
        if not isinstance(client, Client):
            raise TypeError(f"Ожидается объект класса Client")
        if self.current_load + client.cargo_weight > self.capacity:
            raise ValueError("Грузоподъёмность меньше добавляемого груза")
        else: 
            self.current_load += client.cargo_weight
            self.clients_list.append(client)
    
    def __str__(self):
        return f"ID транспорта: {self.vehicle_id} Грузоподъемность: {self.capacity} Текущая загрузка: {self.current_load}"