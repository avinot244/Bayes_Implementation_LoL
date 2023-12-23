from API.DDragon.api_calls import get_champion_mapping_key

def convertToChampionName(id : int):
    return get_champion_mapping_key()[id]