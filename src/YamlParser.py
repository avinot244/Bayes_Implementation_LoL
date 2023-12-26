import yaml

class YamlParser():
    def __init__(self, yaml_path):
        with open(yaml_path, 'r') as file:
            yaml_file = yaml.safe_load(file)
        
        self.ymlDict = yaml_file