import random
from MakeMerkleTree import merkle
import json
from hashlib import sha256
from flask import Flask, jsonify, request
import requests as req
from flask import Flask, jsonify, request
from http.server import BaseHTTPRequestHandler, HTTPServer
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from blockchain import Blockchain
from company_demo import Bank, Company, User, Shop, PAPAJOHNS, WALMART

app = Flask(__name__)

BankOfAmerica = Bank("BankOfAmerica")

Near = Company(name="Near", hiring_threshold=700, bank=BankOfAmerica)
AspiringProgrammer = User(name="Yoav Rafalin", ssn="123456", bank=BankOfAmerica)#"123 Electric Ave")

PapaJohns = Shop("Papa John's", PAPAJOHNS, BankOfAmerica)
WalMart = Shop("Walmart", WALMART, BankOfAmerica)

# Run sample transactions
PapaJohns.record_purchase(AspiringProgrammer, "small_pizza")
WalMart.record_purchase(AspiringProgrammer, "bike")

BankOfAmerica.record_inquiry(AspiringProgrammer)
BankOfAmerica.record_derogatory(AspiringProgrammer)

PapaJohns.record_purchase(AspiringProgrammer, "big_pizza")
WalMart.record_purchase(AspiringProgrammer, "desk")

@app.route('/latest_hash', methods=['GET'])
def get_latest_hash():
    return BankOfAmerica.blockchain.blocks[BankOfAmerica.blockchain.blocknum-1]["hash"]

@app.route('/blockchain', methods=['GET'])
def get_blockchain():
    temp = str([b for b in BankOfAmerica.blockchain.blocks])[1:-1].replace("'", '"')
    return temp

@app.route('/add_block', methods=['POST'])
def recv_block():
    values = request.get_json()
    ssn = values["ssn"]
    name = values["name"]
    transaction = Transaction(values["transaction"]["src"], values["transaction"]["dest"], values["transaction"]["tx_type"], values["transaction"]["tx_value"])
    BankOfAmerica.blockchain.add_block_transaction(get_hashed_address(ssn, name), transaction, BankOfAmerica.registered_users[values['name']].public_key) # TODO: CHANGE THIS rand_pub_key()
    return "complete\n" + str(blockchain.blocks[blockchain.blocknum-1])
    
@app.route('/get_credit_score', methods=["POST"])
def send_credit_score():
    values = request.get_json()
    ssn = values["ssn"]
    name = values["name"]
    private_key = values["private_key"]
    return str(BankOfAmerica.get_credit(BankOfAmerica.registered_users[values['name']]))


if(__name__ == "__main__"):
    app.run(host='10.1.128.115', port=8086)

    print(Near.hire(AspiringProgrammer))