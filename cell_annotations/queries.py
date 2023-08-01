import json
import csv
from utils import get_data

# URL to Entity API and CCF API endpoints
CCF_API = "http://grlc.io/api-git/hubmapconsortium/ccf-grlc/subdir/ccf//cells_located_in_as?endpoint=https%3A%2F%2Fccf-api.hubmapconsortium.org%2Fv1%2Fsparql?format=application/json"
ENTITY_API_ENTITIES = "https://entity.api.hubmapconsortium.org/entities/"
ENTITY_API_ANCESTORS = "https://entity.api.hubmapconsortium.org/ancestors/"

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
            "cell_types": [],
            "assay_type": "",
            "assay_type_description": "",
            "donor_metadata": {
                "sex": "",
                "age": "",
                "race": ""
            }
        }

    # use Entity API to get netadata given a HuBMAP ID
    for key in result:
        data = get_data(ENTITY_API_ENTITIES+key)

        # get assay type and description
        result[key]['assay_type'] = data['direct_ancestors'][0]['ingest_metadata']['metadata']['assay_type']
        try:
            result[key]['assay_type_description'] = data['direct_ancestors'][0]['ingest_metadata']['metadata']['description']
        except:
            result[key]['assay_type_description'] = "no description provided"

        # get donor metadata
        donor_reponse = get_data(ENTITY_API_ANCESTORS+key)
        for entity in donor_reponse:
            if entity['entity_type'] == "Donor":
                # there are organ_donor_data and living_donor_data, and we cannot predict which donor has which
                try:
                    for data_block in entity['metadata']['organ_donor_data']:
                        # now we use our retrieve_donor_fields method to fill in the values for the keys in our donot_metadata dict
                        retrieve_donor_fields(data_block, key, 'sex', 'Sex')
                        retrieve_donor_fields(data_block, key, 'age', 'Age')
                        retrieve_donor_fields(data_block, key, 'race', 'Race')
                except:
                    for data_block in entity['metadata']['living_donor_data']:
                        retrieve_donor_fields(data_block, key, 'sex', 'Sex')
                        retrieve_donor_fields(data_block, key, 'age', 'Age')
                        retrieve_donor_fields(data_block, key, 'race', 'Race')

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


def retrieve_donor_fields(block, key, term_used_by_result_dict, term_used_by_entity_api):
    """A function to fill in the metadata for the donor in the final result dict

    Args:
        block (dict): A donor metadata block
        key (string): Dataset HuBMAP ID
        term_used_by_result_dict (string): a demographic term (in result dict)
        term_used_by_entity_api (string): a demographic term (in reponse from Entity API)
    """
    if block['grouping_concept_preferred_term'] == term_used_by_entity_api:
        if block['grouping_concept_preferred_term'] == "Age":
            result[key]['donor_metadata'][term_used_by_result_dict] = block['data_value']
        else:
            result[key]['donor_metadata'][term_used_by_result_dict] = block['preferred_term']


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
            one_up = get_data(ENTITY_API_ENTITIES+ancestor['hubmap_id'])
            # and try your luck there
            find_rui_location(one_up, DATASET_ID)


# driver code
if __name__ == "__main__":
    main()
