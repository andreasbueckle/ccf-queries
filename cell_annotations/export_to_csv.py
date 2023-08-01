import json
import csv


def main():
    """A function to export a dict as a CSV
    """
    # load json file with result dict
    with open('hubmap_id_cell_types.json') as f:
        result = json.load(f)

    # export to csv
    with open('hubmap_id_cell_types.csv', 'w', newline='') as f:
        wr = csv.writer(f, delimiter=',')

        # write headers
        headers = ['hubmap_id', 'assay_type', 'assay_type_description', 'donor_sex', 'donor_age',
                   'donor_race', 'anatomical_structures', 'predicted_cell_types']
        wr.writerow(headers)

        # iterate thruough result dict and write values to csv
        for key in result:
            data = result[key]
            row = []
            row.extend([key, data['assay_type'],
                       data['assay_type_description'], data['donor_metadata']['sex'], data['donor_metadata']['age'], data['donor_metadata']['race'], ';'.join(data['ccf_annotations']), ';'.join(data['cell_types'])])
            wr.writerow(row)


# driver code
if __name__ == "__main__":
    main()
