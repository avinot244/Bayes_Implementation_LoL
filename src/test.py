from errorHandling import *
from YamlParser import YamlParer

yamlParser : YamlParer = YamlParer("./src/config.yml")

print(checkMatchName(yamlParser, './data'))