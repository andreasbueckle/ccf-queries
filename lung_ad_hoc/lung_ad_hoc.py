import csv
from utils import get_data
import pandas as pd


def main():
    """A function to take a list of HuBMAP IDs and build a CSV file with RUI metadata
    """

    # define global vars
    cols = []
    rows = []

    #  URLs
    ENTITY_API_ENTITIES = "https://entity.api.hubmapconsortium.org/entities/"
    
   # initializing the titles and rows list
    cols = []
    rows = []

    # reading csv file
    with open('data/ids.csv', 'r') as csvfile:
        # creating a csv reader object
        csvreader = csv.reader(csvfile)

        # extracting column headers
        cols = next(csvreader)

        # extracting rows
        for row in csvreader:
            rows.append(row)

    # add extra column headers
    cols.extend(['sample_category', 'is_rui_registered',
                'rui_location_id',])

    # create deata frame to hold result
    d = {}

    # add columns and emoty lists for values
    for c in cols:
        d[c] = []

    # make API calls to get additional metadata
    for row in rows:

        # call Entity API with hubmap_id
        response = get_data(ENTITY_API_ENTITIES+row[0])

        d['sample_id'].append(response['hubmap_id'])
        d['sample_uuid'].append(response['uuid'])
        d['sample_category'].append(response['sample_category'])

        # check if rui registered
        is_rui_registered = "rui_location" in response
        d['is_rui_registered'].append(is_rui_registered)
        if is_rui_registered:
            d['rui_location_id'].append(response['rui_location']['@id'])
        else:
            d['rui_location_id'].append("")

    # export to CSV
    df = pd.DataFrame(data=d)
    df.to_csv("output/sample_registration_status.csv", sep=',')


# driver code
if __name__ == "__main__":
    main()
