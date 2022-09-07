import requests
import json


def main():
    TOKEN = ""
    endpoint = "https://entity.api.hubmapconsortium.org/entities/"
    headers = {"Authorization": "Bearer " + TOKEN}

    obj_list = []

    file = open("HuBMAP_IDs.csv", "r")

    for line in file:
        if "Kidney" in line.split(",")[2]:
            if "none" not in line.split(",")[4]:

                ancestor_id = requests.get(
                    endpoint + line.split(",")[1], headers=headers).json()["direct_ancestors"][0]["hubmap_id"]

                contains_renal_pyramid = False

                try:
                    rui_location = requests.get(
                        endpoint + ancestor_id, headers=headers).json()["direct_ancestor"]["rui_location"]
                except:
                    rui_location = {
                        "ccf_annotations": []
                    }
                    print("An exception occurred")
                if "http://purl.obolibrary.org/obo/UBERON_0004200" in rui_location["ccf_annotations"]:
                    contains_renal_pyramid = True
                    print(ancestor_id)                    
                obj_list.append({
                    "hubmap_id": line.split(",")[1],
                    "type": line.split(",")[2],
                    "ancestor_hubmap_id": ancestor_id,
                    "contains_renal_pyramid": contains_renal_pyramid,
                    "rui_location": rui_location
                })

    print(obj_list)
    file.close()

    f = open("is_rui_registered.csv", "w")
    f.write("hubmap_id,ancestor,contains_renal_pyramid" + "\n")
    for obj in obj_list:
        f.write(obj["hubmap_id"] + "," + obj["ancestor_hubmap_id"] 
                + ","
                + str(obj["contains_renal_pyramid"]) + "\n")
        if "@context" in obj["rui_location"]:
            json_object = json.dumps(obj["rui_location"], indent=4)
            with open("rui_locations_hra_preview" + "/" + obj["ancestor_hubmap_id"] + ".json", "w") as outfile:
                outfile.write(json_object)
    f.close()
    # url for renal pyramid: http://purl.obolibrary.org/obo/UBERON_0004200

if __name__ == "__main__":
    main()
