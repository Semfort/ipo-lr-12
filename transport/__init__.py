from .client import Client
from .ship import Ship
from .truck import Truck
from .transportCompany import TransportCompany
from .vehicle import Vehicle

# Опционально можно определить __all__ для явного указания экспортируемых имен
__all__ = ['Client', 'Ship', 'Truck', 'TransportCompany', 'Vehicle']