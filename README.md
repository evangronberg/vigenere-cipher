## Vigenere Cipher
A command line tool for using and breaking the Vigenere cipher.

### Usage
To run, navigate to the project directory 
and run `python vigenere.py` followed by one
of the following commands:

- `encrypt`\
Specify an input text file via the `-i` flag, an output textfile via the `-o` flag, and a key via the `-k` flag.\
*Example:*\
`python vigenere.py encrypt -i plaintext.txt -o ciphertext.txt -k key`
- `decrypt`
Specify an input text file via the `-i` flag, an output textfile via the `-o` flag, and a key via the `-k` flag.\
*Example:*\
`python vigenere.py decrypt -i ciphertext.txt -o plaintext.txt -k key`
- `crack`\
Specify an input file via the `-i` flag (required) and an output file via the `-o` flag (optional - the plaintext is also outputted to the console).\
*Example:*\
`python vigenere.py crack -i ciphertext.txt`

### Dependencies
- `click`
- `pyspellchecker`
- `ftfy`