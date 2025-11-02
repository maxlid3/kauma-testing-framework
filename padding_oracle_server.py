import sys
import base64
import socket
import argparse

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

# Default Key: 'ABCDEFGHIJKLMNOP'
# Default IV : 'IVIVIVIVIVIVIVIV'


def pksc7_padder(plaintext: str):
    padder = padding.PKCS7(128).padder()
    return padder.update(plaintext) + padder.finalize()

def aes128_cbc_encrypt(iv: str, key: str, plaintext: str) -> bytes:
    iv = bytes(iv, 'utf-8')
    key = bytes(key, 'utf-8')
    plaintext = bytes(plaintext, 'utf-8')

    padded_plaintext = pksc7_padder(plaintext)

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()

    return ciphertext   

def aes128_cbc_decrypt(iv, key, ciphertext) -> bytes:
    if type(iv) is not bytes:
        iv = bytes(iv, 'utf-8')
    if type(key) is not bytes:
        key = bytes(key, 'utf-8')
    if type(ciphertext) is not bytes:
        ciphertext = bytes(key, 'utf-8')

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()

    unpadder = padding.PKCS7(128).unpadder()
    plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()

    return plaintext

def check_pkcs7_padding(plaintext: bytes):
    padding_len = plaintext[-1] # Last Byte should always be padded

    if (padding_len == 0) or padding_len > 16:
        return False
    elif not plaintext[-padding_len:] == bytes([padding_len]) * padding_len:
        return False
    else:
        return True
    
def padding_oracle(iv: str, key: str, ciphertext: str):
    try:
        decrypted_plaintext = aes128_cbc_decrypt(iv, key, ciphertext)
        return True
    except:
        return False
    # return check_pkcs7_padding(decrypted_plaintext)

def recv_exact(socket, n):
    data = b""
    while len(data) < n:
        chunk = socket.recv(n - len(data))
        if not chunk:
            raise ConnectionError('Connection closed before receiving expected data')
        data += chunk
    return data

def handle_client(client_socket: socket.socket, iv: str, key: str):
    # Step 1: 2 Byte key_id
    print('Waiting for key_id (2 Byte)...')

    key_id = client_socket.recv(2)
    print(f'Key_id: {key_id.hex()}')
    if len(key_id) != 2:
        print(f'Wrong key_id size! ({len(key_id)})')
        return

    # Step 2: 16 Byte Ciphertext as binary
    print('Waiting for ciphertext (16 Byte)...')

    ciphertext = client_socket.recv(16)
    print(f'Ciphertext: {ciphertext.hex()}')
    if len(ciphertext) != 16:
        print(f'Wrong ciphertext size! ({len(ciphertext)})')
        return

    while True:
        # Step 3: 2 Byte length field l (for Q-Blocks). If 00, terminate connection
        print('Waiting for length field (2 Byte)...')

        length_field = client_socket.recv(2)
        l = int.from_bytes(length_field, byteorder='little')
        print(f'Length field: {length_field} -> {l}')
        if len(length_field) != 2:
            print(f'Wrong length_field size! ({len(length_field)})')
            return

        if l == 0:
            print('Connection terminated.')
            break

        # Step 4: 16 * l Byte Q-Blocks
        print(f'Waiting for Q-blocks ({16 * l} Byte)...')

        q_blocks = recv_exact(client_socket, 16 * l)
        if len(q_blocks) != 16 * l:
            print(f'Wrong Q-Blocks size! ({len(length_field)})')

        # Step 5: l Byte Answer (01 correct Padding, 00 wrong Padding)
        resp = bytearray()
        for i in range(l):
            if padding_oracle(q_blocks[16 * i:16 * (i + 1)], key, ciphertext):
                resp.append(1)
            else:
                resp.append(0)

        client_socket.sendall(resp)
        print(f'Sent {l} responses.')    

def start_server(host: str, port: int, iv: str, key: str):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        try:
            server.bind((host, port))
            server.listen()
            print(f'Server listening on {host}:{port}\nPress KeyboardInterrupt(most likey Strg-C) to stop server.')
            server.settimeout(2.0)
            while True:
                try:
                    client_socket, client_adress = server.accept()
                    with client_socket:
                        print(f'\nClient connected: {client_adress}')
                        handle_client(client_socket, iv, key)
                        print('Connection terminated.')
                except socket.timeout:
                    continue
                except KeyboardInterrupt:
                    break
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
        print('IV (Base64)'.ljust(19) + ': ' + base64.b64encode(bytes(iv, 'utf-8')).decode('utf-8'))
        print('Key'.ljust(19) + ': ' + key)
        print('Plaintext'.ljust(19) + ': ' + plaintext)
        print('Plaintext (Base64)'.ljust(19) + ': ' + base64.b64encode(pksc7_padder(bytes(plaintext, 'utf-8'))).decode('utf-8'))
        print('Ciphertext (Hex)'.ljust(19) + ': ' + ciphertext.hex())
        print('Ciphertext (Base64)'.ljust(19) + ': ' + base64.b64encode(ciphertext).decode('utf-8'))
    else:
        start_server(args.host, args.port, args.iv, args.key)