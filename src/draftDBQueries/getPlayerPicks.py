from YamlParser import YamlParer

import pandas as pd

def getPlayerPicks(summonnerName : str, gameType : str, yamlParser : YamlParer):
    df = pd.read_csv(yamlParser.ymlDict[''])