from math import factorial
from os import popen
from string import ascii_lowercase as SYMBOLS
from string import ascii_uppercase as UPPER_SYMBOLS
from typing import Any, Callable, Optional


CRYPT_COLS = 10
M = len(SYMBOLS)

# A small help-function for pretty printing:
N_COLS = int(popen("stty size", "r").read().split()[1])
print_center = lambda s, f: print(str.center(s, N_COLS, f))


# --------------------------------------------------------------------------------


def print_crypt(text: str) -> None:
    marks_end_of_word = lambda n: n % 5 == 4
    marks_end_of_line = lambda n: n % (5 * CRYPT_COLS) == 5 * CRYPT_COLS - 1
    for i, char in enumerate(text):
        print(char, end="")
        if marks_end_of_word(i):
            print(" ", end="")
        if marks_end_of_line(i):
            print()
    print()


def excercise_header(text: str) -> Callable:
    def decorator(f: Callable) -> Callable:
        def wrapper(skip: Optional[bool] = False, **kwargs: Any) -> None:
            print_center(text, "-")
            if skip:
                print("(skipping)\n")
                return
            f(**kwargs)

        return wrapper

    return decorator


# --------------------------------------------------------------------------------


class TrivialCipher:
    def encrypt(self, message: str) -> str:
        plaintext = "".join(char for char in str.lower(message) if char in SYMBOLS)
        return "".join(self._encrypt_char(char) for char in plaintext)

    def decrypt(self, ciphertext: str) -> str:
        assert all(char in UPPER_SYMBOLS for char in ciphertext)
        return "".join(self._decrypt_char(char) for char in ciphertext)

    def _encrypt_char(self, char: str) -> str:
        return str.upper(char)

    def _decrypt_char(self, char: str) -> str:
        return str.lower(char)


class CipherWheel(TrivialCipher):
    def __init__(self, shift: int) -> None:
        self.shift = shift % M

    def set_shift(self, new_shift: int) -> None:
        self.shift = new_shift % M

    def _encrypt_char(self, char: str) -> str:
        return UPPER_SYMBOLS[(SYMBOLS.find(char) + self.shift) % M]

    def _decrypt_char(self, char: str) -> str:
        return SYMBOLS[(UPPER_SYMBOLS.find(char) - self.shift) % M]


class SubstitutionCipher(TrivialCipher):
    def __init__(self, permuted_symbols: str) -> None:
        assert all(char in UPPER_SYMBOLS for char in permuted_symbols)
        assert len(permuted_symbols) == M
        self._cipher = {k: v for k, v in zip(SYMBOLS, permuted_symbols)}
        self._decipher = {v: k for k, v in self._cipher.items()}

    def _encrypt_char(self, char: str) -> str:
        return self._cipher[char]

    def _decrypt_char(self, char: str) -> str:
        return self._decipher[char]


# --------------------------------------------------------------------------------


@excercise_header(" Exercise 1.1. ")
def exercise_1_1() -> None:
    def print_helper(encr: str, decr: str, message: Optional[str] = None) -> None:
        if message:
            print(message)
        print_crypt(encr)
        print_crypt(decr)
        print()

    print("a)")
    cipher_wheel = CipherWheel(11)
    message = "A page of history is worth a volume of logic."
    encrypted = cipher_wheel.encrypt(message)
    decrypted = cipher_wheel.decrypt(encrypted)
    print_helper(encrypted, decrypted, message)

    print("b)")
    cipher_wheel.set_shift(7)
    encrypted = "AOLYLHYLUVZLJYLAZILAALYAOHUAOLZLJYLAZAOHALCLYFIVKFNBLZZLZ"
    decrypted = cipher_wheel.decrypt(encrypted)
    print_helper(encrypted, decrypted)

    print("c)")
    encrypted = "XJHRFTNZHMZGAHIUETXZJNBWNUTRHEPOMDNBJMAUGORFAOIZOCC"
    decrypted = ""
    for i, char in enumerate(encrypted, 1):
        cipher_wheel.set_shift(i)
        decrypted += cipher_wheel.decrypt(char)
    print_helper(encrypted, decrypted)


# --------------------------------------------------------------------------------


@excercise_header(" Exercise 1.2. ")
def exercise_1_2(show_only_solution: bool = True) -> None:
    cipher_wheel = CipherWheel(0)

    inputs = [
        ("a)", "LWKLQNWKDWLVKDOOQHYHUVHHDELOOERDUGORYHOBDVDWUHH", 3),
        ("b)", "UXENRBWXCUXENFQRLQJUCNABFQNWRCJUCNAJCRXWORWMB", 9),
        ("c)", "BGUTBMBGZTFHNLXMKTIPBMAVAXXLXTEPTRLEXTOXKHHFYHKMAXFHNLX", 19),
    ]
    for problem_name, encrypted, solution in inputs:
        print(problem_name)
        for i in [solution] if show_only_solution else range(1, M):
            cipher_wheel.set_shift(i)
            print_crypt(cipher_wheel.decrypt(encrypted))
        print()


# --------------------------------------------------------------------------------


@excercise_header(" Exercise 1.3. ")
def exercise_1_3() -> None:
    def print_helper(encr: str, decr: str, message: Optional[str] = None) -> None:
        if message:
            print(message)
        print_crypt(encr)
        print_crypt(decr)
        print()

    permuted_symbols = "SCJAXUFBQKTPRWEZHVLIGYDNMO"
    subst_cipher = SubstitutionCipher(permuted_symbols)

    print("a)")
    message = "The gold is hidden in the garden."
    encrypted = subst_cipher.encrypt(message)
    decrypted = subst_cipher.decrypt(encrypted)
    print_helper(encrypted, decrypted, message)

    print("b)")
    for CHAR in UPPER_SYMBOLS:
        print(f"  {CHAR}", end="")
    print()
    for char in subst_cipher.decrypt(UPPER_SYMBOLS):
        print(f"  {char}", end="")
    print("\n")

    print("c)")
    encrypted = "IBXLXJVXIZSLLDEVAQLLDEVAUQLB"
    decrypted = subst_cipher.decrypt(encrypted)
    print_helper(encrypted, decrypted)


# --------------------------------------------------------------------------------


@excercise_header(" Exercise 1.4. ")
def exercise_1_4() -> None:
    pass


# --------------------------------------------------------------------------------


def mult(low, high):
    result = 1
    for fac in range(low, high + 1):
        result = result * fac
    return result


def n_choose_k(n, k):
    return mult(max(k + 1, n - k + 1), n) // mult(1, min(k, n - k))


def D(n, k):
    if n < 0 or k < 0 or n < k or n == k + 1:
        return 0
    if n == k:
        return 1
    if k == 0:
        return (n - 1) * (D(n - 1, 0) + D(n - 2, 0))
    return n_choose_k(n, k) * D(n - k, 0)


@excercise_header(" Exercise 1.5. ")
def exercise_1_5() -> None:
    print(
        """a)
The number of simple substitution ciphers for a 26 letter alphabet is
the number of ways to permute 26 objects. This number is 
    26! = 26*25*24*...

b)
The number of permutations that leave no letter fixed is known as the
number of "derangements", often denoted  !n . More generally, if we
want to permute  n  objects leaving  k  of them fixed, we are dealing
with "partial derangements", and the number of possible suitable 
permutations is referred to as the "rencontres number" for  n  and  k.
These are typically denoted
               # of partial derangements
    D_{n, k} = of  n  objects that leave
               k  of them fixed

(i) We want to find  D_{n, 0} = !n  for  n=26.  We might try to seek
a closed form expression for  !n , but would quickly come to realize
that this is very difficult to do. (There is a delightfully elegant
and wholly surprising way to do it, but it is not easy to derive)

Instead, let us see if we can find some recurrence relation for the
numbers  !n .

When placing the first letter, "a", we have  n-1  options that put it
in a different place.

Say we place it in spot number 2, belonging to "b". Then, how many
ways are there to permute the remaining  n-1  letters?

We could either put the letter "b" in "a"'s spot, and derange the
remaining  n-2  letters. That could be done in  !(n-2)  ways.
Or, we could avoid putting "b" in "a"'s spot, which we might realise
can be done in  !(n-1)  ways.

This is true for every one of the  n-1  options we had for the
position of "a", and so we arrive at the recurrence relation
    !n = (n-1) * (!(n-1) + !(n-2))
With this, we can compute  !26  recursively:    """
    )
    for n in range(27):
        print(f"  n={n}:  !n={D(n, 0)}")
    print(
        f"""If we compare this result to  n! , we get
    n! / !n
  = {factorial(26)} / {D(26, 0)}
  = {factorial(26) / D(26, 0)}
which is a curiously good approximation of the constant  e ...    """
    )
    print(
        f"""(ii) We now want to find the number of permutations with at least one
letter fixed. This is easy, knowing the total number of permutations,
being  n! , and the number of derangements, being  !n . The answer is
    n! - !n
  = {factorial(n)} - {D(n, 0)}
  = {factorial(n) - D(n, 0)}    """
    )
    print(
        """(iii) Now, how many with exactly one fixed letter? That is, we want
to compute  D_{n, 1}. There are  n  choices we can make for the fixed
letter. The rest will have to be deranged, which can be done in 
D_{n-1, 0} = !(n-1)  ways. So, we get
    D_{n, 1} = n * D_{n-1, 0}    """
    )
    print(f"  = 26 * {D(25, 0)}")
    print(f"  = {26 * D(25, 0)}")
    print(
        """( In general, there are  nCk  ways to choose the  k  fixed letters in
the permutation, and the remaining  n-k must be deranged. That is,
    D_{n, k} = nCk * D_{n-k, 0}   
which makes it easy to calculate any number  D_{n, k}. )    """
    )
    print(
        """(iv) Knowing the values  n!, D_{26, 0}, D_{26, 1}  it is easy to find
the number of permutations leaving at least 2 letters fixed. There
are  n! , and only  D_{26, 0} + D_{26, 1}  that do not satisfy the
requirement. so the answer is
    n! - D_{n, 0} - D_{n, 1}
    26! - !26 - 26 * !25"""
    )
    print(f"  = {factorial(26)}")
    print(f"              - {D(26, 0)} - {D(26, 1)}")
    print(f"  = {factorial(26) - D(26, 0) - D(26, 1)}")
    print()


@excercise_header(" Exercise 1.6. ")
def exercise_1_6() -> None:
    print(
        """Prove:
a)  that a|b  and  b|c , then  a|c
By definition,
    a|b  <=> b = an,    and     b|c  <=> c = bm
for some integers  n,m ,
    =>  c = bm = anm = ak  <=>  a|c
Which was what we wanted to show            []

b)  that if  a|b  and  b|a , then  b = +- a
By the same logic as in (a), we here see that, for some ints.  m,n :
    b = an  and  a = bm
    =>  b = bmn
    => mn = 1
This is only possible for the pairs of integers  
    (n,m) = (1,1) or (-1,-1)
i.e. either   b = a   or   b = -a,
i.e.    b = +- a                            []

c)  that if  a|b  and  a|c ,  then  a|(b+c)  and  a|(b-c)
By definition,
    a|b, a|c    <=>     b = an,  c = am
    =>  b+-c = an+-am = a(m+-n)
    <=>  a|(b+-c)                           []
    """
    )


@excercise_header(" Exercise 1.7. ")
def exercise_1_7() -> None:
    def print_helper(a, b):
        print(f"a)  {a}  =  {a//b} * {b} + {a%b}")

    pairs_of_numbers = [
        (34787, 353),
        (238792, 7843),
        (9829387493, 873485),
        (1498387487, 76348),
    ]
    for a, b in pairs_of_numbers:
        print_helper(a, b)
        print()


# ================================================================================
# ================================================================================


if __name__ == "__main__":
    print_center(" Exercises chapter 1 ", "=")
    exercise_1_1(skip=False)  # skip=True)
    exercise_1_2(skip=False, show_only_solution=True)  # skip=True)
    exercise_1_3(skip=False)
    exercise_1_4(skip=False)
    exercise_1_5(skip=False)
    exercise_1_6(skip=False)
    exercise_1_7(skip=False)
