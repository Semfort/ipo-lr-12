<<<<<<< HEAD
from .client import Client
from .vehicle import Vehicle
=======
from transport import Client
from transport import Vehicle
>>>>>>> parent of b05519b (add modules in gui)

class TransportCompany:
    def __init__(self, name):
        self.name = name
        self.vehicles = []
        self.clients = []

    def add_vehicle(self, vehicle):
        if not isinstance(vehicle, Vehicle):
            raise TypeError("Добавляемый объект должен быть наследником Vehicle")
        for v in self.vehicles:
            if v.vehicle_id == vehicle.vehicle_id:
                raise ValueError(f"Транспорт с таким ID уже существует")
        self.vehicles.append(vehicle)

    def list_vehicles(self):
        return self.vehicles
    
    def add_client(self, client):
        if not isinstance(client, Client):
            raise TypeError("Добавляемый объект должен быть наследником Client")
        for c in self.clients:
            if client.name == c.name:
                raise ValueError(f"Такой клиент уже существует")
        self.clients.append(client)
    
    def optimize_cargo_distribution(self):

        sorted_vehicles = sorted(self.vehicles, key=lambda v: v.capacity)
        sorted_clients = sorted(self.clients, key=lambda a: not a.is_vip)
        unloaded_clients = []
    
        for client in sorted_clients:
            loaded = False

            for vehicle in sorted_vehicles:
                if vehicle.current_load + client.cargo_weight <= vehicle.capacity:
                    try:
                        vehicle.load_cargo(client)
                        loaded = True
                        break
                    except ValueError:
                        continue
        
            if not loaded:
                unloaded_clients.append(client)