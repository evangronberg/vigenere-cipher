"""
Author: Evan Gronberg
Email:  emg0011@uah.edu
Date:   September 3, 2021
Class:  CS 585 (Computer Security)

Module for encrypting/decrypting 
a message using the Vigenere cipher.
"""

# Regex library for validating input
import re
# Ceiling function for key concatenation
from math import ceil

class VigenereCipher():
    """
    Class for encrypting/decrypting 
    a message using the Vigenere cipher. 
    """

    ALPHANUMERIC_MAPPING = {
        'a': 0, 'b': 1, 'c': 2, 'd': 3,
        'e': 4, 'f': 5, 'g': 6, 'h': 7,
        'i': 8, 'j': 9, 'k': 10, 'l': 11,
        'm': 12, 'n': 13, 'o': 14, 'p': 15,
        'q': 16, 'r': 17, 's': 18, 't': 19,
        'u': 20, 'v': 21, 'w': 22, 'x': 23,
        'y': 24, 'z': 25
    }

    LETTERS = list(ALPHANUMERIC_MAPPING.keys())

    def encrypt(self, plaintext, key):
        """
        Encrypts plaintext using a key string.
        """
        return self.cipher(plaintext, key, 'encrypt')

    def decrypt(self, ciphertext, key):
        """
        Decrypts a ciphertext using a key string.
        """
        return self.cipher(ciphertext, key, 'decrypt')

    def cipher(self, message, key, mode):
        """
        Depending on mode, either enciphers
        or deciphers the inputted message
        based on the inputted key.
        """
        # Checks that valid input was received
        if not self.verify_input(message, key):
            return 'ERROR: Invalid message or key received.'

        # Concatenates the key to itself
        # as many times as necessary
        key_multiplier = ceil(len(message) / len(key))
        key = key * key_multiplier

        output = ''
        key_index = 0
        for character in message:
            # If the character is punctuation,
            # simply add it to the output
            if character in [' ', '.', ',', "'", '"', '?', '!', '’', '\n']:
                output += character
                continue
            # Otherwise, ciphers the character
            # and increments the key index
            character = character.lower()
            output += self.map(character, key[key_index], mode)
            key_index += 1

        return output

    def map(self, character, key, mode):
        """
        Maps a given character to another
        based on the inputted key character.
        """
        # If encrypting, ADDS the values
        # of the message and key characters
        if mode == 'encrypt':
            numeric_value = self.ALPHANUMERIC_MAPPING[character] +\
                            self.ALPHANUMERIC_MAPPING[key]
        # If decrypting, SUBTRACTS the values
        # of the message and key characters
        else:
            numeric_value = self.ALPHANUMERIC_MAPPING[character] -\
                            self.ALPHANUMERIC_MAPPING[key]
        # Applies modulo 26 to get the value
        # back in range of the alphabet
        numeric_value = numeric_value % 26
        # Returns the character value of the above number
        character_value = self.LETTERS[numeric_value]
        return character_value

    def verify_input(self, message, key):
        """
        Verifies that the user's inputted
        strings consist only of letters and spaces.
        """
        message_pattern = re.compile(r'^[a-zA-Z ,.!?\'"’\n]+$')
        key_pattern = re.compile(r'^[a-zA-Z]+$')
        if not re.fullmatch(message_pattern, message):
            return False
        elif not re.fullmatch(key_pattern, key):
            return False
        return True
