from YamlParser import YamlParer

import pandas as pd

def getPlayerPicks(summonerName : str, patch : str, yamlParser : YamlParer):
    df = pd.read_csv(yamlParser.ymlDict['database_path'] + "drafts/draft_player_picks.csv")

    res : dict = dict()
    cpt : int = 0
    for i in df.index:
        if patch != "":
            if df['SummonerName'][i] == summonerName and df['Patch'][i] == patch:
                if df['championName'][i] in res.keys():
                    res[df['championName'][i]] += 1
                else:
                    res[df['championName'][i]] = 1
                cpt += 1
        else:
            if df['SummonerName'][i] == summonerName:
                if df['championName'][i] in res.keys():
                    res[df['championName'][i]] += 1
                else:
                    res[df['championName'][i]] = 1
                cpt += 1
    
    for k, _ in res.items():
        res[k] /= cpt
    
    print(res)