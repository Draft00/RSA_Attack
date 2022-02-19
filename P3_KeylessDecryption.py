def decipher(n : int, c : int, e : int) -> int:
    ci = c
    ci_last = None
    while True:
        ci = pow(ci, e, n)
        if ci == c % n:
            break
        else:
            ci_last = ci
    return ci_last

if __name__ == "__main__":
    n = 9173503
    e = 3
    d = 6111579
    m = 111

    print("1. Encrypt message %s with e=%s." % (m, e))
    print("2. Decipher process: ", end="")
    if decipher(n, pow(m, e, n), e) == m:
        print("success.")
    else:
        print("failure.")