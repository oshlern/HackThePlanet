import random
from MakeMerkleTree import merkle
import json
from hashlib import sha256

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

class Blockchain:
    def __init__(self):
        self.blocks = []
        self.blocknum = 0
        self.DIFF = 4

        self.blocks.append(Block(0, 0, Transaction(0, 0, "", 0))) # Null genesis block

    def add_block_transaction(self, user, transaction):
        new_block = Block(self.blocks[len(block)-1].hash, user, transaction)
        self.blocks.append(new_block)
        self.blocknum += 1

    def add_block(self, new_block):
        self.blocks.append(new_block)
        self.blocknum += 1

class Block:
    def __init__(self, prev_hash, user, transaction):
        self.prev_hash = prev_hash
        self.user = user
        self.transaction = transaction
        self.hash = merkle(self.transaction.dump())
        self.header = {'addr': self.user, 'ph':prev_hash, 'merkle': self.hash, 'nonce': 0}

    def find_nonce(self):
        nonce = 0
        head = self.header
        tester = sha256(json.dumps(head).encode())
        while tester.digest().hex()[:self.DIFF] != '0'*self.DIFF:
            nonce += 1
            head['nonce'] = nonce
            tester = sha256(json.dumps(head).encode())
        #print(nonce)
        #print(tester.digest().hex())
        return nonce
        
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

def generate_random_text(n):
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(n))