import json

ABC = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
cipher = "EKMFLGDQVZNTOWYHXUSPAIBRCJ"


class Rotor:
    ABC = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    name = ""
    cypher = ""
    notch = ''
    position_ring = ""
    setting = ""

    def __init__(self, name, cypher, notch, position_ring, setting):
        self.name = name
        self.cypher = Rotor.caesar(self, cypher, ABC.index(setting))
        self.notch = notch
        self.position_ring = Rotor._rotate(ABC, ABC.index(position_ring))
        self.setting = setting

    @staticmethod
    def _rotate(text: str, ticks: int):
        cut = len(text) - ticks
        text = text[cut:] + text[:cut] if ticks > 0 else text
        return text[0]

    def forward_encode(self, letter: chr):
        return Rotor._encode_letter(letter, self.position_ring, ABC, self.cypher)

    def backward_encode(self, letter: chr):
        return Rotor._encode_letter(letter, self.position_ring, self.cypher, ABC)

    @staticmethod
    def _encode_letter(letter: chr, position: chr, first: str, second: str) -> chr:
        size = len(ABC)

        index_of_p = ABC.index(position)
        index_of_l = ABC.index(letter)

        f = first[(index_of_l - index_of_p) % size]

        s = second.index(f)
        index = first.index(f)
        return ABC[(size + (s-index)) % size]

    def notch_position1(self, letter: chr):
        return self.notch == letter

    def turn(self):
        if self.position_ring == "Z":
            self.position_ring = "A"
        else:
            self.position_ring = ABC[ABC.index(self.position_ring) + 1 % len(ABC)]

    @staticmethod
    def _caesar_ch(ch, shift):
        n = ord(ch)
        if ord('A') <= n <= ord('Z'):
            n = n - ord('A')
            n = (n + shift) % 26
            n = n + ord('A')
            return chr(n)
        else:
            return ch

    def caesar(self, s, shift):
        return ''.join(self._caesar_ch(ch, shift) for ch in s)
