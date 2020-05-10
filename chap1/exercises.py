from string import ascii_lowercase as SYMBOLS
from string import ascii_uppercase as UPPER_SYMBOLS
from typing import Optional


CRYPT_COLS = 10
M = len(SYMBOLS)


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
        if i % (5*CRYPT_COLS) == 5*CRYPT_COLS - 1:
            print("\n", end="")
    print()
    

def exercise_1_1():
    # a)
    cipher_wheel = CipherWheel(11)
    message = "A page of history is worth a volume of logic."
    encrypted = cipher_wheel.encrypt(message)
    decrypted = cipher_wheel.decrypt(encrypted)
    print(message)
    print_crypt(encrypted)
    print_crypt(decrypted)
    print()

    # b)
    cipher_wheel.set_shift(7)
    encrypted = "AOLYLHYLUVZLJYLAZILAALYAOHUAOLZLJYLAZAOHALCLYFIVKFNBLZZLZ"
    decrypted = cipher_wheel.decrypt(encrypted)
    # -> therearenosecretsbetterthanthesecretsthateverybodyguesses
    print_crypt(encrypted)
    print_crypt(decrypted)  
    print()

    # c)
    encrypted = "XJHRFTNZHMZGAHIUETXZJNBWNUTRHEPOMDNBJMAUGORFAOIZOCC"
    decrypted = ""
    for i, char in enumerate(encrypted):
        cipher_wheel.set_shift(i + 1)
        decrypted += cipher_wheel.decrypt(char)
    # -> whenangrycounttenbeforeyouspeakifveryangryanhundred
    print_crypt(encrypted)
    print_crypt(decrypted)  
    print()


def exercise_1_2():
    cipher_wheel = CipherWheel(0)
    show_solution = True
    inputs = [
        ("LWKLQNWKDWLVKDOOQHYHUVHHDELOOERDUGORYHOBDVDWUHH", 3),
        # ithinkthatishallneverseeabillboardlovelyasatree
        ("UXENRBWXCUXENFQRLQJUCNABFQNWRCJUCNAJCRXWORWMB", 9),
        # loveisnotlovewhichalterswhenitalterationfinds
        ("BGUTBMBGZTFHNLXMKTIPBMAVAXXLXTEPTRLEXTOXKHHFYHKMAXFHNLX", 19),
        # inbaitingamousetrapwithcheesealwaysleaveroomforthemouse
    ]   

    def helper(text: str, solution: Optional[int]) -> None:
        for i in ([solution] if solution else range(1, M)):
            cipher_wheel.set_shift(i)
            print_crypt(cipher_wheel.decrypt(encrypted))

    for encrypted, solution in inputs:
        helper(encrypted, solution if show_solution else None)
        print()


if __name__ == "__main__":
    # exercise_1_1()
    exercise_1_2()
