import random


def generate_extranonce1():

    return f"{random.randint(0, 0xffffffff):08x}"
