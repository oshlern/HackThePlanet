import random
from MakeMerkleTree import merkle
import json
from hashlib import sha256
import requests as req
from http.server import BaseHTTPRequestHandler, HTTPServer

# The structure of a transaction
# encryptions and information each group has access to
# {
# address: (THE ADDRESS)
# source: (address or bank account)
# dest: (address or bank account)
# ENCRYPTED:
# tx_value: (int)
# tx_type: (string) (element of [hard_inquiry, derogatory_mark, transaction, loan, account_setup, account_deletion]) (etc.)
# 
# }

class Server(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        self.request = request
        self.client_address = client_address
        self.server = server

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        self.wfile.write(bytes(self.blockchain.blocks[self.blockchain.blocknum-1].hash, encoding="utf-8")) # Just return the newest hash
        return

    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself

        if(post_data == "request_update"):
            self.wfile.write([b.dump() for b in self.blockchain.blocks])

class Blockchain:
    def __init__(self):
        self.blocks = []
        self.blocknum = 0

        self.blocks.append(Block(0, 0, Transaction(0, 0, "", 0))) # Null genesis block

    def validate_chain(self, chain=None): # False if chain is invalid, true if it is valid
        if chain == None:
            chain = self.blocks

        last_block = chain[0] # Genesis block
        for block in chain[1:]:
            if(block.prev_hash != sha256(json.dumps(last_block.header).encode()).digest().hex()):
                return False
            if block.hash != merkle(block.transaction.dump()):
                return False
            last_block = block
        return True
    
    def add_block_transaction(self, user_address, transaction):
        new_block = Block(sha256(json.dumps(self.blocks[self.blocknum].header).encode()).digest().hex(), user_address, transaction)
        new_block.header['nonce'] = new_block.find_nonce(2)
        self.blocks.append(new_block)
        self.blocknum += 1

    def add_block(self, new_block):
        new_block.header['nonce'] = new_block.find_nonce(2)
        self.blocks.append(new_block)
        self.blocknum += 1

class Block:
    def __init__(self, prev_hash, user_address, transaction):
        self.prev_hash = prev_hash
        self.user_address = user_address
        self.transaction = transaction
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
            "transaction": self.transaction.dump(),
            "hash": merkle(self.transaction.dump()),
            "header": self.header
        }
        return temp_dict

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
    return join(random.choice(string.ascii_lowercase + string.digits) for _ in range(n))

def run(server_class=HTTPServer, handler_class=Server, port=8080):
    server_address = ('127.0.0.1', port)
    httpd = server_class(server_address, handler_class)
    print('Starting httpd...')
    httpd.serve_forever()

if(__name__ == "__main__"):
    # blockchain = Blockchain()
    # for i in range(1,11):
    #     blockchain.add_block_transaction(i, Transaction(i, i+1, "transaction", 1))
    
    # print(blockchain.validate_chain())
    
    blockchain = Blockchain()
    nodes = set() # List of IP addresses of the other blockchains
    usertable = set()

    run()