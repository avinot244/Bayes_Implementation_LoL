splitList = [90,540,1491]
toSplit = [0, 50, 90, 250, 540, 1200]
print(toSplit)
temp = [[] for _ in range(len(splitList))]
res = list()

for snapShotTime in toSplit:
    for i in range(len(splitList)):
        print(temp)
        if snapShotTime < splitList[i]:
            temp[i].append(snapShotTime)
            break
        

print(temp)