from enum import Enum, auto


class TransportCategory(Enum):
    """Transport categories
    Update for: 13.06.2021
    Source: https://api-docs-v2.readthedocs.io/ru/latest/auto_ria/used_cars/options/type-of-transport.html
    """
    cars = 1
    moto = auto()
    water_transport = auto()
    special_equipments = auto()
    trailers = auto()
    trucks = auto()
    buses = auto()
    motorhomes = auto()
    air_transport = auto()
    agricultural_machinery = auto()


class AutoBodyType(Enum):
    """Auto body types
    Update for: 13.06.2021
    Source: https://api-docs-v2.readthedocs.io/ru/latest/auto_ria/used_cars/options/body-types.html
    """
    universal = 2
    sedan = auto()
    hatchback = auto()
    crossover = auto()
    coupe = auto()
    convertible = auto()
    minivan = auto()
    pickup = auto()


class AutoDriverType(Enum):
    """Auto body types
    Update for: 13.06.2021
    Source: https://api-docs-v2.readthedocs.io/ru/latest/auto_ria/used_cars/options/driverTypes.html
    """
    four_wheel = 1
    front_wheel = auto()
    rear_wheel = auto()
