from YamlParser import YamlParser
from EMH.Summary.SummaryData import SummaryData
from Separated.Game.SeparatedData import SeparatedData
from API.Bayes.api_calls import get_games_by_page, save_downloaded_file, get_download_link
from utils_stuff.utils_func import getUnsavedGameNames, replaceMatchName, getSummaryData, getData
from errorHandling import checkTeamComposition
from AreaMapping.AreaMapping import AreaMapping
from Separated.Game.SeparatedData import SeparatedData

import os


def downloadGames(page : int, gameType : str, yamlParser : YamlParser):
    patch = yamlParser.ymlDict['patch']
    gameNames : list[str] = get_games_by_page(page, gameType, patch)
    gameNames = getUnsavedGameNames(gameNames, yamlParser.ymlDict['brute_data'])

    # Downloading and saving the json files and updating database
    for gameName in gameNames :
        if not(os.path.exists(yamlParser.ymlDict['brute_data'] + "{}/Separated/".format(gameName))):
            os.makedirs(yamlParser.ymlDict['brute_data'] + "{}/Separated/".format(gameName))

        path = yamlParser.ymlDict['brute_data'] + "{}/".format(gameName)

        # Downloading files
        save_downloaded_file(get_download_link(gameName, "GAMH_DETAILS"), path, gameName, "GAMH_DETAILS")
        save_downloaded_file(get_download_link(gameName, "GAMH_SUMMARY"), path, gameName, "GAMH_SUMMARY")
        save_downloaded_file(get_download_link(gameName, "HISTORIC_BAYES_SEPARATED"), path + "/Separated", gameName, "HISTORIC_BAYES_SEPARATED")

        
        print("Updating yml file")
        yamlParser.ymlDict['match'] = gameName
        replaceMatchName([gameName], "./config.yml")
        yamlParser = YamlParser("./config.yml")
        # Set upping path for database saving
        if not(os.path.exists("{}/drafts/".format(yamlParser.ymlDict['database_path']))):
            os.mkdir("{}/drafts/".format(yamlParser.ymlDict['database_path']))
        new = False
        if not(os.path.exists("{}/drafts/draft_pick_order.csv".format(yamlParser.ymlDict['database_path']))):
            new = True
        save_path = "{}/drafts/".format(yamlParser.ymlDict['database_path'])

        # Loading data of the game
        rootdir = yamlParser.ymlDict['brute_data'] + "{}/".format(gameName)
        # Getting global info of the game
        (data, _, _, _) = getData(yamlParser, idx=0)
        summaryData : SummaryData = getSummaryData(rootdir)

        patch = summaryData.patch

        # Updating database
        print("Saving to database")
        data.draftToCSV(save_path, new, patch)

def areaMappingRunner(yamlParser : YamlParser, time : int):
    (data, gameDuration, begGameTime, endGameTime) = getData(yamlParser, idx=0)
    areaMapping : AreaMapping = AreaMapping()

    # Splitting our data so we get the interval between [950s; time]
    splitList : list[int] = [120, time, gameDuration]
    splittedDataset : list[SeparatedData] = data.splitData(gameDuration, splitList)
    
    dataBeforeTime : SeparatedData = splittedDataset[1] # Getting the wanted interval
    
    # Computing and displaying results
    areaMapping.computeMapping(dataBeforeTime)

    print("Lane presence for team one at {}:".format(time))
    print(areaMapping.teamOneMapping)
    print("\n------------------\n")
    print("Lane presence for team two at {}:".format(time))
    print(areaMapping.teamTwoMapping)