from lib2to3.pgen2 import token
from brownie import AdvancedCollectible
from scripts.helpful_scripts import get_breed
from metadata.sample_metadata import metadata_template
from pathlib import Path
import requests
import json

def main():
    advanced_collectible = AdvancedCollectible[-1]
    number_of_advanced_collectibles = advanced_collectible.tokenCounter()
    print(f"You have created {number_of_advanced_collectibles} collectibles!")
    for token_id in range(number_of_advanced_collectibles):
        breed = get_breed(advanced_collectible.tokenToBreed(token_id))
        metadata_file_name = f"./metadata/{network.show_active()}/{token_id}-{breed}.json"
    collectible_metdata = metadata_template
    if Path(metadata_file_name).exists():
        print("it already exists!")
    else:
        print(f"creating metadata file: {metadata_file_name}")
        collectible_metadata["name"] = breed
        collectible_metadata["description"] = f"An adorable {breed} pup!"
        print(collectible_metdata)
        image_path = "./img/" + breed.lower().replace("_", "-") + ".png"
        image_uri = upload_to_ipfs()
        collectible_metdata['image'] = image_uri
        with open(metadata_file_name, "w") as file:
            json.dump(collectible_metdata, file)
        upload_to_ipfs(metadata_file_name)

def upload_to_ipfs(filepath):
    with Path(filepath).open("rb") as fp:
        image_binary = fp.read()
        ipfs_url = "https://127.0.0.1:5001"
        endpoint = '/api/v0/add'
        response = requests.post(ipfs_url + endpoint, files={"file":image_binary})
        ipfs_hash = response.json()['Hash']
        filename = filepath.split("/")[-1:][0]
        image_uri = f"https:ipfs.io/ipfs/{ipfs_hash}?filename={filename}"
        return image_uri
