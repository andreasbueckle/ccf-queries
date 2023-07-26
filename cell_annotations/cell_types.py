import json
import csv
from utils import get_data

# URL to Entity API and CCF API endpoints
CCF_API = "http://grlc.io/api-git/hubmapconsortium/ccf-grlc/subdir/ccf//cells_located_in_as?endpoint=https%3A%2F%2Fccf-api.hubmapconsortium.org%2Fv1%2Fsparql?format=application/json"

# dict for CCF API response with all AS-CT pairings
as_ct_all = {}

# a dictionary with all unique cell types and counts for them
result = {}


def main():
    """A method to identify all cell types in the ASCT+B Tables and count unique ontologies
    This method uses the endpoint at http://grlc.io/api-git/hubmapconsortium/ccf-grlc/subdir/ccf//cells_located_in_as?endpoint=https%3A%2F%2Fccf-api.hubmapconsortium.org%2Fv1%2Fsparql?format=application/json to run a SPARQL query to obtain all cell types associated with all anatomical structures
    """
    # make initial API call to get all AS-CT connections
    as_ct_all = get_data(CCF_API)

    # A list of sources for cell type IDs
    prefixes = ["https://purl.org/ccf/", "http://purl.obolibrary.org/obo/"]

    # pre-fill dict to capture counts ID source
    for source in prefixes:
        result[source] = 0

    # get unique cell types
    unique_cell_types = set()
    for pairs in as_ct_all:
        current = pairs['cell_iri']
        print(current)
        unique_cell_types.add(current)

        # get counts
    for id in unique_cell_types:
        for source in prefixes:
            if source in id:
                result[source] = result[source] + 1

    # export the counts to JSON
    with open('counts.json', 'w') as f:
        json.dump(result, f)

    # export the unique CTs to CSV
    with open('unique_cell_types.csv', 'w', newline='') as f:
        wr = csv.writer(f, delimiter=',')
        wr.writerow(["cell_type"])
        for item in unique_cell_types:
            print(item)
            wr.writerow([item])


# driver code
if __name__ == "__main__":
    main()
