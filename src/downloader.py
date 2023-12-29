from YamlParser import YamlParser
from EMH.Summary.SummaryData import SummaryData
from API.Bayes.api_calls import get_games_by_page, save_downloaded_file, get_download_link
from utils_stuff.utils_func import getUnsavedGameNames, replaceMatchName, getSummaryData, getData

import os


def downloadGames(page : int, gameType : str, yamlParser : YamlParser, load : bool):
    patch = yamlParser.ymlDict['patch']
    gameNames : list[str] = get_games_by_page(page, gameType, patch)
    gameNames = getUnsavedGameNames(gameNames, yamlParser.ymlDict['brute_data'])

    # Downloading and saving the json files and updating database
    for gameName in gameNames :
        if not(os.path.exists(yamlParser.ymlDict['brute_data'] + "{}/g1/Separated/".format(gameName))):
            os.makedirs(yamlParser.ymlDict['brute_data'] + "{}/g1/Separated/".format(gameName))

        path = yamlParser.ymlDict['brute_data'] + "{}/g1/".format(gameName)

        # Downloading files
        save_downloaded_file(get_download_link(gameName, "GAMH_DETAILS"), path, gameName, "GAMH_DETAILS")
        save_downloaded_file(get_download_link(gameName, "GAMH_SUMMARY"), path, gameName, "GAMH_SUMMARY")
        save_downloaded_file(get_download_link(gameName, "HISTORIC_BAYES_SEPARATED"), path + "/Separated", gameName, "HISTORIC_BAYES_SEPARATED")

        
        print("Updating yml file")
        yamlParser.ymlDict['match'] = gameName
        replaceMatchName(gameName, "./config.yml")
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
        (data, _, _, _) = getData(load, yamlParser)
        summaryData : SummaryData = getSummaryData(rootdir)

        patch = summaryData.patch

        # Updating database
        print("Saving to database")
        data.draftToCSV(save_path, new, patch)