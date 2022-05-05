from lib2to3.pgen2 import token
from brownie import network, AdvancedCollectible
from nft.scripts.helpful_scripts import get_account
from scripts.helpful_scripts import get_breed, get_account

dog_metadata_dic = {}

def main():
    advanced_collectible = AdvancedCollectible[-1]
    number_of_collectibles = advanced_collectible.tokenCounter()
    for token_id in range(number_of_collectibles):
        breed = advanced_collectible.tokenIdToBreed(token_id)
        if not advanced_collectible.tokenURI(token_id).startswith("https://"):
            print(f"setting tokenURI of {token_id}")
            set_tokenURI(token_id, advanced_collectible, dog_metadata_dic[breed])

def set_tokenURI(token_id, nft_contract, tokenURI):
    account = get_account()
    tx = nft_contract.setTokenURI(token_id, _tokenURI, {"from":account}):
    tx.wait(1)
    print(f'you can view your nft at {OPENSEA_URL.format(nft_contract.address, token_id)}')
    print("please wait up to 20 minutes and hit refresh metadata button.")
