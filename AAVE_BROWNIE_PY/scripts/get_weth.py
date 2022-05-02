from scripts.helpful_scripts import get_account
from brownie import interface, network, config

def get_weth():
    '''
    Mints WETH by depositing ETH.
    '''
    #ABI 
    #address
    account = get_account()
    weth = interface.WethInterface(config['networks'][network.show_active()]["weth_token"])
    tx = weth.deposit({"from":account, 'value': .1 * 10**18})
    tx.wait(1)
    print('received 0.1 WETH')
    return tx

def main():
    get_weth()