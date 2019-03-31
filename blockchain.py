import random
from MakeMerkleTree import merkle
import json
from hashlib import sha256
from flask import Flask, jsonify, request
import requests as req
from http.server import BaseHTTPRequestHandler, HTTPServer
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import PKCS1_OAEP

# The structure of a transaction
# encryptions and information each group has access to
# {
# address: (THE ADDRESS)
# source: (address or bank account)
# dest: (address or bank account)
# ENCRYPTED:
# tx_value: (int)
# tx_type: (string) (element of [hard_inquiry, derogatory_mark, transaction, loan, account_setup, account_deletion]) (etc.)
# }

class Blockchain:
    def __init__(self):
        self.blocks = []
        self.blocknum = 0

        self.blocks.append(Block(0, 0, Transaction(0, 0, "", 0)).dump()) # Null genesis block

    def validate_chain(self, chain=None): # False if chain is invalid, true if it is valid
        if chain == None:
            chain = self.blocks

        last_block = chain[0] # Genesis block
        for block in chain[1:]:
            if(block['prev_hash'] != sha256(last_block['header'].encode()).digest().hex()):
                return False
            last_block = block
        return True
    
    def add_block_transaction(self, user_address, transaction, key):
        new_block = Block(sha256(json.dumps(self.blocks[self.blocknum]['header']).encode()).digest().hex(), user_address, transaction, key)
        new_block.header['nonce'] = new_block.find_nonce(2)
        self.blocks.append(new_block.dump())
        self.blocknum += 1

    def add_block(self, new_block):
        new_block.header['nonce'] = new_block.find_nonce(2)
        self.blocks.append(new_block.dump())
        self.blocknum += 1

class Block:
    def __init__(self, prev_hash, user_address, transaction, key):
        self.prev_hash = prev_hash
        self.user_address = user_address
        self.transaction = transaction
        self.key = key
        self.hash = merkle(self.transaction.dump()) # IS THIS WRONG??
        self.header = {'addr': self.user_address, 'ph': prev_hash, 'merkle': merkle(self.transaction.dump()), 'nonce': 0}

    def find_nonce(self, DIFF):
        nonce = 0
        head = self.header
        # print(head, type(head))
        # print(json.dumps(head))
        tester = sha256(json.dumps(head).encode())
        while tester.digest().hex()[:DIFF] != '0'*DIFF:
            nonce += 1
            head['nonce'] = nonce
            tester = sha256(json.dumps(head).encode())
        #print(nonce)
        #print(tester.digest().hex())
        return nonce
    
    def dump(self):
        temp_dict = {
            "prev_hash": self.prev_hash,
            "user_address": self.user_address,
            "transaction": encrypt_txs(self.key),
            "hash": merkle(self.transaction.dump()),
            "header": json.dumps(self.header)
        }
        return temp_dict
    
    def encrypt_txs(self, pub_key):
        # key = RSA.generate(2048)
        # private_key = key

        # public_key = key.publickey()
       
        # data = "I met aliens in UFO. Here is the map.".encode("utf-8")
        # session_key = get_random_bytes(16)

        # Encrypt the session key with the public RSA key
        cipher_rsa = PKCS1_OAEP.new(pub_key)
        enc_txs = cipher_rsa.encrypt(self.transaction.dump())

        # Decrypt the session key with the private RSA key
        # cipher_rsa = PKCS1_OAEP.new(private_key)
        # session_key = cipher_rsa.decrypt(enc_session_key)
        return enc_txs

class Transaction:
    def __init__(self, src, dst, tx_type, tx_value):
        self.source = src
        self.dest = dst
        self.value = tx_value
        self.type = tx_type

    def dump(self):
        temp_dict = {'source': self.source,
                    'dest': self.dest,
                    'value': self.value,
                    'type': self.type
                    }
        return json.dumps(temp_dict)

    def __str__(self):
        return self.dump()

def generate_random_text(n):
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(n))


# blockchain = Blockchain()
# for i in range(1,11):
#     blockchain.add_block_transaction(i, Transaction(i, i+1, "transaction", 1))

# print(blockchain.validate_chain())

blockchain = Blockchain()
nodes = set()
usertable = set()

app = Flask(__name__)

@app.route('/latest_hash', methods=['GET'])
def get_latest_hash():
    return blockchain.blocks[blockchain.blocknum-1].hash

@app.route('/blockchain', methods=['GET'])
def get_blockchain():
    temp = str([b for b in blockchain.blocks])[1:-1].replace("'", '"')
    return temp

@app.route('/add_block', methods=['POST'])
def recv_block():
    values = request.get_json()
    user = values["user"]
    transaction = Transaction(values["transaction"]["src"], values["transaction"]["dest"], values["transaction"]["tx_type"], values["transaction"]["tx_value"])
    blockchain.add_block_transaction(user, transaction, )
    return "complete\n" + blockchain.blocks[blockchain.blocknum-1].hash

if(__name__ == "__main__"):
    app.run(host='127.0.0.1', port=8080)
