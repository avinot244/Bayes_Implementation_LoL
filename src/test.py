from AreaMapping.AreaMapping import AreaMapping
from utils_stuff.Position import Position
from utils_stuff.plotsZone import *
from utils_stuff.globals import *
from utils_stuff.utils_func import *
from utils_stuff.Computation.computation import centralSymmetry
import os


rootdir = "../data/JDGvsT1/g1"
summaryData = getSummaryData(rootdir)
data = SeparatedData(rootdir + "/Separated")
gameDuration = summaryData.gameDuration
begGameTime = data.begGameTime
endGameTime = data.endGameTime
splitList = [90, 300, 900, 1200, 1300, gameDuration]

splittedDataset : list[SeparatedData] = data.splitData(gameDuration, splitList)
mappingDataList : list[AreaMapping] = list()

for split in splittedDataset:
    mappingDataTemp = AreaMapping()
    mappingDataTemp.computeMapping(split)
    mappingDataList.append(mappingDataTemp)

for mappingData in mappingDataList:
    print(mappingData.teamOneMapping)
    print("\n=======================")