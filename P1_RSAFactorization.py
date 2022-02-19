"""
    python -m pip install sympy
    requires python 3.8+
"""
from sys import version_info
import math
import random
from typing import List


def egcd(a, b):
    if a == 0:
        return b, 0, 1
    g, y, x = egcd(b % a, a)
    return g, x - (b // a) * y, y


def modulo_multiplicative_inverse(a, m):
    return pow(a, -1, m)

# def modulo_multiplicative_inverse(a, m):
#     g, x, y = egcd(a, m)
#     if g != 1:
#         raise Exception('No modular inverse')
#     return x % m


def phi(n):
    from sympy.ntheory.factor_ import totient
    return totient(n)

def rsafactor(d: int, e: int, N: int) -> List[int]:
    """
    This function returns the factors of N, where p*q=N
      Return: [p, q]

    We call N the RSA modulus, e the encryption exponent, and d the decryption exponent.
    The pair (N, e) is the public key. As its name suggests, it is public and is used to
        encrypt messages.
    The pair (N, d) is the secret key or private key and is known only to the recipient
        of encrypted messages.
    """
    k = d * e - 1
    p = 0
    q = 0
    while p == 0:
        g = random.randint(2, N - 1)
        t = k
        while True:
            if t % 2 == 0:
                t = t // 2
                x = pow(g, t, N)
                y = math.gcd(x - 1, N)
                if x > 1 and y > 1:
                    p = y
                    q = N // y
                    break  # find the correct factors
            else:
                break  # t is not divisible by 2, break and choose another g
    return sorted([p, q])

if __name__ == "__main__":
    assert version_info >= (3, 8)
    n = 8771708822383904746827554456624559065188589612292490844455744878860715773468203338896305549126401366847822434986828675092658594372979835112159051508210739
    e = 65537
    d = 2927962863702493251775326629127345684270955130056464740731401726810153321946172662644233935029843480533342196404453763634900059801905651205977946057805313

    print("Step 1. Find p, q...")
    p, q = rsafactor(d, e, n)
    print("p = %s\nq = %s\n" % (p, q))

    assert(p * q == n)

    print("Step 2. Find other d...")
    phi_n = (p - 1)*(q - 1)
    print("d = %s\n" % (modulo_multiplicative_inverse(e, phi_n) % phi_n ))
