import random

def sample_f(n):
    """sample one coefficient from f(n)
    takes n; larger n gives tigher noise
    returns an int in the set {-2, -1, 0, 1, 2}"""

    a = [random.randint(0, 1) for _ in range(n)]
    sign = 2 * a[n-1] - 1 # sign is +1 if last bit is 1, else -1
    magnitude = (1 - a[0]) + 2 * int(all(a[i] == 1 for i in range(n-1)))
    return sign * magnitude