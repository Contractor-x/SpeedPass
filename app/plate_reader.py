import random
from database import owners, get_owner

def read_plate():
    plate = random.choice(list(owners.keys()))
    owner = get_owner(plate)
    return plate, owner
