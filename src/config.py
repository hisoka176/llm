import yaml
import os.path

root_path = os.path.dirname(__file__)


def include(self, node):
    filename = os.path.join(root_path, f'resource/{node.value}')
    if os.path.exists(filename):
        with open(filename, 'r') as fr:
            return yaml.load(fr, Loader=yaml.FullLoader)


yaml.add_constructor('!include', include)


def load_yaml(file_name):
    """Load YAML file to be dict"""
    # config_filepath = os.path.join(root_path, file_name)
    if os.path.exists(file_name):
        with open(file_name, 'r', encoding="utf-8") as fr:
            dict_obj = yaml.load(fr, Loader=yaml.FullLoader)
        return dict_obj
    else:
        raise FileNotFoundError(f'NOT Found YAML file {file_name}')


if __name__ == '__main__':
    data = load_yaml('offline/es/data.yaml')
    print(data)
