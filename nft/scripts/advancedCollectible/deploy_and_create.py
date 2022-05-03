from scripts.helpful_scripts import get_account
from brownie import SimpleCollectible

sample_token_URI = "ipfs://Qmd9MCGtdVz2miNumBHDbvj8bigSgTwnr4SbyH6DNnpWdt?filename=0-PUG.json"

def deploy_and_create():
    account = get_account()
    simple_collectible = SimpleCollectible.deploy({'from':account})
    tx = simple_collectible.createCollectible()
    tx.wait(1)
    print(f"awesome. you can view your nft at {OPENSEA_URL.format(simple_collectible.address, simple_collectible.tokenCounter() - 1)}")
    return simple_collectible

def main():
    deploy_and_create()
    