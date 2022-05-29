import os
from typing import Dict, Any
import yaml
import logging

logger = logging.getLogger('config')


class Config(object):

    def __init__(self):
        self.base_dir = os.path.join(os.getcwd(), 'config')
        self.configs: Dict[Any, Any] = {}

    def initialize(self, config_files: list):
        for file in config_files:
            path = os.path.join(self.base_dir, file)
            if os.path.exists(path):
                try:
                    data = yaml.safe_load(open(path, 'r'))
                    if data is not {}:
                        self.configs = {**self.configs, **data}
                except Exception as e:
                    logger.info(f'error while reading file: {path}')
                    logger.error(e)

    def get(self, key):
        return self.configs.get(key, None)
