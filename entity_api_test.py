import requests
import json


def main():
    TOKEN = ""
    endpoint = "https://entity.api.hubmapconsortium.org/entities/"
    headers = {"Authorization": "Bearer " + TOKEN}

    data = requests.get(endpoint, headers=headers).json()
    print(data)


main()