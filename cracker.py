"""
Module for cracking the Vigenere cipher.
"""

# Regex library for split ciphertext into threads
import re
# Time library for timing the cracker
import time
# Function for generating all possible
# combinations of potential key characters
from itertools import product

# Object for checking potential plaintexts
from spellchecker import SpellChecker

# Internal library used for decryption
from cipher import VigenereCipher

class VigenereCracker():
    """
    Class for cracking the Vigenere cipher. 
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

    PUNCTUATION = '!"#$%&\'()*+,-./:;<=>?@[\]^_`{|}~’\n'

    def __init__(self, key_length, num_test_chars):
        self.cipher = VigenereCipher()
        self.spell_checker = SpellChecker()
        self.key_length = key_length
        self.num_test_chars = num_test_chars

    def crack_cipher(self, ciphertext):
        """
        Provides a statistical analysis of
        the most likely key for a given ciphertext.
        """
        start_time = time.time()
        # Splits the ciphertext into a number
        # of threads equal to the cipher's key length
        threads = self.split_ciphertext(ciphertext)

        distributions = {}
        popular_letters = {}
        potential_key_characters = []
        # For each letter in the key...
        for i in range(self.key_length):
            # Creates a distribution for each thread
            distributions[i] = self.analyze_thread(threads[i])
            # Retrieves the most popular letters from each distribution
            popular_letters[i] = self.get_popular_letters(distributions[i])
            # Converts those popular letters to potential
            # letters for the ith letter in the key
            potential_key_characters.append([])
            potential_key_characters[i] = self.get_potential_key_characters(popular_letters[i])

        # Generates the potential keys given the potential key characters
        potential_keys = self.get_potential_keys(potential_key_characters)
        
        # Counts the number of non-English words in each potential ciphertext
        potential_keys_word_counter = {}
        for key in potential_keys:
            potential_keys_word_counter[key] = self.get_num_of_misspelled_words(ciphertext, key)

        # Sets the correct key to whichever potential
        # key resulted in the fewest number of non-English words
        correct_key = min(potential_keys_word_counter, key=potential_keys_word_counter.get)
        # Decrypts the plaintext based on the correct key
        plaintext = self.cipher.decrypt(ciphertext, correct_key)
        
        end_time = time.time()
        run_time = end_time - start_time

        return plaintext, correct_key, run_time

    def split_ciphertext(self, ciphertext):
        """
        Splits the ciphertext into the number
        of threads specified by the cipher's key_length.
        """
        threads = {}
        # Creates a thread for each
        # letter in the key
        for i in range(self.key_length):
            threads[i] = ''

        index = 0
        pattern = re.compile(r'^[a-zA-Z]$')
        # Adds only letters from the
        # ciphertext to the threads
        for character in ciphertext:
            if re.fullmatch(pattern, character):
                current_thread = index % self.key_length
                threads[current_thread] += character.lower()
                index += 1
        
        return threads

    def analyze_thread(self, thread):
        """
        Produces a dictionary of the distribution
        of letters in a given thread.
        """
        letter_counts = {}
        for letter in self.LETTERS:
            letter_counts[letter] = 0
        
        total_letter_count = 0
        for character in thread:
            if not character in self.LETTERS:
                continue
            total_letter_count += 1
            letter_counts[character] += 1
        
        distribution = {}
        for letter in self.LETTERS:
            distribution[letter] = float(letter_counts[letter] / total_letter_count)

        return distribution

    def get_popular_letters(self, distribution):
        """
        Returns the most popular letters
        from a given distribution.
        """
        popular_letters = []
        # Sorts the given distribution of letters
        # from least to greatest and casts it to a list of letters
        sorted_distribution = list(sorted(distribution.items(), key=lambda x:x[1]))
        for i in range(self.num_test_chars):
            # Pops off the last (and greatest) value from the
            # list of letters and appends it to the list of popular letters
            popular_letters.append(sorted_distribution.pop()[0])

        return popular_letters

    def get_potential_key_characters(self, popular_letters):
        """
        Returns a list of key letter candidates
        for a given list of popular letters.
        """
        potential_key_characters = []
        for letter in popular_letters:
            numeric_value = self.ALPHANUMERIC_MAPPING[letter] -\
                            self.ALPHANUMERIC_MAPPING['e']
            # Applies modulo 26 to get the value
            # back in range of the alphabet
            numeric_value = numeric_value % 26
            # Returns the character value of the above number
            character_value = self.LETTERS[numeric_value]
            potential_key_characters.append(character_value)

        return potential_key_characters

    def get_potential_keys(self, potential_key_characters):
        """
        Returns a list of potential keys given
        a list of lists of potential key characters.
        """
        potential_keys = []
        potential_key_character_combinations = [c for c in product(*potential_key_characters)]
        for combination in potential_key_character_combinations:
            potential_key = ''
            for letter in combination:
                potential_key += letter
            potential_keys.append(potential_key)
        return potential_keys

    def get_num_of_misspelled_words(self, ciphertext, potential_key):
        """
        Checks to see how many non-English words
        a potential plaintext contains.
        """
        # Gets potential plaintext based on potential key
        potential_plaintext = self.cipher.decrypt(ciphertext, potential_key)
        # Splits the potential plaintext into an array of words
        potential_plaintext_words = potential_plaintext.split(' ')
        # Cleans each word of punctuation
        for index in range(len(potential_plaintext_words)):
            potential_plaintext_words[index] = potential_plaintext_words[index].translate(str.maketrans('', '', self.PUNCTUATION))

        # Gets a list of all misspelled words in the potential plaintext
        misspelled = self.spell_checker.unknown(potential_plaintext_words)
        # Returns the number of misspelled words in the potential plaintext
        return len(misspelled)
