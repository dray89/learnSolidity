from brownie import accounts, network, config

FORKED_LOCAL_ENVIRONMENTS = ['mainnet-fork', 'mainnet-fork-dev']
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ['development', 'ganache-local']
OPENSEA_URL = "https://testnets.opensea.io/ASSETS/{}/{}"
BREED_MAPPING = {0: "PUG", 1: "SHIBA_INU", 2: "ST_BERNARD"}

contract_to_mock = {
    'vrf_coordinator': VRFCoordinatorMock,
    'link_token': LinkToken
}


def get_account(index=None, id=None): 
    #accounts[0]
    # accounts.add("env")
    # accounts.load('id')
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or network.show_active() in FORKED_LOCAL_ENVIRONMENTS
    ):
        return accounts[0]
    
    return accounts.add(config['wallets']['from_key'])


def get_contract(contract_name):
    """ 
    This function will grab contract addresses from brownie config if defined
    otherwise it will deploy a mock version of that contract and return that mock contract

    args:
    contract_name: string

    Returns: 
        brownie.network.contract.ProjectContract: The most recently deployed version of this contract
    """
    contract_type  = contract_to_mock[contract_name]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        if len(contract_type) <=0:
            #how many mockv3aggregators has been deployed
            deploy_mocks()
        contract = contract_type[-1]
        #mockv3aggregator[-1]
    else:
        contract_address = config['networks'][network.show_active()][contract_name]
        #address , abi 
        contract = Contract.from_abi(contract_type._name, contract_address, contract_type.abi)
    return contract 

DECIMALS = 8
INITIAL_VALUE = 200000000

def deploy_mocks(decimals=DECIMALS, initial_value=INITIAL_VALUE):
    account = get_account()
    MockV3Aggregator.deploy(decimals, initial_value, {'from': account})
    link_token = LinkToken.deploy({'from':account})
    VRFCoordinatorMock.deploy(link_token.address, {'from':account})
    print('deployed')

def fund_with_link(contract_address, account=None, link_token=None, amount=100000000000000000):
    account = account if account else get_account()
    link_token = link_token if link_token else get_contract('link_token')
    tx = link_token.transfer(contract_address, amount, {'from':account})
    #link_token_contract = interface.LinkTokenInterface(link_token.address)
    #tx = link_token_contract.transfer(contract_address, amount, {'from':account})
    tx.wait(1)
    print('fund contract')
    return tx

def get_breed():
    return BREED_MAPPING[breed_number]
    