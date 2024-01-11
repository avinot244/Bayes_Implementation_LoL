from api_calls import *

sequenseIdList = get_last_games(10, "SCRIM")
dlDict = get_all_downlaod_links(2619698)

for downloadDict in dlDict['files']:
    fileType = downloadDict["fileName"].split(".")[-1]
    fileName = downloadDict["fileName"].split(".")[0]
    path = "./{}/".format(2619698)
    if fileType != "rofl":
        download(downloadDict['fullURL'], fileName, path, fileType)
