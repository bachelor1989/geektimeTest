import os
import yaml


class DataUtil:
    @staticmethod
    def load_yaml(path):
        root_path = os.path.dirname(os.path.dirname(__file__))
        yaml_path = os.path.join(root_path, path)
        with open(yaml_path, 'r', encoding='utf-8') as f:
            env = yaml.safe_load(f)
            return env
