from solcx import compile_standard, install_solc
import json 
from web3 import Web3
import os
from dotenv import load_dotenv
load_dotenv()

#"with open" closes automatically
with open("./simpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

#compile solidity

install_solc("0.6.0")

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"simpleStorage.sol": {'content': simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*" : {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.6.0",
)

with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

# get bytecode
bytecode = compiled_sol['contracts']['simpleStorage.sol']["SimpleStorage"]['evm']['bytecode']['object']

# get abi
abi = compiled_sol['contracts']["simpleStorage.sol"]['SimpleStorage']['abi']
#connect to rinkeby
w3 = Web3(Web3.HTTPProvider("https://rinkeby.infura.io/v3/47c38027cd0547abad59d1ab06f6fc3c"))
chain_id = 4
my_address = "0x743455077a8d9A651A0De75E4E4B31221ed045E9"
#bad practice to hard code private key - set env variables in terminal and command lines
private_key = os.getenv("PRIVATE_KEY")
#print(os.getenv("PRIVATE_KEY")*100)
private_key = '0x2b2c3c283bf56227f8a3ed1eddb1d039dd657cefe06696d92383389dfe3fd06a'
#Create the contract in Python
SimpleStorage = w3.eth.contract(abi = abi, bytecode=bytecode)

#Build a transaction
#nonce a word coined for an occassion. every transaction is hashed with a new nonce
#get the latest transaction
nonce = w3.eth.getTransactionCount(my_address) #num of transactions and nonce
#create transaction object
transaction = SimpleStorage.constructor().buildTransaction(
    {"chainId": chain_id, "gasPrice":w3.eth.gas_price, "from": my_address, "nonce": nonce})
#sign
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)

#send 
print("Deploying Contract")
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print("Deployed!!!!")
#working with contract

simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
# on functions ...
# Call - simulate making the call and getting a return value
# transact  - make state change
#print(simple_storage.functions.retrieve().call()) #call
#print(simple_storage.functions.store(15))
print("Updating contract!!!!!!")
store_transaction = simple_storage.functions.store(15).buildTransaction(
    {"chainId": chain_id, "gasPrice":w3.eth.gas_price, "from": my_address, "nonce": nonce + 1}
)
signed_store_txn = w3.eth.account.sign_transaction(store_transaction, private_key=private_key)

send_store_tx = w3.eth.send_raw_transaction(
    signed_store_txn.rawTransaction)

tx_receipt = w3.eth.wait_for_transaction_receipt(send_store_tx)
print("updated!!!!!!!!")
print(simple_storage.functions.retrieve().call())
