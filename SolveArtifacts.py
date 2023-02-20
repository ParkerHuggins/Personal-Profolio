artifactsFile = open("Artifact_Thing.txt")
lines = artifactsFile.readlines()

#set up lines so that the first 318 entries are all the artifacts in order
lines.pop(0)
lines.pop(0)

#FUNCTIONS
#convert a string of format XeY to a number of X * 10**Y
def scientificStringToNumber(str):
    if str.count('e') == 0:
        return float(str)
    nums = str.split('e')
    x = float(nums[0])
    y = int(nums[1])
    while not x.is_integer():
        x = x * 10
        y = y - 1
    x = int(x)
    return x * (10 ** y)

artifacts = [] #artifacts[n] = [name, power, damage type, slot ID, starting cost]

#populate artifacts table
for line in lines:
    if not line[:1].isdecimal():
        break
    artifactData = line.removesuffix('\n').split('\t')
    artifactData[2] = scientificStringToNumber(artifactData[2])
    artifactData[4] = int(artifactData[4])
    artifactData[5] = scientificStringToNumber(artifactData[5])
    artifacts.append(artifactData[1:6])

equippedArtifacts = [[],[],[],[],[],[],[],[]] #equippedArtifacts[0-7] = [artifactNum, lvl]
nextArtifact = 0
cores = 0

#This buying method takes the current amount of cores, as spends all of them as effectively as possible
def BuyMethod1():
    global nextArtifact
    global cores
    global artifacts
    global equippedArtifacts
    while True:
        #the cost and effeciency of the next buyable artifact
        costOfNext = artifacts[nextArtifact][4] #just base cost
        currentDmg = 1
        currentToReplace = equippedArtifacts[artifacts[nextArtifact][3]]
        if not len(currentToReplace) == 0:
            currentDmg = (1 + artifacts[currentToReplace[0]][1] * currentToReplace[1]) #1 + power * lvl
        effOfNext = (1 + artifacts[nextArtifact][1])/currentDmg/costOfNext #(1 + power)/multInSlot/cost
    
        #the cost and effecinecy of upgrading all the artifacts
        upgradeCostAndEff = [[],[],[],[],[],[],[],[]]
        for index, value in enumerate(equippedArtifacts):
            if not len(value) == 0:
                costOfEquipped = artifacts[value[0]][4] * (1.1 ** value[1]) #base * 1.1^lvl
                effOfEquipped = (artifacts[value[0]][1])/( 1 + artifacts[value[0]][1] * value[1])/costOfEquipped #(power)/(1 + power * lvl)/cost
                upgradeCostAndEff[index] = [costOfEquipped, effOfEquipped]

        #find which upgrade is the most effecient while also remaining affordable
        bestUpgrade = -1
        bestUpgradeEff = 0
        for index, value in enumerate(upgradeCostAndEff):
            if (not len(value) == 0) and (not value[0] > cores) and (value[1] > bestUpgradeEff):
                bestUpgradeEff = value[1]
                bestUpgrade = index

        #if buying is affordable and is the most effecient option
        if costOfNext <= cores and effOfNext > bestUpgradeEff:
            equippedArtifacts[artifacts[nextArtifact][3]] = [nextArtifact, 1]
            nextArtifact = nextArtifact + 1
            cores = cores - costOfNext
        #if there is a previously found best affordable upgrade
        elif bestUpgrade != -1:
            equippedArtifacts[bestUpgrade][1] = equippedArtifacts[bestUpgrade][1] + 1
            cores = cores - upgradeCostAndEff[bestUpgrade][0]
        #if nothing is affordable
        else:
            break

def getMult():
    overallMult = 1
    for value in equippedArtifacts:
        if len(value) == 0:
            continue
        overallMult = overallMult * (1 + artifacts[value[0]][1] * value[1])
    return overallMult



worldMultsFile = open(r"worldMults.txt", "w")

equippedArtifacts = [[],[],[],[],[],[],[],[]] #equippedArtifacts[0-7] = [artifactNum, lvl]
nextArtifact = 0
cores = 0
worldMults = []
SYSTEM = 250
#output code
for world in range(30*SYSTEM):
    cores = cores + (40 * 1.05**world)
    BuyMethod1()
    mult = getMult()
    previousMult = 1
    if not world == 0:
        previousMult = worldMults[world-1]
    worldMults.insert(world, mult)

worldMultsFile.write("system,growth per world\n")
for system in range(SYSTEM):
    firstWorld = worldMults[30*system]
    lastWorld = worldMults[30*system+29]
    overallGrowthPerWorld = (lastWorld/firstWorld) ** (1/30)
    growth = "{},{}\n".format(system+1, overallGrowthPerWorld)
    print("Average growth per world in system {} is {}".format(system+1, overallGrowthPerWorld))
    worldMultsFile.write(growth)

print("Overall all growth across all worlds for {} systems is {}".format(SYSTEM, (worldMults[len(worldMults)-1])**(1/len(worldMults))))
