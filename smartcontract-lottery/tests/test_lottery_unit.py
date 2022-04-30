from brownie import Lottery, accounts, config, network, exceptions
from web3 import Web3
from scripts.deploy_lottery import deploy_lottery
import pytest 
from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account, fund_with_link

def test_get_entrance_fee():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    # arrange
    lottery = deploy_lottery()
    #act
    expected_entrance_fee = Web3.toWei(0.025, 'ether')
    entrance_fee = lottery.getEntranceFee()
    #assert

def test_cant_enter_unless_started():
    #arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    #act
    lottery = deploy_lottery()
    #assert
    with pytest.raises(exceptions.VirtualMachineError):
        lottery.enter({"from":get_account(), 'value':lottery.getEntranceFee()})

def test_can_start_and_enter_lottery():
        #arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({'from':account})
    #act
    lottery.enter({'from':account, 'value':lottery.getEntranceFee()})
    #assert
    assert lottery.players(0) == account

def test_can_end_lottery():
        #arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({'from':account})
    lottery.enter({'from':account, 'value':lottery.getEntranceFee()})
    fund_with_link(lottery)
    lottery.endLottery({'from':account})
    assert lottery.lottery_state() == 2

def test_can_pick_winner_correctly():
    #arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({'from':account})
    lottery.enter({'from':account, 'value':lottery.getEntranceFee()})
    lottery.enter({'from':get_account(index=1), 'value':lottery.getEntranceFee()})
    lottery.enter({'from':get_account(index=2), 'value':lottery.getEntranceFee()})
    fund_with_link(lottery)
    transaction = lottery.endLottery({'from':account})
    request_id = transaction.events['RequestedRandomness']['requestId']
    