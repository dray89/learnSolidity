from brownie import FundMe
from scripts.helpful_scripts import get_account

def fund():
    fund_me = FundMe[-1]
    print(fund_me ,'fund_me')
    print(fund_me.getEntranceFee())
    account = get_account()
    print(account)
    #entrance_fee = fund_me.getEntranceFee()
    #print(entrance_fee)
    #fund_me.fund({"from":account, "value":entrance_fee})

def main():
    fund()