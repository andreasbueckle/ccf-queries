import requests
import json
import csv
from utils import get_data

# URL to Entity API and CCF API endpoints
CCF_API = "http://grlc.io/api-git/hubmapconsortium/ccf-grlc/subdir/ccf//cells_located_in_as?endpoint=https%3A%2F%2Fccf-api.hubmapconsortium.org%2Fv1%2Fsparql?format=application/json"
ENTITY_API = "https://entity.api.hubmapconsortium.org/entities/"

# dict to hold metadata for each HuBMAP ID
result = {}

# dict for CCF API response with all AS-CT pairings
as_ct_all = {}


def main():
    """A method to identify anatomical structure tags and associated cell types for a set of HuBMAP IDs.
    This method uses the endpoint at http://grlc.io/api-git/hubmapconsortium/ccf-grlc/subdir/ccf//cells_located_in_as?endpoint=https%3A%2F%2Fccf-api.hubmapconsortium.org%2Fv1%2Fsparql?format=application/json to run a SPARQL query to obtain all cell types associated with all anatomical structures
    """
    # make initial API call to get all AS-CT connections
    as_ct_all = get_data(CCF_API)

    # load hubmap_ids.csv
    with open('hubmap_ids.csv', mode='r') as file:

        # reading the CSV file
        csvFile = csv.reader(file)

        # adding all HuBMAP IDs into a set
        ids = set()
        for line in csvFile:
            if line[1] != "x":
                ids.add(line[1])

    # loop through all provided IDs and get metadata
    for id in ids:
        # fill result dict with HuBMAP IDs as keys and add a dict as value for AS tags and cell types
        result[id] = {
            "ccf_annotations": [],
            "cell_types": []
        }

    # use Entity API to get netadata given a HuBMAP ID
    for key in result:
        data = get_data(ENTITY_API+key)
        # use recursive function to "travel up" the provenance graph to check if a parent sample has a rui_location
        find_rui_location(data, key)

    # get cell types for all HuBMAP datasets with AS tags (i.e., that have a rui_location)
    for key in result:
        # initialize an empty list for all found cells
        cells_found = []
        # loop through all the AS tags
        for tag in result[key]["ccf_annotations"]:
            # set a flag to check to denote if an AS tags has been found in an ASCT+B Table
            found_in_asct_b_tables = False
            # loop through all AS-CT pairs in the CCF API response from earlier
            for pairs in as_ct_all:
                # if there is a match between the as_iri and the AS tags...
                if pairs['as_iri'] == tag:
                    # check for duplicates
                    if pairs['cell_iri'] not in cells_found:
                        # then add the cell type associated with the as_iri to the cells_found list
                        cells_found.append(pairs['cell_iri'])
                        # adjust the flag
                        found_in_asct_b_tables = True
            # if no cell types were found for this AS tag, say so
            if found_in_asct_b_tables == False:
                cells_found.append(f"No CTs found for {tag}")
            # finally, assign the list of cell types as value in the dict for AS tags and cell types
            result[key]["cell_types"] = cells_found

    # export the data to JSON
    with open('hubmap_id_cell_types.json', 'w') as f:
        json.dump(result, f)


def find_rui_location(data, DATASET_ID):
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
                # take its ccf_annotations (aka AS Tags) and assign them as value to the "ccf_annotations" key
                result[DATASET_ID]["ccf_annotations"] = ancestor["rui_location"]["ccf_annotations"]
        else:
            # if not base case, take the HuBMAP ID of the direct_ancestor...
            one_up = get_data(ENTITY_API+ancestor['hubmap_id'])
            # and try your luck there
            find_rui_location(one_up, DATASET_ID)


# driver code
if __name__ == "__main__":
    main()
