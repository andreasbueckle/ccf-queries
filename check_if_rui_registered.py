import requests
import json


def main():
    TOKEN = "AggxOzWlzqkwJBMoYrq83V4xJV5llb8kKV5bQabb4yMpljB7v8UJC1WKnykXd6GDv9rwV9B02942YU0dqG3XsM3WQ"
    endpoint = "https://entity.api.hubmapconsortium.org/entities/"
    headers = {"Authorization": "Bearer " + TOKEN}

    obj = []

    file = open("HuBMAP_IDs.csv", "r")

    for line in file:
        if "Kidney" in line.split(",")[2]:
            if "none" not in line.split(",")[4]:
                print("now going for " + line.split(",")[1])
                ancestor_id = requests.get(
                    endpoint + line.split(",")[1], headers=headers).json()["direct_ancestors"][0]["hubmap_id"]
                print("found: " + ancestor_id)
                print()
                rui_location = requests.get(
                    endpoint + ancestor_id, headers=headers).json()["direct_ancestor"]["rui_location"]
                obj.append({
                    "hubmap_id": line.split(",")[1],
                    "type": line.split(",")[2],
                    "ancestor_hubmap_id": ancestor_id,
                    "ccf_annotations": rui_location["ccf_annotations"]
                })
                # print(obj)

    print(obj)
    file.close()

    f = open("is_rui_registered.csv", "a")
    f.write("hubmap_id,type,source_id" + "\n")
    for key in dict:
        data = requests.get(endpoint + key, headers=headers).json()
        # print(key)
        # print(dict[key])
        f.write(key + "," + dict[key].strip() + "," +
                data["direct_ancestors"][0]["hubmap_id"] + "\n")
    f.close()


if __name__ == "__main__":
    main()
