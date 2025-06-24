import random
from driver_manager import drivers, get_driver

def read_plate():
    plate = random.choice(list(drivers.keys()))
    owner = get_driver(plate)
    return plate, owner

