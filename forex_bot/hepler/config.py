import os
import yaml


def config(base_path="config", setting='base_setting.yml') -> dict:
    with open(os.path.join(base_path, setting), 'r') as file:
        documents = yaml.full_load(file)

    return documents
