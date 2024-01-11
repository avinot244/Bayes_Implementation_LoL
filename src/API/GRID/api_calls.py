import requests
import json
import pandas as pd
import os
import zipfile
import io

from get_token import get_token


def get_last_games(amount : int, gameType : str) -> list[str]:
    assert gameType == "SCRIM" or gameType == "COMPETITIVE" or gameType == "ESPORTS"
    url = "https://api.grid.gg/central-data/graphql"
    body = """
    {
        allSeries(
            first: """ + str(amount) + """,
            filter: { 
                types: """ + str(gameType) + """
            }
            orderBy: ID
            orderDirection: DESC
        ) {
            totalCount
            pageInfo {
                hasPreviousPage
                hasNextPage
                startCursor
                endCursor
            }
            edges {
                node {
                    id
                }
            }
        }
    }
    """
    token = get_token()
    headers = {
        "x-api-key": token
    }
    response = requests.post(url=url,json={"query": body}, headers=headers)
    if response.status_code != 200:
        response.raise_for_status()
    
    result : dict = response.json()
    idList : list = list()
    edges = result["data"]["allSeries"]["edges"]
    for edge in edges:
       idList.append(edge["node"]["id"])
    
    return idList

def get_all_downlaod_links(seriesId):
    url = "https://api.grid.gg/file-download/list/{}".format(seriesId)
    token = get_token()
    headers = {
        "x-api-key": token
    }
    response = requests.get(url=url, headers=headers)
    if response.status_code != 200:
        response.raise_for_status()
    
    result : dict = response.json()
    return result
    
def download(url : str, fileName : str, path : str, fileType : str):
    if not(os.path.exists(path)):
        os.mkdir(path)

    token = get_token()
    headers = {
        "x-api-key": token
    }
    response = requests.get(url=url, headers=headers)
    if response.status_code != 200:
        response.raise_for_status()

    if fileType == "json":
        with open(path + fileName + ".{}".format(fileType), "w") as file:
            json.dump(response.json(), file)
    
    if fileType == "jsonl":
        live_data = response.content.decode('utf-8').splitlines()

        i = 0
        if not(os.path.exists(path + "/Separated")):
            os.mkdir(path + "/Separated/")
        for event in live_data:
            with open(path + "/Separated/" + "{}.json".format(i), "w") as file:
                event_data = json.loads(event)
                json.dump(event_data, file)
            i += 1

    if fileType == "zip":
        z = zipfile.ZipFile(io.BytesIO(response.content))
        z.extractall(path=path + fileName)
        with open(path + fileName + "/" + fileName + ".jsonl", "r") as jsonFile :
            json_list = list(jsonFile)
            i = 0
            for json_str in json_list:
                result = json.loads(json_str)
                with open(path + fileName + "/{}".format(i), "w") as separatedJson:
                    json.dump(result, separatedJson)
                i += 1
            os.remove(path + fileName + "/" + fileName + ".jsonl")


def get_download_link_end_summary(seriesId : str, games : int):
    url = "https://api.grid.gg/file-download/end-state/riot/series/{}/games/{}/summary".format(seriesId, games)
    token = get_token()
    headers = {
        "x-api-key": token
    }
    response = requests.get(url=url, headers=headers)
    if response.status_code != 200:
        response.raise_for_status()
    
    with open("summary_{}_game_{}.json".format(seriesId, games), "w") as file:
        json.dump(response.json(), file)

    


    