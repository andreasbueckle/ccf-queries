import csv
import json

def main():

    # capture data from the input file in a data structure (Missing Registration class)
    missing_registrations = []

    with open("data/datasets-without-registered-samples-2-14-2022.tsv") as file:

        tsv_file = csv.reader(file, delimiter="\t")

        for line in tsv_file:
            if "organ.hubmap_id" in line[0]:
                continue
            missing = MissingRegistration(
                line[0], line[1], line[2], line[3], line[4], line[5], line[6], line[7])
            missing_registrations.append(missing)

        names = set()
        for item in missing_registrations:
            names.add(item.organ_created_by_user_email)

        # create dictionary to capture relevant data for output (email, hubmap_id, submission_id)
        missing_registrations_dict = {}
        for item in missing_registrations:
            if item.organ_created_by_user_email in missing_registrations_dict:
                missing_registrations_dict[item.organ_created_by_user_email]["hubmap_id"].append(
                    item.samples_without_location_hubmap_id)
                missing_registrations_dict[item.organ_created_by_user_email]["submission_id"].append(
                    item.samples_without_location_sub_id)
            else:
                missing_registrations_dict[item.organ_created_by_user_email] = {
                    "hubmap_id": [item.samples_without_location_hubmap_id],
                    "submission_id": [item.samples_without_location_sub_id]
                }

    # flatten lists for all creator emails and remove duplicates
    for email in missing_registrations_dict:
        missing_registrations_dict[email]["hubmap_id"] = remove_duplicate(flatten(
            missing_registrations_dict[email]["hubmap_id"]))
        missing_registrations_dict[email]["submission_id"] = remove_duplicate(flatten(
            missing_registrations_dict[email]["submission_id"]))

    # save as json
    json_object = json.dumps(missing_registrations_dict, indent=4)
    with open('output/samples_without_rui_location.json', 'w') as outfile:
        outfile.write(json_object)

    # save as csv
    f = open('output/samples_without_rui_location.csv', 'w', newline='')
    writer = csv.writer(f)
    writer.writerow(["email", "sample_id", "submission_id"])
    for tuple in missing_registrations_dict.items():

        for i in range(0, len(tuple[1]["hubmap_id"])):
            row = [tuple[0], tuple[1]["hubmap_id"]
                   [i], tuple[1]["submission_id"][i]]
            writer.writerow(row)
    f.close()

# utility functions
def remove_duplicate(list):
    """
    A function to remove duplicates in a list
    """
    result = []
    for item in list:
        if item not in result:
            result.append(item)
    return result


def flatten(list):
    """
    A function to flatten nested lists into 1D lists
    """
    result = []
    for l in list:
        if ',' in l:
            temp = l.split(',')
            for item in temp:
                result.append(item.strip("[]"))
        else:
            result.append(l.strip("[]"))
    return result


class MissingRegistration:
    """
    A class to capture data for a missing registration
    """

    def __init__(self, hub_id, organ_sub, sample_sub_id, sample_hub_id, type, dataset_hub_id, org_grp_name, email):
        self.organ_hubmap_id = hub_id
        self.organ_submission_id = organ_sub
        self.samples_without_location_sub_id = sample_sub_id
        self.samples_without_location_hubmap_id = sample_hub_id
        self.sample_types = type
        self.dataset_hubmap_id = dataset_hub_id
        self.organ_group_name = org_grp_name
        self.organ_created_by_user_email = email


# driver code
if __name__ == '__main__':
    main()
