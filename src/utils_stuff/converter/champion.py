from API.DDragon.api_calls import get_champion_mapping_key

def convertToChampionName(id : int):
    if id > 0:
        return get_champion_mapping_key()[id]
    else:
        return None