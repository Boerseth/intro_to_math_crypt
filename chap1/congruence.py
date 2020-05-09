from euclid import gcd


def check_identity(N):
    for i in range(N):
        for j in range(N):
            for m in range(1, N):
                if (i * j) % m == 1:
                    assert gcd(i, m) == 1
                    assert gcd(j, m) == 1
                if gcd(i, m) == 1 and gcd(j, m) == 1:
                    assert (i * j) % m == 1
