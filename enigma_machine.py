import json

from Rotor import Rotor

with open("code-book.json", 'r') as f:
    book = dict(json.load(f))
code_book = book

with open("reflector.json", 'r') as f:
    reflector = dict(json.load(f))

with open("rings.json", 'r') as f:
    rings = dict(json.load(f))


# --------------------------------------------------------------------------------------------
# Transmits the letter through the enigma machine
# --------------------------------------------------------------------------------------------
def forward(letter: chr, list_of_rotors: list):
    return_letter = letter
    list_of_rotors[0].turn()
    for rotor in list_of_rotors:
        if rotor.notch_position1(return_letter):
            rotor.turn()
        return_letter = rotor.forward_encode(return_letter)
    return return_letter


# --------------------------------------------------------------------------------------------
# Passes the letter through the reflector
# --------------------------------------------------------------------------------------------
def through_reflector(letter: chr):
    return_letter = reflector.get(letter)
    return return_letter


# --------------------------------------------------------------------------------------------
# Returns the letter back through the rotors
# --------------------------------------------------------------------------------------------
def backward(letter: chr, list_of_rotors: list):
    return_letter = letter
    for rotor in reversed(list_of_rotors):
        return_letter = rotor.backward_encode(return_letter)
    return return_letter


# --------------------------------------------------------------------------------------------
# encryption a letter
# --------------------------------------------------------------------------------------------
def encryption(letter: chr, list_of_rotors: list):
    return_letter = forward(letter, list_of_rotors)
    return_letter = through_reflector(return_letter)
    return_letter = backward(return_letter, list_of_rotors)
    return return_letter


# --------------------------------------------------------------------------------------------
# encryption a word
# --------------------------------------------------------------------------------------------
def word_to_encryption(word1, list_of_rotors: list):
    word_to_return = []
    for letter_i in word1:
        letter = encryption(letter_i, list_of_rotors)
        word_to_return.append(letter)
    return word_to_return


# --------------------------------------------------------------------------------------------
# print the word
# --------------------------------------------------------------------------------------------
def print_word(word_to_print: list):
    count = 0
    for ch in word_to_print:
        print(ch, end='')
        count = count + 1
        if count == 5:
            print(" ", end='')
            count = 0


def change_to_word(word_to_change: list):
    temp = ""
    for ch in word_to_change:
        temp += ch
    return temp


# --------------------------------------------------------------------------------------------
#  get the settings from the code-book and Creates a list of sittings
# --------------------------------------------------------------------------------------------
def get_settings(num):
    settings1 = []
    for letter in code_book.get(num)["settings"]:
        settings1.append(letter)
    return settings1


# --------------------------------------------------------------------------------------------
# get the positions from the code-book and Creates a list of positions
# --------------------------------------------------------------------------------------------
def get_positions(num):
    positions = []
    for ch in code_book.get(num)["positions"]:
        positions.append(ch)
    return positions


# --------------------------------------------------------------------------------------------
# reset the settings of the rotors
# --------------------------------------------------------------------------------------------
def reset_rotors(num: str):
    ciphers = []
    notches = []
    for rotor in code_book.get(num)["rotors"]:
        if rotor in rings:
            ciphers.append(rings[rotor]["cipher"])
            notches.append(rings[rotor]["notch"])

    settings = get_settings(num)
    positions = get_positions(num)

    rotor_1 = Rotor(code_book.get(num)["rotors"][0], ciphers[0], notches[0], positions[0], settings[0])
    rotor_2 = Rotor(code_book.get(num)["rotors"][1], ciphers[1], notches[1], positions[1], settings[1])
    rotor_3 = Rotor(code_book.get(num)["rotors"][2], ciphers[2], notches[2], positions[2], settings[2])
    all_rotors = [rotor_1, rotor_2, rotor_3]
    return all_rotors


if __name__ == '__main__':

    print("Welcome to the Enigma machine.")
    day = input("Enter a day of encryption (a number between 1 to 30) = ")
    is_true = True
    if not day.isdigit():
        print("input is not an int, try again")
        while is_true:
            day = input("try again= ")
            if day.isdigit():
                is_true = False

    rotors = reset_rotors(day)

    word_to_encode = input("Enter a word to encode= ")

    # Ignore special character and spaces
    word_to_encode = ''.join(char for char in word_to_encode if char.isalnum())
    word_to_encode = word_to_encode.upper()

    encrypted_word = word_to_encryption(word_to_encode, rotors)
    print("--------------------------------------")
    print("The word after encryption:.... ", end='')
    print_word(encrypted_word)
    print()
    print("--------------------------------------")
    # ------------------------------------------------------------------------------------------------part B
    print("if you want to continue to the receiving and encrypting a broadcast file click = ok." + '\n'
                                                                                                   " If not click any other button to exit")
    continued = input("your answer?= ")
    if continued == "ok":
        print("lets start....")

        # --------------------------------------------------------------------------------------------
        #  creator the source file and the destination file
        # --------------------------------------------------------------------------------------------
        s = input("Enter the original file= ")
        source_file = open(s, 'w')

        d = input("Enter the target file= ")
        destination_file = open(d, 'a')

        # --------------------------------------------------------------------------------------------
        #  Fills the file with words that the user returns
        # --------------------------------------------------------------------------------------------
        for i in range(1, 30):
            print("Enter a word to encryption for day ", i)
            word_to_en = input("word to encryption =  ")
            source_file.write(str(i) + '\t')
            source_file.write(word_to_en + '\n')
        source_file.close()

        # --------------------------------------------------------------------------------------------
        #  Creates a new list and fills it with values from the file
        # --------------------------------------------------------------------------------------------
        lines = []
        with open(s, 'r') as p:
            for line in p:
                all_lines = line
                all_lines = ''.join([i for i in all_lines if not i.isdigit()])
                all_lines = ''.join(char for char in all_lines if char.isalnum())
                lines.append(all_lines)

        # --------------------------------------------------------------------------------------------
        #  Prints and inserts the words after encryption into the destination file
        # --------------------------------------------------------------------------------------------
        print("words after encryption:")
        for i, word_in_lines in enumerate(lines):
            word_in_lines = word_in_lines.upper()
            i += 1
            rotors_day = reset_rotors(str(i))
            word_in_lines = word_to_encryption(word_in_lines, rotors_day)
            print_word(word_in_lines)
            print()
            word = change_to_word(word_in_lines)
            destination_file.write(word)
        destination_file.close()
else:
    print("good by")
