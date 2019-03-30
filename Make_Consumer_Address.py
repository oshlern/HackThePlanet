#!/usr/bin/env python3
import ecdsa
from hashlib import sha256, new
import codecs
# https://github.com/warner/python-ecdsa this is the ecdsa library, since pycrypto doesn't have it
# helpful https://medium.freecodecamp.org/how-to-create-a-bitcoin-wallet-address-from-a-private-key-eca3ddd9c05f


# If you want to import a private key
# WIF decoding for private keys from electrum https://en.bitcoin.it/wiki/Wallet_import_format
def createKeys():
    priv_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)

    # Compressing the private keys and converting them to public keys
    key = priv_key.get_verifying_key()
    key = codecs.encode(key.to_string(), 'hex')
    key_string = key.decode('utf-8')
    key_h_len = len(key) // 2
    key_half = key[:key_h_len]
    # Bitcoin byte, 0x02 if last digit is even, 0x03 if last digit is odd
    last_byte = int(key_string[-1], 16)
    bitcoin_byte = b'02' if last_byte % 2 == 0 else b'03'
    key = bitcoin_byte + key_half
    key = bytearray.fromhex(key.decode('utf-8'))

    # If you already have a compressed public key:
    #key = bytearray.fromhex('02f273a2050dce3b71b406a096b2ac33827eeb0663082ad920102eb006149716fe')

    ripe_fruit = sha256(sha256(key).digest()).digest()
    return codecs.encode(ripe_fruit, 'hex').decode('utf-8'), codecs.encode(priv_key.to_string(), 'hex').decode('utf-8')