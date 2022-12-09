import json
import os

import inquirer

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


questions: tuple = (
    inquirer.List(name='stage', message='What stage you want to deploy?', choices=('dev', 'prod')),
    inquirer.Confirm(name='envs', message='Do you want to modify environment variables?', default=False)
)


@dataclass
class ChangeEnvs:
    envs: bool = False

    @staticmethod
    def __update_config():
        for key, value in environments.items():
            try:
                question = (inquirer.Confirm(name=key, message=f'Do you want to change {key}?', default=False),)
                if inquirer.prompt(question)[key]:
                    question = (inquirer.Text(name=key, message=f'New value for {key}', default=value),)
                    environments[key] = inquirer.prompt(question)[key]
            except KeyError:
                print('Cancelled by user')
                exit(1)

    def __call__(self, *args, **kwargs):
        if self.envs:
            self.__update_config()


if __name__ == '__main__':
    answers: dict = inquirer.prompt(questions)
    if not answers:
        exit(1)
    ChangeEnvs(envs=answers['envs'])()
    Deploy(stage=answers.get('stage'))()
