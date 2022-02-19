from sys import version_info
from random import randint, getrandbits

# all this code: https://qna.habr.com/q/7255

def rmspp(number, attempts=28):
    if number < 2:
        return False
    if number == 2:
        return True
    if number % 2 == 0:
        return False

    s = number-1
    r = 0
    while s % 2 == 0:
        r += 1
        # s /= 2
        s //= 2
    while attempts:

        a = randint(1, number - 1)

        if mod_exp(a, s, number) != 1:

            for j in range(0, r):
                if mod_exp(a, (2 ** j) * s, number) == number - 1:
                    break
            else:
                return False
        attempts -= 1
        continue

    return True


def mod_exp(base, exponent, modulus):
    result = 1
    while exponent > 0:
        if (exponent & 1) == 1:
            result = (result * base) % modulus
        exponent >>= 1
        base = (base * base) % modulus
    return result


def keys(bits):
    e = 2 ** 16 + 1
    while True:

        s = bits // 2
        mask = 0b11 << (s - 2) | 0b1
        while True:
            p = getrandbits(s) | mask

            if p % e != 1 and rmspp(p):
                break
        s = bits - s
        mask = 0b11 << (s - 2) | 0b1
        while True:
            q = getrandbits(s) | mask
            if q != p and q % e != 1 and rmspp(q):
                break
        n = p * q
        phi = (p - 1) * (q - 1)

        d = mmi(e, phi)
        if d:
            break
    return (n, e), (n, d)


def mmi(a, m):
    gcd, x, q = egcd(a, m)
    if gcd != 1:

        return None
    else:
        return (x + m) % m


def egcd(a, b):
    if b == 0:
        return (a, 1, 0)
    else:
        d, x, y = egcd(b, a % b)
        return d, y, x - y * (a // b)


if __name__ == "__main__":
    (n, e), (n, d) = keys(512)
    print("n       = {}".format(n))
    print("public  = {}".format(e))
    print("private = {}".format(d))