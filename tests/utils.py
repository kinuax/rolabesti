import random
import string


def get_random_string() -> str:
    return "asdf"
    seed = string.ascii_letters + string.digits
    return "".join(random.sample(seed, len(seed)))
