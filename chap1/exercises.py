from os import popen
from string import ascii_lowercase as SYMBOLS
from string import ascii_uppercase as UPPER_SYMBOLS
from typing import Any, Callable, Optional


CRYPT_COLS = 10
M = len(SYMBOLS)

# A small help-function for pretty printing:
N_COLS = int(popen("stty size", "r").read().split()[1])
print_center = lambda s, f: print(str.center(s, N_COLS, f))


class CipherWheel:
    def __init__(self, shift: int) -> None:
        self.shift = shift % M

    def set_shift(self, new_shift: int) -> None:
        self.shift = new_shift % M

    def encrypt(self, message: str) -> str:
        plaintext = "".join(char for char in str.lower(message) if char in SYMBOLS)
        return "".join(self._encrypt_char(char) for char in plaintext)

    def decrypt(self, ciphertext: str) -> str:
        assert all(char in UPPER_SYMBOLS for char in ciphertext)
        return "".join(self._decrypt_char(char) for char in ciphertext)

    def _encrypt_char(self, char: str) -> str:
        return UPPER_SYMBOLS[(SYMBOLS.find(char) + self.shift) % M]

    def _decrypt_char(self, char: str) -> str:
        return SYMBOLS[(UPPER_SYMBOLS.find(char) - self.shift) % M]


def print_crypt(text: str) -> None:
    for i, char in enumerate(text):
        print(char, end="")
        if i % 5 == 4:
            print(" ", end="")
        if i % (5 * CRYPT_COLS) == 5 * CRYPT_COLS - 1:
            print("\n", end="")
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
    for i, char in enumerate(encrypted):
        cipher_wheel.set_shift(i + 1)
        decrypted += cipher_wheel.decrypt(char)
    print_helper(encrypted, decrypted)


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


if __name__ == "__main__":
    print_center(" Exercises chapter 1 ", "=")
    exercise_1_1()  # skip=True)
    exercise_1_2(show_only_solution=False)  # skip=True)
