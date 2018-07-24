#!/usr/bin/python3

import overseer
import random

class Match(object):
    def __init__(self):
        self.allPlayersList = []
        self.tempPlayerList = []

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

        return len(self.allPlayersList)


    def battleCycle(self):

        self.hitsTakenDict={}
        self.killedByDict = {}

        self.generateMatchUps()

        while(len(self.allPlayersList) != 0):

            if not bool(self.hitsTakenDict):
                self.generateMatchUps()

            for pair in self.allPairings:
                self.hitsTakenDict[pair[0][1]] = 0
                self.hitsTakenDict[pair[1][1]] = 0


            for pair in self.allPairings:
                while not self.isDead(pair[0][1]) and not self.isDead(pair[1][1]):
                    self.scenarioGenerator(pair)
                    self.determineWinner(pair)

            for player in self.allPlayersList:
                print(player, "\n")

            self.writeRoundResults()


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

        if self.scenario in self.strengthScenarios:
            if pair[0][2] > pair[1][2]:
                print("%s %s %s" % (pair[1][1], self.scenario, pair[0][1]))
                self.hitsTakenDict[pair[1][1]]=self.hitsTakenDict[pair[1][1]]+1


                if self.isDead(pair[1][1]):
                    self.killedByDict[pair[1][1]] = pair[0][1]
                    self.eliminate(pair[1][1])

                else:
                    self.scenarioGenerator(pair)


            elif pair[0][2] == pair[1][2]:
                print("Both %s and %s survived!" % (pair[0][1], pair[1][1]))

                self.scenarioGenerator(pair)

            else:
                print("%s %s %s" % (pair[0][1], self.scenario, pair[1][1]))
                self.hitsTakenDict[pair[0][1]]=self.hitsTakenDict[pair[0][1]]+1


                if self.isDead(pair[0][1]):
                    self.killedByDict[pair[0][1]] = pair[1][1]
                    self.eliminate(pair[0][1])

                else:
                    self.scenarioGenerator(pair)

        elif self.scenario in self.dexterityScenarios:
            if pair[0][5] > pair[1][5]:
                print("%s %s %s" %(pair[1][1],  self.scenario, pair[0][1]))
                self.hitsTakenDict[pair[1][1]]=self.hitsTakenDict[pair[1][1]]+1


                if self.isDead(pair[1][1]):
                    self.killedByDict[pair[1][1]] = pair[0][1]
                    self.eliminate(pair[1][1])

                else:
                    self.scenarioGenerator(pair)

            elif pair[0][5] == pair[1][5]:
                print("Both %s and %s survived!" % (pair[0][1], pair[1][1]))
                self.scenarioGenerator(pair)

            else:
                print("%s %s %s" % (pair[0][1], self.scenario, pair[1][1]))
                self.hitsTakenDict[pair[0][1]]=self.hitsTakenDict[pair[0][1]]+1


                if self.isDead(pair[0][1]):
                    self.killedByDict[pair[0][1]] = pair[1][1]
                    self.eliminate(pair[0][1])

                else:
                    self.scenarioGenerator(pair)


        elif self.scenario in self.intelligenceScenarios:
            if pair[0][4] > pair[1][4]:
                print("%s %s %s" % (pair[1][1], self.scenario, pair[0][1]))
                self.hitsTakenDict[pair[1][1]]=self.hitsTakenDict[pair[1][1]]+1

                if self.isDead(pair[1][1]):
                    self.killedByDict[pair[1][1]] = pair[0][1]
                    self.eliminate(pair[1][1])

                else:
                    self.scenarioGenerator(pair)

            elif pair[0][4] == pair[1][4]:
                print("Both %s and %s survived!" % (pair[0][1], pair[1][1]))
                self.scenarioGenerator(pair)

            else:
                print("%s %s %s" % (pair[0][1], self.scenario, pair[1][1]))
                self.hitsTakenDict[pair[0][1]]=self.hitsTakenDict[pair[0][1]]+1


                if self.isDead(pair[0][1]):
                    self.killedByDict[pair[0][1]] = pair[1][1]
                    self.eliminate(pair[0][1])

                else:
                    self.scenarioGenerator(pair)



        elif self.scenario in self.charismaScenarios:
            if pair[0][3] > pair[1][3]:
                print("%s %s %s" % (pair[1][1], self.scenario, pair[0][1]))
                self.hitsTakenDict[pair[1][1]]=self.hitsTakenDict[pair[1][1]]+1

                if self.isDead(pair[1][1]):
                    self.killedByDict[pair[1][1]] = pair[0][1]
                    self.eliminate(pair[1][1])

                else:
                    self.scenarioGenerator(pair)

            elif pair[0][3] == pair[1][3]:
                print("Both %s and %s survived!" % (pair[0][1], pair[1][1]))
                self.scenarioGenerator(pair)

            else:
                print("%s %s %s" % (pair[0][1], self.scenario, pair[1][1]))
                self.hitsTakenDict[pair[0][1]]=self.hitsTakenDict[pair[0][1]]+1

                if self.isDead(pair[0][1]):
                    self.killedByDict[pair[0][1]] = pair[1][1]
                    self.eliminate(pair[0][1])

                else:
                    self.scenarioGenerator(pair)


    def isDead(self, player):
        if self.hitsTakenDict[player] == 3:
            print("%s has been killed\n" % player)
            return True;
        else:
            return False;



    def scenarioGenerator(self, pair):
        self.strengthScenarios = [" was hit with an overpriced Calculus textbook by "]
        self.dexterityScenarios  = [" was pushed out of the engineering building by ", " was struck by Chip the Buffalo that was being ridden by ", " was hit by an RTD bus that was stolen by "]
        self.intelligenceScenarios = [" was fed C4C meat that had been poisoned by "]
        self.charismaScenarios = [" wore a CSU shirt on campus after being convinced by "]

        self.allScenarios=[]
        self.allScenarios.append(self.strengthScenarios)
        self.allScenarios.append(self.dexterityScenarios)
        self.allScenarios.append(self.intelligenceScenarios)
        self.allScenarios.append(self.charismaScenarios)



        #Selecting random category of scenarios
        self.attributeTypeNum = random.randint(0, int(len(self.allScenarios))-1)
        self.attributeType = self.allScenarios[self.attributeTypeNum]

        #Selecting random scenario
        self.scenarioNum = random.randint(0, int(len(self.attributeType))-1)
        self.scenario = self.attributeType[self.scenarioNum]




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

        with open("RoundResults.txt", mode="w") as roundResults:
            for killed, killer in self.killedByDict.items():
                roundResults.write(killer + " killed " + killed + "\n")




def main():
    matchUps = Match()
    numberOfPlayers = matchUps.storePlayerInfo()
    matchUps.battleCycle()
    #matchUps.writeRoundResults()

if(__name__ == "__main__"):
    main()
