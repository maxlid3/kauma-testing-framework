import sys
import base64
import socket
import argparse

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

# Default Key: 'ABCDEFGHIJKLMNOP'
# Default IV : 'IVIVIVIVIVIVIVIV'

def aes128_cbc_encrypt(iv: str, key: str, plaintext: str) -> bytes:
    iv = bytes(iv, 'utf-8')
    key = bytes(key, 'utf-8')
    plaintext = bytes(plaintext, 'utf-8')
    padder = padding.PKCS7(128).padder()
    padded_plaintext = padder.update(plaintext) + padder.finalize()

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()

    return ciphertext


def start_server(host: str, port: int):
    with socket.socket(socket.AF_INET, socket.SOCK_stream) as server:
        server.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        try:
            server.bind((host, port))
            server.listen()
            print(f'Server listening on {host}:{port}\nPress KeyboardInterrupt(most likey Strg-C) to stop server.')
            while True:
                client_socket, client_adress = server.accept()
                with client_socket:
                    print(f'\nClient connected: {client_adress}')
                    ##############handle_client(client_socket)
                    print('Connection terminated.')

        except KeyboardInterrupt:
            print('Received KeyboardInterrupt, shutting down server...')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(usage='python python %(prog)s kauma_path [options] <args>', description='padding-oracle-server for running a padding-oracle and for encrypting plaintexts for testcases.')
    parser.add_argument('-e', '--encrypt', type=str, help='Encrypt Mode: Enter plaintext to be encrypted. Usable with -iv and --key.')
    parser.add_argument('-iv', type=str, default='IVIVIVIVIVIVIVIV', help="Specify used IV as plaintext. Default: 'IVIVIVIVIVIVIVIV'")
    parser.add_argument('-k', '--key', type=str, default='ABCDEFGHIJKLMNOP', help="Specify used key as plaintext. Default: 'ABCDEFGHIJKLMNOP'")
    parser.add_argument('--host', type=str, default='localhost', help="Specify a host. Default: '::1' (IPv6 localhost)")
    parser.add_argument('--port', type=int, default=12345, help='Specify a port. Default: 12345')

    try:
        args = parser.parse_args()
    except SystemExit:
        print()
        sys.exit(1)

    if args.iv is not None:
        if len(args.iv) != 16:
            print(f'IV has wrong size! ({len(args.iv)}) Should be 16!')
            sys.exit(1)
    if args.key is not None:
        if len(args.key) != 16:
            print(f'Key has wrong size! ({len(args.key)}) Should be 16!')
            sys.exit(1)

    if args.encrypt:
        iv = args.iv
        key = args.key
        plaintext = args.encrypt
        ciphertext = aes128_cbc_encrypt(iv, key, plaintext)
        print('IV'.ljust(19) + ': ' + iv)
        print('Key'.ljust(19) + ': ' + key)
        print('Plaintext'.ljust(19) + ': ' + plaintext)
        print('Ciphertext (Bytes)'.ljust(19) + ': ' + str(ciphertext))
        print('Ciphertext (Base64)'.ljust(19) + ': ' + base64.b64encode(ciphertext).decode('utf-8'))
    else:
        start_server(args.host, args.port)