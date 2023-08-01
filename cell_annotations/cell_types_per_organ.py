import json
import csv


def main():
    """A function to count cells by CT ontology/source per organ
    """
    # load json file with ASCT+ table data as JSON file
    with open('data/ccf-asctb-all.json') as f:
        all = json.load(f)

    # the dict we will be outputting at the end
    result = {}

    # loop through ASCT+B dictionaries for all organs
    for organ in all:
        result[organ] = {
            # set to capture unique CTs
            'source_counts': {},
            'unique_cell_types': []
        }

        for rows in all[organ]['data']:
            for cell_type in rows['cell_types']:
                # if unmapped, we use the cell_name (because id will be empty)
                if cell_type['id'] != "":
                    if cell_type['id'] not in result[organ]['unique_cell_types']:
                        result[organ]['unique_cell_types'].append(
                            cell_type['id'])
                else:
                    if cell_type['name'] not in result[organ]['unique_cell_types']:
                        result[organ]['unique_cell_types'].append(
                            ":"+cell_type['name'])

        # get counts for source instances
        result[organ]['source_counts'] = get_unique_sources(
            result[organ]['unique_cell_types'])

    # export the counts to JSON
    with open('output/counts_per_organ_per_source.json', 'w') as f:
        json.dump(result, f)

    # export the coounts to CSV
    with open('output/counts_per_organ_per_source.csv', 'w', newline='') as f:
        wr = csv.writer(f, delimiter=',')
        # write headers (organ and number of unmapped CTs)
        headers = ['organ', 'not_mapped']
        wr.writerow(headers)

        # iterate thruough result dict and write values to csv
        for organ in result:
            row = [organ]
            if "NOT_MAPPED" in result[organ]['source_counts']:
                row.append(result[organ]['source_counts']['NOT_MAPPED'])
            else:
                row.append("0")
            wr.writerow(row)


def get_unique_sources(cell_type_set):
    """A function to isolate unique sources given a set of cel type ID

    Args:
        cell_type_set (set): A set of cell types

    Returns:
        dict: s source count dictionary
    """
    # create a duct to capture source counts
    sources = {}
    for element in cell_type_set:
        # isolate prefix
        prefix = element.split(":")[0]
        if prefix == "":
            prefix = "NOT_MAPPED"
        # counts prefix instances
        if prefix not in sources:
            sources[prefix] = 1
        else:
            sources[prefix] = sources[prefix]+1
    return sources


# driver code
if __name__ == "__main__":
    main()
