import random
def random_letter():
    num = random.choice(range(0,2**16))
    return chr(num)