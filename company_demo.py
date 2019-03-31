import random
from MakeMerkleTree import merkle
import json
import string
from blockchain import *
from hashlib import sha256

PAPAJOHNS = {'big_pizza': 20, 'small_pizza': 10, 'kid_pizza': 6, 'salad': 8}
WALMART = {'bike': 300, 'gun': 400, 'desk': 100, 'utensils': 30, 'tupperware': 15}
DEBUG = True

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

def generate_random_text(n):
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(n))

class Company:
    def __init__(self, name, hiring_threshold, bank):
        self.name = name
        self.hiring_threshold = hiring_threshold
        self.bank = bank
        self.employees = []

    def hire(self, user):
        credit = self.bank.get_credit(user)
        if credit >= self.hiring_threshold:
            return True
        else:
            return False

    def __str__(self):
        return self.name

class Bank:
    def __init__(self, name):
        self.accounts = {} # {bank_number: amount}
        self.account_numbers = {} # {User: bank_number}
        self.name = name
        self.blockchain = Blockchain()

    def get_hashed_address(self, user):
        print(sha256((user.ssn + user.name).encode()).digest())
        print(sha256(sha256((user.ssn + user.name).encode()).digest()).digest())
        print(sha256(sha256((user.ssn + user.name).encode()).digest()))
        address = sha256(sha256((user.ssn + user.name).encode()).digest()).digest()
        return address

    def register_user(self, user):
        bank_number = generate_random_text(20)
        self.account_numbers[user] = bank_number
        self.accounts[bank_number] = 0
        return bank_number

    def get_credit(self, user):
        user_transactions = self.find_relevant_transactions(user.address)
        credit = self.compute_credit(user_transactions)
        return credit

    # Find all transactions by the user
    def find_relevant_transactions(self, user_address):
        user_blocks = []
        for block in self.blockchain.blocks:
            if block.header['addr'] == user_address:
                user_blocks.append(block)
        # user_transactions = [decrypt(block, user_key) for block in user_blocks]
        user_transactions = [block.transaction for block in user_blocks]
        return user_transactions

    def compute_credit(self, transactions):
        credit = 0
        
        # TODO: write code to compute credit
        # 35% payment history
        # 30% amount owed
        # 15% length of history
        # 10% new credit
        # 10% type of credit used
        return credit

    def record_transaction(self, address, source, destination, value):
        transaction = Transaction(source, destination, value, "transaction")
        self.blockchain.add_block_transaction(address, transaction)

    def __str__(self):
        return self.name

class User:
    def __init__(self, name, ssn, bank):
        self.name = name
        self.bank = bank
        self.ssn = ssn
        self.address = self.bank.get_hashed_address(self)
        self.bank_account = bank.register_user(self)

    def __str__(self):
        return self.name

class Shop:
    def __init__(self, name, items, bank):
        self.name = name
        self.items = items
        self.bank = bank
        self.bank_account = bank.register_user(self)

    def record_purchase(self, user, item):
        assert item in self.items
        price = self.items[item]
        source = user.bank_account
        destination = self.bank_account
        self.bank.record_transaction(user.address, source, destination, price)
        if DEBUG:
            print("{} bought {} from {} for {} dollars".format(user, item, self, price))

    def __str__(self):
        return self.name

def main():
    BankOfAmerica = Bank("BankOfAmerica")

    Near = Company(name="Near", hiring_threshold=700, bank=BankOfAmerica)
    AspiringProgrammer = User(name="Aliaksandr Hudzilin", ssn="123456", bank=BankOfAmerica)#"123 Electric Ave")

    PapaJohns = Shop("Papa John's", PAPAJOHNS, BankOfAmerica)
    WalMart = Shop("Walmart", WALMART, BankOfAmerica)

    # Run sample transactions
    PapaJohns.record_purchase(AspiringProgrammer, "small_pizza")
    WalMart.record_purchase(AspiringProgrammer, "bike")

    print(Near.hire(AspiringProgrammer))

    print([str(block.transaction) for block in BankOfAmerica.blockchain.blocks])

if __name__ == "__main__":
    main()