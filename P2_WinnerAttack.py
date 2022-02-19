from sys import version_info


import random
import keygen


def contfrac_to_rational(frac):
    """
        Converts a finite continued fraction [a0, ..., an]
        to an x/y rational.
    """
    if len(frac) == 0:
        return (0, 1)
    num = frac[-1]
    denom = 1
    for _ in range(-2, -len(frac) - 1, -1):
        num, denom = frac[_] * num + denom, num
    return num, denom


def rational_to_contfrac(x, y):
    """
        Converts a rational x/y fraction into
        a list of partial quotients [a0, ..., an]
    """
    a = x // y
    pquotients = [a]
    while a * y != x:
        x, y = y, x - a * y
        a = x // y
        pquotients.append(a)
    return pquotients


def convergents_from_contfrac(frac):
    """
        Computes the list of convergents
        using the list of partial quotients
    """
    convs = []
    for i in range(len(frac)):
        convs.append(contfrac_to_rational(frac[0:i]))
    return convs


def bitlength(x):
    assert x >= 0
    return x.bit_length()
    # n = 0
    # while x > 0:
    #     n = n + 1
    #     x = x >> 1
    # return n


def isqrt(n):
    """
        Calculates the integer square root
        for arbitrary large nonnegative integers
    """
    if n < 0:
        raise ValueError('square root not defined for negative numbers')
    if n == 0:
        return 0

    a, b = divmod(bitlength(n), 2)
    x = 2 ** (a + b)
    while True:
        y = (x + n // x) // 2
        if y >= x:
            return x
        x = y


def is_perfect_square(n):
    """
        If n is a perfect square it returns sqrt(n), otherwise returns -1
    """
    h = n & 0xF  # last hexadecimal "digit"

    if h > 9:
        return -1  # return immediately in 6 cases out of 16.

    # Take advantage of Boolean short-circuit evaluation
    if h != 2 and h != 3 and h != 5 and h != 6 and h != 7 and h != 8:
        # take square root if you must
        t = isqrt(n)
        if t * t == n:
            return t
        else:
            return -1

    return -1


def getPrimePair(bits=512):
    def gen_prime(nbits):
        """
            Generates a prime of b bits using the
            miller_rabin_test
        """
        while True:
            p = random.getrandbits(nbits)
            # force p to have nbits and be odd
            p |= 2 ** nbits | 1
            if keygen.rmspp(p):
                return p

    def gen_prime_range(start, stop):
        """
            Generates a prime within the given range
            using the miller_rabin_test
        """
        while True:
            p = random.randrange(start, stop - 1)
            p |= 1
            if keygen.rmspp(p):
                return p

    assert bits % 4 == 0

    p = gen_prime(bits)
    q = gen_prime_range(p + 1, 2 * p)

    return p, q


def generateVulKeys(nbits=1024):
    """
        Generates a key pair
            public = (e,n)
            private = d
        such that
            n is nbits long
            (e,n) is vulnerable to the Wiener Continued Fraction Attack
    """
    assert nbits % 4 == 0

    p, q = getPrimePair(nbits // 2)
    n = p * q
    phi = (p - 1) * (q - 1)

    # generate a d such that:
    #    (d, n) = 1
    #    36d^4 < n
    good_d = False
    while not good_d:
        d = random.getrandbits(nbits // 4)
        if keygen.egcd(d, phi)[0] == 1 and 36 * pow(d, 4) < n:
            good_d = True

    return pow(d, -1, phi), n, d


def Winner_attack(e, n):
    """
        Finds d knowing (e,n) applying the Wiener continued fraction attack
    """
    frac = rational_to_contfrac(e, n)
    convergents = convergents_from_contfrac(frac)

    for (k, d) in convergents:
        # check if d is actually the key
        if k != 0 and (e * d - 1) % k == 0:
            phi = (e * d - 1) // k
            s = n - phi + 1
            # check if the equation x^2 - s*x + n = 0
            # has integer roots
            discr = s * s - 4 * n
            if discr >= 0:
                t = is_perfect_square(discr)
                if t != -1 and (s + t) % 2 == 0:
                    print("Hacked!\nd=%s" % (d))
                    return d
    print("Hacking failure")
    return None


if __name__ == "__main__":
    assert version_info >= (3, 8)

    print("Step 1. Generate vulnerable RSA keys...")
    e, n, d = generateVulKeys()
    print("e=%s\nd=%s\nn=%s\n" % (e, d, n))

    print("Step 2. Run Winner attack...")
    hack_d = Winner_attack(e, n)

    assert hack_d == d
