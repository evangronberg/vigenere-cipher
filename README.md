# Vigenère Cipher
A command line tool for using and breaking the Vigenère cipher.

## Usage
Navigate to the project directory and run `python vigenere.py` followed by one of these three commands:

- `encrypt`

Encrypts a given plaintext using the specified key.\
Specify an input text file via the `-i` flag, an output text file via the `-o` flag, and a key via the `-k` flag.

`python vigenere.py encrypt -i plaintext.txt -o ciphertext.txt -k key`

- `decrypt`

Decrypts a given ciphertext using the specified key.\
Specify an input text file via the `-i` flag, an output text file via the `-o` flag, and a key via the `-k` flag.

`python vigenere.py decrypt -i ciphertext.txt -o plaintext.txt -k key`

- `crack`

Analyzes a given ciphertext and outputs its plaintext, as well the key that was originally used to encrypt the message.\
Specify an input text file via the `-i` flag (required) and an output text file via the `-o` flag (optional - the plaintext is also outputted to the console).\
Specify a key length via the `-l` flag (required) and a number of characters to test per key character via the `-n` flag (optional - set to 3 by default).

`python vigenere.py crack -i ciphertext.txt -l 3`

## Dependencies
- `click`
- `pyspellchecker`
- `ftfy`
