from brownie import SimpleStorage, accounts, config

def read_contract():
    simple_storage = SimpleStorage[-1] 
    print(simple_storage)
    #abi already has it saved in deployments and in json file
    #address
    #print(SimpleStorage.retrieve())

def main():
    read_contract()
