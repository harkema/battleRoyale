#!/usr/bin/python3

import overseer
import random
import numpy
import os

class Match(object):
    def __init__(self):
        #Stores players remaining in the battle
        self.allPlayersList = []
        #Temporarily stores the tuple (containg player info) that has been converted to this list
        self.tempPlayerList = []

        self.strengthScenarios = [" was hit with a stick by  ", " was pushed down a mountain by ", " was punched in the nose by ", " was kicked in the shins ", " strangled by " ]
        self.dexterityScenarios  = [" fell into a river while following ", " failed to dodge a rock thrown by  ", " fell out of a tree after the branch was broken by  "]
        self.intelligenceScenarios = [" ate toxic berries left by ", " was set on fire by ", " slept through a surprise attack from "]
        self.charismaScenarios = [" was beaten up by a new gang led by " , " cried after being yelled at by ", " was stabbed in the back (literally and metaphorically) by ", " was attacked by a wolf who was befriended by "  ]

        self.allScenarios=[]
        self.allScenarios.append(self.strengthScenarios)
        self.allScenarios.append(self.dexterityScenarios)
        self.allScenarios.append(self.intelligenceScenarios)
        self.allScenarios.append(self.charismaScenarios)

        #Tracks number of kills by each player
        self.playerKillsDict={}

        self.itemsDict={}

        #Items that players can pick up
        self.itemsDict["helmet"] = "strength"
        self.itemsDict["protein shake"] = "strength"
        self.itemsDict["shield"] = "strength"

        self.itemsDict["dagger"] = "dexterity"
        self.itemsDict["running shoes"] = "dexterity"
        self.itemsDict["energy drink"] = "dexterity"

        self.itemsDict["leather jacket"] = "charisma"
        self.itemsDict["sunglasses"] = "charisma"
        self.itemsDict["breath mint"] = "charisma"

        self.itemsDict["map"] = "intelligence"
        self.itemsDict["book"] = "intelligence"
        self.itemsDict["glasses"] = "intelligence"


    def storePlayerInfo(self):
        """
        Exports the players and their information to a list format (list of tuples w/ each tuple containing each players' information)
        """

        #overseer.BattleRoyale().connectDB()
        #Gets all information from the database
        self.allPlayers = overseer.BattleRoyale().retrievePlayerInfo()

        #For each tuple within the overall table tuple, it is converted into a list
        #and added to a list off all players and their attributes
        for tup in list(self.allPlayers):
            self.tempPlayerList = list(tup)
            self.allPlayersList.append(self.tempPlayerList)

        #Initializes kill count and hits taken to 0
        for player in self.allPlayersList:
            self.playerKillsDict[player[1]] = 0



        return len(self.allPlayersList)

    def movePlayer(self, player):
        """
        Moves the player to a new location on the map. Checks for items players can pick up at this new locations

        Input: player (int, str, int ...)
        """
        playerRow = random.randint(0, 10)
        playerCol = random.randint(0, 10)



        print("%s ran away\n" % player[1])

        #Sees if position the player ran to contains an item
        if self.map[playerRow][playerCol] in self.itemsDict.keys():
            #Checks what attribute the item increases
            if self.itemsDict[self.map[playerRow][playerCol]] == "strength":
                player[2]=player[2]+2
                print("%s picked up the %s" % (player[1], self.map[playerRow][playerCol]))

            elif self.itemsDict[self.map[playerRow][playerCol]] == "charisma":
                player[3]=player[3]+2
                print("%s picked up the %s" % (player[1], self.map[playerRow][playerCol]))

            elif self.itemsDict[self.map[playerRow][playerCol]] == "intelligence":
                player[4]=player[4]+2
                print("%s picked up the %s" % (player[1], self.map[playerRow][playerCol]))

            else:
                player[5]=player[5]+2
                print("%s picked up the %s" % (player[1], self.map[playerRow][playerCol]))

    def addItems(self):
        """
        Randomly generates location for the items to be placed at
        """
        for item, itemType in self.itemsDict.items():
            itemRow=0
            itemCol=0

            while self.map[itemRow][itemCol] != " " :
                itemRow = random.randint(0, 10)
                itemCol = random.randint(0, 10)


            self.map[itemRow][itemCol] = item


    def battleCycle(self):

        #Tracks number of hits each player takes in a given round
        self.hitsTakenDict={}

        #Creates initital matchups
        self.generateMatchUps()

        #Documents who kills who
        self.killedByDict = {}

        #Matrix represented by a 2D List (10 x 10)
        self.map = numpy.full((11,11), " ", dtype=object)

        self.addItems()

        for pair in self.allPairings:
            self.hitsTakenDict[pair[0][1]] = 0
            self.hitsTakenDict[pair[1][1]] = 1

        #Assigns scenarios to each pair until one player takes 3 hits (dead)
        for pair in self.allPairings:
            self.usedScenarios=[]

            while not self.isDead(pair[0][1]) and not self.isDead(pair[1][1]):
                self.scenarioGenerator(pair)
                self.determineWinner(pair)

        #Returns players remaining
        return len(self.allPlayersList)

    def eliminate(self, playerName):
        """
        Removes player from entire player list once they have been eliminated from the battle royale

        Input: playerName <str>
        """
        for index, player in enumerate(self.allPlayersList):
            if player[1] == playerName:
                del self.allPlayersList[index]
                break


    def determineWinner(self, pair):
        """
        Determines which player wins in each matchup based upon the attribute associated with each scenario

        Input: pair[[<int>, <str>, <int>...], [<int>, <str>, <int>...]]
        """

        #Check if both players have same attribute distribution - move players until one picks up an item
        if(pair[0][2] == pair[1][2] and pair[0][3] == pair[1][3] and pair[0][4] == pair[1][4] and pair[0][5] == pair[1][5]):
            while (pair[0][2] == pair[1][2] and pair[0][3] == pair[1][3] and pair[0][4] == pair[1][4] and pair[0][5] == pair[1][5]):
                movementNum = random.randint(1,2)
                if movementNum == 1:
                    self.movePlayer(pair[0])
                    print("%s followed %s" % (pair[1][1], pair[0][1]))
                else:
                    self.movePlayer(pair[1])
                    print("%s followed %s" % (pair[1][1], pair[0][1]))

        ##############
        #Strength
        ##############
        #Checks what category the assigned scenario is in
        #Based on the category, attribute points are compared to determine winner
        if self.scenario in self.strengthScenarios:
            #Comparing category attribute points
            if pair[0][2] > pair[1][2]:
                print("%s %s %s" % (pair[1][1], self.scenario, pair[0][1]))
                #Increases loser's hits taken
                self.hitsTakenDict[pair[1][1]]=self.hitsTakenDict[pair[1][1]]+1

                #If player has taken 3 hits, their killer is documented and they are eliminated from the players list
                if self.isDead(pair[1][1]):
                    self.killedByDict[pair[1][1]] = pair[0][1]
                    self.eliminate(pair[1][1])
                    self.playerKillsDict[pair[0][1]] = self.playerKillsDict[pair[0][1]] + 1
                #Continues to assign scenarios until a player has taken 3 hits
                else:
                    if(self.hitsTakenDict[pair[1][1]] == 2):
                        self.movePlayer(pair[1])

                    self.scenarioGenerator(pair[1])
            #Case in which attribute points are the same between players
            elif pair[0][2] == pair[1][2]:
                print("%s and %s are in a close battle!" % (pair[0][1], pair[1][1]))
                self.scenarioGenerator(pair)

            else:
                print("%s %s %s" % (pair[0][1], self.scenario, pair[1][1]))
                self.hitsTakenDict[pair[0][1]]=self.hitsTakenDict[pair[0][1]]+1


                if self.isDead(pair[0][1]):
                    self.killedByDict[pair[0][1]] = pair[1][1]
                    self.eliminate(pair[0][1])
                    self.playerKillsDict[pair[1][1]] = self.playerKillsDict[pair[1][1]] + 1

                else:
                    if(self.hitsTakenDict[pair[0][1]] == 2):
                        self.movePlayer(pair[0])

                    self.scenarioGenerator(pair)

        ##############
        #Dexterity
        ##############
        elif self.scenario in self.dexterityScenarios:
            if pair[0][5] > pair[1][5]:
                print("%s %s %s" %(pair[1][1],  self.scenario, pair[0][1]))
                self.hitsTakenDict[pair[1][1]]=self.hitsTakenDict[pair[1][1]]+1


                if self.isDead(pair[1][1]):
                    self.killedByDict[pair[1][1]] = pair[0][1]
                    self.eliminate(pair[1][1])
                    self.playerKillsDict[pair[0][1]] = self.playerKillsDict[pair[0][1]] + 1

                else:
                    if(self.hitsTakenDict[pair[1][1]] == 2):
                        self.movePlayer(pair[1])

                    self.scenarioGenerator(pair)

            elif pair[0][5] == pair[1][5]:
                print("%s and %s are in a close battle!" % (pair[0][1], pair[1][1]))
                self.scenarioGenerator(pair)

            else:
                print("%s %s %s" % (pair[0][1], self.scenario, pair[1][1]))
                self.hitsTakenDict[pair[0][1]]=self.hitsTakenDict[pair[0][1]]+1


                if self.isDead(pair[0][1]):
                    self.killedByDict[pair[0][1]] = pair[1][1]
                    self.eliminate(pair[0][1])
                    self.playerKillsDict[pair[1][1]] = self.playerKillsDict[pair[1][1]] + 1

                else:
                    if(self.hitsTakenDict[pair[0][1]] == 2):
                        self.movePlayer(pair[0])

                    self.scenarioGenerator(pair)

        ##############
        #Intelligence
        ##############
        elif self.scenario in self.intelligenceScenarios:
            if pair[0][4] > pair[1][4]:
                print("%s %s %s" % (pair[1][1], self.scenario, pair[0][1]))
                self.hitsTakenDict[pair[1][1]]=self.hitsTakenDict[pair[1][1]]+1


                if self.isDead(pair[1][1]):
                    self.killedByDict[pair[1][1]] = pair[0][1]
                    self.eliminate(pair[1][1])
                    self.playerKillsDict[pair[0][1]] = self.playerKillsDict[pair[0][1]] + 1

                else:
                    if(self.hitsTakenDict[pair[1][1]] == 2):
                        self.movePlayer(pair[1])

                    self.scenarioGenerator(pair)

            elif pair[0][4] == pair[1][4]:
                print("%s and %s are in a close battle!" % (pair[0][1], pair[1][1]))
                self.scenarioGenerator(pair)

            else:
                print("%s %s %s" % (pair[0][1], self.scenario, pair[1][1]))
                self.hitsTakenDict[pair[0][1]]=self.hitsTakenDict[pair[0][1]]+1


                if self.isDead(pair[0][1]):
                    self.killedByDict[pair[0][1]] = pair[1][1]
                    self.eliminate(pair[0][1])
                    self.playerKillsDict[pair[1][1]] = self.playerKillsDict[pair[1][1]] + 1

                else:
                    if(self.hitsTakenDict[pair[0][1]] == 2):
                        self.movePlayer(pair[0])

                    self.scenarioGenerator(pair)

        ##############
        #Charisma
        ##############
        elif self.scenario in self.charismaScenarios:
            if pair[0][3] > pair[1][3]:
                print("%s %s %s" % (pair[1][1], self.scenario, pair[0][1]))
                self.hitsTakenDict[pair[1][1]]=self.hitsTakenDict[pair[1][1]]+1

                if self.isDead(pair[1][1]):
                    self.killedByDict[pair[1][1]] = pair[0][1]
                    self.eliminate(pair[1][1])
                    self.playerKillsDict[pair[0][1]] = self.playerKillsDict[pair[0][1]] + 1

                else:
                    if(self.hitsTakenDict[pair[1][1]] == 2):
                        self.movePlayer(pair[1])

                    self.scenarioGenerator(pair)

            elif pair[0][3] == pair[1][3]:
                print("%s and %s are in a close battle!" % (pair[0][1], pair[1][1]))
                self.scenarioGenerator(pair)

            else:
                print("%s %s %s" % (pair[0][1], self.scenario, pair[1][1]))
                self.hitsTakenDict[pair[0][1]]=self.hitsTakenDict[pair[0][1]]+1

                if self.isDead(pair[0][1]):
                    self.killedByDict[pair[0][1]] = pair[1][1]
                    self.eliminate(pair[0][1])
                    self.playerKillsDict[pair[1][1]] = self.playerKillsDict[pair[1][1]] + 1

                else:
                    if(self.hitsTakenDict[pair[0][1]] == 2):
                        self.movePlayer(pair[0])

                    self.scenarioGenerator(pair)

    def isDead(self, player):
        if self.hitsTakenDict[player] == 3:
            print("%s has been killed\n" % player)
            return True;
        else:
            return False;



    def scenarioGenerator(self, pair):
        """
        Generates scenarios for a pair to fight in. Randomly assigns a scenario to a pair

        Input: pair[[<int>, <str>, <int> ...x4], [<int>, <str>, <int> ...x4]]
        """
        #Selecting random category of scenarios
        self.attributeTypeNum = random.randint(0, int(len(self.allScenarios))-1)
        self.attributeType = self.allScenarios[self.attributeTypeNum]

        #Selecting random scenario
        self.scenarioNum = random.randint(0, int(len(self.attributeType))-1)
        self.scenario = self.attributeType[self.scenarioNum]


        if self.scenario in self.usedScenarios:
            #Keep generating scenarios until unused scenario is used
            while self.scenario in self.usedScenarios:
                #Case in which all scenarios have been run through
                if(len(self.usedScenarios)) == (len(self.strengthScenarios) + len(self.charismaScenarios) + len(self.intelligenceScenarios) +len(self.dexterityScenarios)):
                    self.usedScenarios = []

                #Selecting random category of scenarios
                self.attributeTypeNum = random.randint(0, int(len(self.allScenarios))-1)
                self.attributeType = self.allScenarios[self.attributeTypeNum]

                #Selecting random scenario
                self.scenarioNum = random.randint(0, int(len(self.attributeType))-1)
                self.scenario = self.attributeType[self.scenarioNum]




        self.usedScenarios.append(self.scenario)



    #Creates battle pairings
    def generateMatchUps(self):
        """
        Randomly assign each player to another player for the initital matchup. Uses a random number generator
        """
        self.assignNumsDict = {}
        self.allPairings = []
        self.usedNums = []


        #if (len(self.allPlayersList)%2 == 0):
        for playerList in self.allPlayersList:

            #If there is an odd number of players, this player stored in the variable automatically proceeds to next round
            if len(self.usedNums) == int(len(self.allPlayersList)/2):
                self.remainingPlayer = playerList
                break

            #Number that is randomly assigned to each player
            assignNum = random.randint(1, (int(len(self.allPlayersList)/2)))

            #Checks and makes sure the number has not been used more than twice
            while assignNum in self.usedNums:
                assignNum = random.randint(1, (int(len(self.allPlayersList)/2)))

            #Pairing is ready to be made
            if assignNum in self.assignNumsDict.values():
                #Get other player name key in dictionary w/ same random num generator
                #Place in tempList
                #Add to dictionary
                tempPairing = []
                tempPairing.append(playerList)

                #Iterates through dictionary and check which player has the matching number
                for playerName, number in self.assignNumsDict.items():
                    if(number == assignNum and playerName != playerList[1]):
                        #Access the player from the entire players list to get access to attribute information
                        for smallerPlayerList in self.allPlayersList:
                            if smallerPlayerList[1] == playerName:
                                tempPlayerList = smallerPlayerList
                                #Appends the matching player's information to the temporary pairing list
                                tempPairing.append(smallerPlayerList)
                                break

                #Appends the pair to the pairings array
                self.allPairings.append(tempPairing)
                #Keeps track of numbers that have already been assigned
                self.usedNums.append(assignNum)

            #Add the number to the list of assigned numbers and wait to pair until the number is randomly generated again
            else:
                self.assignNumsDict[playerList[1]] = assignNum

    def writeRoundResults(self):
        """
        Writes results of each round to file that is immediately sent to the webpage of viewing
        """
        with open("RoundResults.txt", mode="w") as roundResults:
            for killed, killer in self.killedByDict.items():
                roundResults.write(killer + " killed " + killed + "\n")

    def writeBattleResults(self):
        """
        Writes results of the overall battle (total kills) to file
        """

        self.tempKillsDict={}


        with open("Kills.txt", mode="r") as battleResults:
            firstLine = battleResults.readline()

            #If the first line is not empty, the kills need to be temporarily stored and added to the new kill counts
            if firstLine != "":
                firstLine=firstLine.strip()
                lineList=firstLine.split(": ")
                self.tempKillsDict[lineList[0]]=int(lineList[1])

                for line in battleResults.readlines():
                    line=line.strip()
                    lineList=line.split(": ")
                    self.tempKillsDict[lineList[0]]=int(lineList[1])

        with open("Kills.txt", mode="w") as battleResults:
            for killer, kills in self.playerKillsDict.items():
                #Dictionary is empty -> file is empty and kills are being recorded for the first time
                if not self.tempKillsDict:
                    battleResults.write(killer + ": " + str(kills) + "\n")

                #Kills are being added to already existing kill count taken from the previous iteration of the file
                else:
                    #Player exists previously and has not just been added
                    if killer in self.tempKillsDict.keys():
                        battleResults.write(killer + ": " + str(kills + self.tempKillsDict[killer]) + "\n")
                    else:
                        battleResults.write(killer + ": " + str(kills + self.playerKillsDict[killer]) + "\n")




def main():
    matchUps = Match()
    numberOfPlayers = matchUps.storePlayerInfo()
    matchUps.battleCycle()
    matchUps.writeRoundResults()

if(__name__ == "__main__"):
    main()
