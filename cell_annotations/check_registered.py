import csv
from utils import get_data


def main():
    """A function to check if user-provided datasets with HuBMAP IDs are RUI-registered
    """
    
    ENTITY_API_ENDPOINT = "https://entity.api.hubmapconsortium.org/entities/"
    
    # load CSV
    ids = []
    with open('data/ids.csv', mode ='r') as file:
        csvFile = csv.reader(file)
        for lines in csvFile:
            for id in lines:
                ids.append(id.strip())
            # print(line.strip())

        # initialize output
    result = {}

    # check if IDs are RUI-registered
    for id in ids:
       data = get_data(ENTITY_API_ENDPOINT+id)
       
    #    Add entry to result with default value
       result[id] = False
       find_rui(data, ENTITY_API_ENDPOINT, result, id)
    
    # print the result, could also be exported to CSV
    for key in result:
        print(f'''{key}:{result[key]}''')

        
def find_rui(data, ENTITY_API_ENDPOINT, result, id):
    for ancestor in data["direct_ancestors"]:
    # base case: we arrived at the sample in provenance
        if ancestor['entity_type'] == "Sample":
            # if the sample has a rui_location...
            if "rui_location" in ancestor:
                result[id] = True
        else:
            # if not base case, take the HuBMAP ID of the direct_ancestor...
            one_up = get_data(ENTITY_API_ENDPOINT+ancestor['hubmap_id'])
            # and try your luck there
            find_rui(one_up, id, result, id)
            

# driver code
if __name__ == "__main__":
    main()
