import requests
import json

def get_data(endpoint):
    """A method to retrieve data from an API endpoint

    Args:
        endpoint (string): The URL of the endpoint
    """
    f = open('access_token.txt', 'r')
    
    # You need a token to get published and unpublished entities from the endpoint. I suggest storing the token in a separate text file and adding it to gitignore
    TOKEN = f.readline()
    headers = {"Authorization": "Bearer " + TOKEN}
    data = requests.get(endpoint, headers=headers).json()
    return data

def find_rui_location(data, dataset_id, ENTITY_API_ENDPOINT):
    """Recursive function to move up the data hierarchy given a hubmap ID to get the RUI location if RUI registered

    Args:
        data (any): de-serialized JSON dict
        DATASET_ID (string): a HuBMAP ID for a dataset (constant)
    """
    for ancestor in data["direct_ancestors"]:
        # base case: we arrived at the sample in provenance
        if ancestor['entity_type'] == "Sample":
            # if the sample has a rui_location...
            if "rui_location" in ancestor:
               return True
        else:
            # if not base case, take the HuBMAP ID of the direct_ancestor...
            one_up = get_data(ENTITY_API_ENDPOINT+ancestor['hubmap_id'])
            # and try your luck there
            find_rui_location(one_up, dataset_id)