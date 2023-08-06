import random
def random_letter():
    num = random.choice(range(0,2**16))
    return chr(num)
class randomer:
    def __init__(self):
        None
    def random_letter_(self):
        num = random.choice(range(0,2**16))
        return chr(num)