import requests
import json
from dateutil import parser


def main():
    contest_start_date = "2019-01-01 00:00:00"
    contest_end_date = "2022-10-27 23:59:59"

    # first, let's get the most recent data
    # To get TOKEN for viewing unpublished data, go to EUI, log in, then view source, then copy token from browser
    TOKEN = ""
    endpoint = "https://ccf-api.hubmapconsortium.org/v1/hubmap/rui_locations.jsonld"
    headers = {"Authorization": "Bearer " + TOKEN}
    # data = requests.get(endpoint, headers=headers).json()
    # data = json.load("rui_locations.jsonld")
    
    #load local version of rui_locations.jsonld, copy and pasted from https://ccf-api.hubmapconsortium.org/#/operations/hubmap-rui-locations
    f = open("rui_locations.jsonld")
    data = json.load(f)

    # create empty arrays to capture data
    dates = []
    components = []
    organs = []
    people = []
    tmc_person_pairs = {}
    person_organ_pairs = {}
    unique_users = set()

    for item in data['@graph']:
        for sample in item['samples']:
            # Parse string as datetime object to detemine if in contest range
            as_date_time = parser.parse(
                sample['rui_location']['creation_date'])
            if as_date_time > parser.parse(contest_start_date) and as_date_time < parser.parse(contest_end_date):
                # print(as_date_time)
                # print(sample)
                component = sample['label'].split(',')[2].strip()
                dates.append(as_date_time)
                components.append(component)
                organs.append(sample['rui_location']
                              ['placement']['target'])
                people.append(sample['rui_location']['creator'].strip())
                tmc_person_pairs[sample['label'].split(
                    ',')[2].strip()] = sample['rui_location']['creator'].strip()
                person_organ_pairs[sample['rui_location']['creator'].strip(
                )] = sample['rui_location']['placement']['target']
                
                unique_users.add(sample['rui_location']['creator'].strip().lower())
                  

    # print(tmc_person_pairs)
    # print(person_organ_pairs)
    # print(organs)

    winners = []
    for p in people:
        if p.lower() not in winners:
            winners.append(p.lower())
    # print(winners)

    # count submission per team
    counts = {}
    for item in components:
        if item not in counts:
            counts[item] = 1
        else:
            counts[item] += 1
    # print(counts)

    # now, let's count all the submissions in the contest
    total_submissions = 0
    for item in counts:
        total_submissions += counts[item]
    # print("Total #submissions: " + str(total_submissions))

    # Find out on which dates blocks were submitted
    date_counts = {}
    for item in dates:
        as_string = str(item)[0:10]
        if as_string not in date_counts:
            date_counts[as_string] = 1
        else:
            date_counts[as_string] += 1
    # print(date_counts)

    # find out submissions by organ
    organ_counts = {}
    for item in organs:
        if item not in organ_counts:
            organ_counts[item] = 1
        else:
            organ_counts[item] += 1
    # print(organ_counts)

    # determine unique organ/creator combos (for trophies)
    organ_by_creator = []
    for i in range(0, len(organs)):
        organ_by_creator.append((organs[i], components[i]))
    # print(organ_by_creator)

    unique = []
    for combo in organ_by_creator:
        if combo not in unique:
            unique.append(combo)
    # print(unique)

    print(f'''
person_organ_pairs: { person_organ_pairs}
counts: { counts }
total_submissions: {total_submissions }
date_counts: { date_counts}
unique_users: {unique_users}
number of unique_users: {len(unique_users)}
''')


# driver code
if __name__ == '__main__':
    main()
