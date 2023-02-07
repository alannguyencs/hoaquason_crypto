import json


def load(json_path):
    with open(json_path) as json_file:
        return json.load(json_file)

def save(json_data, json_path):
    with open(json_path, 'w') as json_file:
        json.dump(json_data, json_file)