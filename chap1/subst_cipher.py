from copy import deepcopy
from typing import Callable, Dict, List, Optional, Union
from os import popen
from random import seed, shuffle


# fmt: off
SYMBOLS = [
    "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
    "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
    "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
    "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z",
    "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "=", "+", "-",
    " ", ".", ",", "_", "?", "!", "(", ")", "/", "\\", "*", "%", "&",
    "\n", "\t",
]
# fmt: on


def get_random_perm(random_seed: str) -> List[str]:
    seed(random_seed)
    new_symbols = deepcopy(SYMBOLS)
    shuffle(new_symbols)
    return new_symbols


def get_shift_perm(shift: int) -> List[str]:
    return SYMBOLS[shift:] + SYMBOLS[:shift]


class SubstitutionCipher:
    permitted_permutation_types = ["random", "shift"]

    def __init__(
        self, perm_type: str = "random", encr_key: str = "", encr_shift: int = 0,
    ) -> None:
        assert perm_type in self.permitted_permutation_types
        if perm_type == "random":
            self._cipher = {k: v for k, v in zip(SYMBOLS, get_random_perm(encr_key))}
        if perm_type == "shift":
            self._cipher = {k: v for k, v in zip(SYMBOLS, get_shift_perm(encr_shift))}
        self._decipher = {v: k for k, v in self._cipher.items()}

    def encrypt(self, plaintext: str) -> str:
        return "".join([self._cipher[char] for char in plaintext])

    def decrypt(self, ciphertext: str) -> str:
        return "".join([self._decipher[char] for char in ciphertext])


# -------------------------------------------------------------------------------------


MESSAGE = """In publishing and graphic design, Lorem ipsum is a
placeholder text commonly used to demonstrate the
visual form of a document or a typeface without
relying on meaningful content. Lorem ipsum may be
used before final copy is available, but it may
also be used to temporarily replace copy in a
process called greeking, which allows designers to
consider form without the meaning of the text
influencing the design."""

if __name__ == "__main__":
    # Example of usage:
    cipher = SubstitutionCipher(perm_type="shift", encr_shift=61)
    encrypted = cipher.encrypt(MESSAGE)
    decrypted = cipher.decrypt(encrypted)
    equal: bool = (MESSAGE == decrypted)

    # A small help-function for pretty printing:
    N_COLS = int(popen("stty size", "r").read().split()[1])
    print_center = lambda s, f: print(str.center(s, N_COLS, f))
    # Lots of printing to see the result:
    print()
    print_center(" Message, encrypted, and decrypted ", "=")
    print(f"{MESSAGE}\n\n{encrypted}\n\n{decrypted}")
    print_center("", "=")
    print()
    print_center(
        f"Original and decrypted {'are NOT ' if not equal else 'ARE '}the same!", " "
    )
    print()
