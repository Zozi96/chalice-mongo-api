import json
import os

from dataclasses import dataclass

environments: dict = {
    'MONGO_DBNAME': os.getenv('MONGO_DBNAME'),
    'MONGO_HOST': os.getenv('MONGO_HOST'),
    'MONGO_PASSWORD': os.getenv('MONGO_PASSWORD'),
    'MONGO_USERNAME': os.getenv('MONGO_USERNAME'),
    'DEBUG': os.getenv('DEBUG')
}

CONFIG_PATH: str = '.chalice/config.json'


@dataclass
class Deploy:
    stage: str

    def __add_variables(self):
        with open(CONFIG_PATH, 'r') as file_json:
            config: dict = json.load(file_json)
        config['stages'][self.stage]['environment_variables'] = environments
        with open(CONFIG_PATH, 'w') as f:
            json.dump(config, f, indent=2)

    def __remove_variables(self):
        with open(CONFIG_PATH, 'r') as file_json:
            config: dict = json.load(file_json)
            config['stages'][self.stage]['environment_variables'] = {}
        with open(CONFIG_PATH, 'w') as f:
            json.dump(config, f, indent=2)

    def set_config(self):
        self.__add_variables()
        os.system(f'chalice deploy --stage {self.stage}')
        self.__remove_variables()

    def __call__(self, *args, **kwargs):
        self.set_config()


if __name__ == '__main__':
    stage: str = input('Stage: ')
    Deploy(stage)()
