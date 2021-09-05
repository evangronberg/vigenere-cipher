import click
from ftfy import fix_text
from cipher import VigenereCipher
from cracker import VigenereCracker

@click.group()
def cli():
    pass

@click.command()
@click.option('-f', '--filename')
@click.option('-m', '--message')
@click.option('-k', '--key', required=True)
def encrypt(input_file, output_file, key):
    cipher = VigenereCipher()
    plaintext_input_file = open(input_file, 'r')
    plaintext_input = plaintext_input_file.read()
    plaintext_input = fix_text(plaintext_input)
    ciphertext_output = cipher.encrypt(plaintext_input, key)
    if output_file:
        ciphertext_output_file = open(output_file, 'w')
        ciphertext_output_file.write(ciphertext_output)

@click.command()
@click.option('-i', '--input_file', required=True)
@click.option('-o', '--output_file', required=True)
@click.option('-k', '--key', required=True)
def decrypt(input_file, output_file, key):
    cipher = VigenereCipher()
    ciphertext_input_file = open(input_file, 'r')
    ciphertext_input = ciphertext_input_file.read()
    ciphertext_input = fix_text(ciphertext_input)
    plaintext_output = cipher.decrypt(ciphertext_input, key)
    if output_file:
        plaintext_output_file = open(output_file, 'w')
        plaintext_output_file.write(plaintext_output)

@click.command()
@click.option('-i', '--input_file', required=True)
@click.option('-o', '--output_file')
def crack(input_file, output_file):
    cracker = VigenereCracker()
    ciphertext_file = open(input_file, 'r')
    ciphertext = ciphertext_file.read()
    ciphertext = fix_text(ciphertext)
    plaintext = cracker.crack_cipher(ciphertext)
    if output_file:
        plaintext_file = open(output_file, 'w')
        plaintext_file.write(plaintext)

if __name__ == '__main__':
    cli.add_command(encrypt)
    cli.add_command(decrypt)
    cli.add_command(crack)
    cli()
