import random

def receive_transaction_data():

def put_on_near():
def get_from_near():

def add_to_blockchain(tx):
    
    
# The structure of a transaction
# encryptions and information each group has access to
# {
# address:
# money_source: (address or bank account)
# money_dest: (address or bank account)
# tx_value: (int)
# debt_to_source: (True/False)
# repayment: (True/False)
# }


class Transaction:
    def __init__(self, address, src, dst, value, debt, repayment):
    self.address = address
    self.money_source = src
    self.money_dest = dst
    self.value = value
    self.debt = debt
    self.repayment = repayment

class Company:
    def __init__(self, hiring_threshold, bank):
        self.hiring_threshold = hiring_threshold
        self.bank = bank
        self.employees = []
    
    def hire(self, user):
        credit = self.bank.getCredit(user)
        if credit >= selfhiring_threshold:
            return True
        

class Bank:
    def __init__(self):
        self.accounts = {}
        

    def hash_user(self, name, address):
        # TODO: hash name and address
        
        return hashed_user

    def register_user(self):
        pass

class User:
    def __init__(self, name, address, bank):
        self.name = name
        self.address = address
        self.bank_account = bank.register_user(self)

class Shop:
    def __init__(self, items):
        self.items = items # dict of items and prices (e.g. {"pizza": 10, "cheese": 3})
        self.bank_account = 

    def pass_tx(self, src, dst, value, debt=False, repayment=False):  # btw, bank accounts are BBBB CCCC CCCC CCCC CCCC
        user_bank = random.
        Transaction

    def record_purchase(self, user, item):
        assert item in self.items
        price = self.items[item]
        src = user.name # address?
        debt, repayment = False, False
        self.pass_tx(user, self, price)

def main():
    Near = Company(hiring_threshold=700)
    AspiringProgrammer = User("Aliaksandr Hudzilin", "123 Electric Ave")
    BankOfAmerica = Bank()

    PapaJohns = Shop()
    WalMart = Shop()

    # Run sample transactions
    PapaJohns.record_purchase(AspiringProgrammer, "pizza")
    WalMart.record_purchase(AspiringProgrammer, "TV")

    Near.hire(AspiringProgrammer)