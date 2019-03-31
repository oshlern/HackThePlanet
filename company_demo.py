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
            print("{} hired {}!".format(self, user))
            self.employees.append(user)
            return True
        else:
            print("{} rejected {}!".format(self, user))
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
        address = sha256(sha256((user.ssn + user.name).encode()).digest()).digest().hex()
        return address

    def register_user(self, user):
        bank_number = generate_random_text(20)
        self.account_numbers[user] = bank_number
        self.accounts[bank_number] = 0
        return bank_number

    def get_credit(self, user):
        print("{} fetching {}'s transactions using their hashed signature from blockchain database".format(self, user))
        user_transactions, user_merkles = self.find_relevant_transactions(user.address)
        user_transactions = user.decrypt_please(user_transactions)
        for tx in range(len(user_transactions)):
            if merkle(user_transactions[tx]) != user_merkles[tx]:
                raise ValueError("Incorrect merkle hash, {} is lying".format(user))
            else:
                print("{}'s decrypted transactions verified via merkle hash".format(user))
        credit = self.compute_credit(user, user_transactions)
        if DEBUG:
            print("Retrieved {}'s credit: {}".format(user, credit))
        return credit

    # Find all transactions by the user
    def find_relevant_transactions(self, user_address):
        user_blocks = []
        for block in self.blockchain.blocks:
            if block['header']['addr'] == user_address:
                user_blocks.append(block)
        # user_transactions = [decrypt(block, user_key) for block in user_blocks]
        user_transactions = [block['transaction'] for block in user_blocks]
        user_merkles = [block['hash'] for block in user_blocks]
        return user_transactions, user_merkles

    def compute_credit(self, user, transactions):
        credit = 0
        derog = 0
        transactions = [json.loads(transaction) for transaction in transactions]
        for transaction in transactions:
            if transaction['type'] == "derogatory_mark":
                derog += 1
            else:
                derog = 0
            if derog == 0:
                payment_history += 75
            if derog == 1:
                payment_history += 55
            if derog == 2:
                payment_history += 25
            if derog == 3:
                payment_history += 15
            if derog == 4:
                payment_history += 10
            else:
                payment_history = 0
        payment_history = 0
        amount_in_bank = self.accounts[self.account_numbers[user]]
        amount_owed = 0
        if amount_in_bank >= 0:
            amount_owed = 0
        else:
            amount_owed += amount_in_bank/100
        length_of_history = len(transactions)
        num_inquiries = 0
        for transaction in transactions:
            if transaction['type'] == "hard_inquiry":
                num_inquiries += 1
        new_credit = -num_inquiries
        type_of_credit = 1  # number of banks
        credit = 0.35 * payment_history + 0.3 * amount_owed + 0.15 * length_of_history + 0.1 * new_credit + 0.1 * type_of_credit
        print("Computing credit using {}'s history of payment_history: {}, amount_owed: {}, length_of_history: {}, new_credit: {}, type_of_credit: {}".format(user, payment_history, amount_owed, length_of_history, new_credit, type_of_credit))
        print("{}'s computed credit: {}, ".format(user, credit))
        scaled_credit = min(max((credit+3) * 100, 400), 750)

        return scaled_credit

    def record_transaction(self, address, source, destination, value, pub_key):
        transaction = Transaction(source, destination, "transaction", value)
        self.blockchain.add_block_transaction(address, transaction, pub_key)
        if DEBUG:
            print("Transaction of {} dollars from {} to {} recorded in blockchain database".format(value, source, destination))

    def record_derogatory(self, user):
        transaction = Transaction(user.address, user.address, 0, "derogatory_mark")
        self.blockchain.add_block_transaction(user.address, transaction, user.public_key)
        if DEBUG:
            print("Derogatory mark recorded for {} in blockchain database".format(user))

    def record_inquiry(self, user):
        transaction = Transaction(user.address, user.address, 0, "hard_inquiry")
        self.blockchain.add_block_transaction(user.address, transaction, user.public_key)
        if DEBUG:
            print("Hard inquiry recorded for {} in blockchain database".format(user))

    def __str__(self):
        return self.name

class User:
    def __init__(self, name, ssn, bank):
        self.name = name
        self.bank = bank
        self.ssn = ssn
        self.address = self.bank.get_hashed_address(self)
        self.bank_account = bank.register_user(self)
        self.private_key = RSA.generate(2048)
        self.public_key = self.private_key.publickey()

    def decrypt_please(self, enc_transactions):
        cipher_rsa = PKCS1_OAEP.new(self.private_key)
        if DEBUG:
            print("{} decrypted their transactions using their secret private key".format(self))
        decrypted = [cipher_rsa.decrypt(enc_transaction).decode() for enc_transaction in enc_transactions]
        return decrypted

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
        self.bank.record_transaction(user.address, source, destination, price, user.public_key)
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

    BankOfAmerica.record_inquiry(AspiringProgrammer)
    BankOfAmerica.record_derogatory(AspiringProgrammer)

    PapaJohns.record_purchase(AspiringProgrammer, "big_pizza")
    WalMart.record_purchase(AspiringProgrammer, "desk")

    print(Near.hire(AspiringProgrammer))

if __name__ == "__main__":
    main()