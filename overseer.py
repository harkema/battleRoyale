#!/usr/bin/env python3

import cherrypy
import os, os.path

import pymysql
import sys

import mainMenu
import matchUps

import webbrowser
import random

from multiprocessing import cpu_count, Process
import argparse

import json

from selenium import webdriver

from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader('/home/kiha6349/Dropbox/battleRoyale/templates'))


class WebProcess(Process):
    def __init__(self, db, battleRoyale, results, roundDescDriver):
        Process.__init__(self)
        self.db = db
        self.battleRoyale = battleRoyale
        self.results = results
        self.roundDescDriver = roundDescDriver


    def run(self):
        #Opens web page
        conf = {
            '/': {
                'tools.sessions.on': True,
                'tools.staticdir.root': os.path.abspath(os.getcwd())
            },
            '/static': {
                'tools.staticdir.on': True,
                'tools.staticdir.dir': './public'
            }
        }
        cherrypy.quickstart(self.results, '/', conf)




class Database(object):
    def __init__(self, server="server", username="", password="", dbName=""):
        self.server=server
        self.username = username
        self.password = password
        self.dbName = dbName

        #Tables to create
        self.playerTable = "Player"
        self.roundTable = "Round"
        self.deathTable = "Death"

        self.cxn = None

        self.cur = None

        self.playerNames = []

    def connectDB(self):
        """
        Establishing connection to the database
        """
        self.cxn = pymysql.connect(self.server, self.username, self.password, self.dbName)

        self.cur = self.cxn.cursor()

        self.cxn.autocommit(True)


    def createDB(self):
        """
        Creates the three tables for the database
        """

        #Player information
        createStmt = "CREATE TABLE IF NOT EXISTS Player (PersonalID INT NOT NULL AUTO_INCREMENT,\
                                                       PlayerName VARCHAR(30) NOT NULL,\
                                                       Strength INT,\
                                                        Charisma INT,\
                                                         Intelligence INT,\
                                                          Dexterity INT,\
                                                            Kills INT,\
                                                           PRIMARY KEY (PersonalID))"

        self.cur.execute(createStmt)

        #Round activites
        createStmt = "CREATE TABLE IF NOT EXISTS Round (RoundID INT NOT NULL AUTO_INCREMENT,\
                                                       RoundNumber INT not null,\
                                                       PlayerOne VARCHAR(30),\
                                                        PlayerTwo VARCHAR(30),\
                                                         Scenario TEXT,\
                                                           PRIMARY KEY (RoundID))"

        self.cur.execute(createStmt)

        #Kills completed during the battle
        createStmt = "CREATE TABLE IF NOT EXISTS Death (KillID INT NOT NULL AUTO_INCREMENT,\
                                                      Killer VARCHAR(30),\
                                                      Victim VARCHAR(30),\
                                                      PRIMARY KEY (KillID))"

        self.cur.execute(createStmt)

    def checkBattleID(self, battleID):
        """
        Checks if BattleID already exists

        Input: battleID <int>
        """

        checkStmt = "SELECT * FROM Death WHERE EXISTS (SELECT * FROM Death WHERE BattleID=%d)"

        return self.cur.execute(checkStmt % battleID)


    def insertPlayer(self, name, strength, charisma, intelligence, dexterity):
        """
        Inserts a new player into the the database

        Input: name <str>, strength <int>, charisma <int>, intelligence <int>, dexterity <int>
        """
        insertStmt = ("INSERT INTO Player (PlayerName, Strength, Charisma, Intelligence, Dexterity)" "Values(%s, %s, %s, %s, %s)")

        data = (name, strength, charisma, intelligence, dexterity)

        self.cur.execute(insertStmt, data)

    def retrievePlayerInfo(self):
        """
        Retrieves player information
        """
        retrieveAllStmt = ("SELECT * FROM Player")

        self.cur.execute(retrieveAllStmt)

        self.playerSelect = self.cur.fetchall()

        for row in self.playerSelect:
            self.playerNames.append(row[1])

        return self.playerSelect

    def retrieveSinglePlayerInfo(self, pid):
        """
        Retrieves information for only one player
        """
        retrieveOneStmt = ("SELECT * FROM Player WHERE PersonalID = %d")

        self.cur.execute(retrieveOneStmt % pid)

        self.playerInfo = self.cur.fetchone()

        return self.playerInfo

    def editPlayer(self, att, changedValue, pid):
        """
        Edits player based on provided attribute and changed value
        """
        if(att == "PlayerName"):
            editStmt = ("UPDATE Player SET %s = '%s' WHERE PersonalID = %d")

        else:
            editStmt = ("UPDATE Player SET %s = %d WHERE PersonalID = %d")

        self.cur.execute(editStmt % (att, changedValue, pid))


    def retrieveRoundInfo(self, battleID):
        """
        Retrieves round activites for a particular battle

        Input: battleID <int>
        """

        retrieveAllStmt = ("SELECT * FROM Round WHERE BattleID = %d")

        self.cur.execute(retrieveAllStmt % battleID)

        self.roundSelect = self.cur.fetchall()

        return self.roundSelect

    def retrieveKillInfo(self, battleID):
        """
        Retrieves kills for a particular battle

        Input: battleID <int>
        """
        retrieveAllStmt = ("SELECT * FROM Death WHERE BattleID = %d")

        self.cur.execute(retrieveAllStmt % battleID)

        self.deathSelect = self.cur.fetchall()

        return self.deathSelect

    def deletePlayer(self, pid):
        """
        Deletes player from the database

        Input: pid <int>
        """
        deleteStmt="DELETE FROM Player WHERE PersonalId = '%d'"
        self.cur.execute(deleteStmt % pid)

    def addRoundResults(self, battleID, roundNumber, killer, victim):
        """
        Adds kill information to the database

        Input: battleID <int>, roundNumber <int>, killer <str>, victim <str>
        """
        insertKillStmt = ("INSERT INTO Death (BattleID, RoundNumber, Killer, Victim)" "Values(%s, %s, %s, %s)")

        data = (battleID, roundNumber, killer, victim)

        self.cur.execute(insertKillStmt, data)

    def addRoundDesc(self, battleID, roundNumber, playerOne, playerTwo, scenario):
        """
        Add round activities to the database

        Input: battleID <int>, roundNumber <int>, playerOne <str>, scenario <str>
        """
        insertDescStmt = ("INSERT INTO Round (BattleID, RoundNumber, PlayerOne, PlayerTwo, Scenario)" "Values(%s, %s, %s, %s, %s)")

        data = (battleID, roundNumber, playerOne, playerTwo, scenario)

        self.cur.execute(insertDescStmt, data)

    def addKills(self, playerID, numberOfKills):
        """
        Add kills for a existing player tabvle
        """
        insertKillNumberStmt = ("UPDATE Player SET Kills = %d WHERE PersonalID = %d")

        self.cur.execute(insertKillNumberStmt % (numberOfKills, playerID))


    def getChecksum(self, tableName):
        """
        Returns the checksum for a table
        """
        checkStmt = ("CHECKSUM TABLE %s")

        self.cur.execute(checkStmt % tableName)

        self.checkSum = self.cur.fetchone()

        if self.checkSum != None:
            return self.checkSum[1]
        else:
            print("Error: Checksum not valid")
            return -1


class BattleRoyale(object):
    def __init__(self, db):
        self.playerName = ""
        self.strength=0
        self.charisma=0
        self.intelligence=0
        self.dexterity=0


        self.playerNames=[]

        self.refresh = False

        self.db = db

        #Generates battleID
        self.battleID = random.randint(0, 1000)

        #Generates battleID until it is unique
        if self.db.checkBattleID(self.battleID) ==True:
            while self.db.checkBattleID(self.battleID) == True:
                self.battleID = random.randint(0, 1000)


    def createMatch(self):
        """
        Creates a match object that lets the battle begin
        """
        match=matchUps.Match(self.db, self.battleID)
        playersRemaining = match.storePlayerInfo()

        return match, playersRemaining


def readRoundDesc(db, battleID):
    """
    Reads the round desc from file and adds to a list that can be interpreted by jinja
    """
    descList=[]
    roundList=[]
    namesList=[]
    prevRound=1

    #Retrieves round descriptions from the database
    roundInfo = db.retrieveRoundInfo(battleID)

    #Tracks which round is currently being manipulated
    index=0

    #Iterates through each round in the retrieved info
    for roundTup in roundInfo:
        #If is is the last round, the round description is added to the list which is then added to the overall list
        if roundTup == roundInfo[-1]:
            roundList.append(roundTup[5])
            descList.append(roundList)
            break

        #If the round is different, a new sublist is created for the new round
        if roundTup[2] != prevRound:
            descList.append(roundList)
            roundList=[]

        #Adds player names to namesList for reference by HTML
        if roundTup[3] not in namesList:
            namesList.append(roundTup[3])

        if roundTup[4] not in namesList:
            namesList.append(roundTup[4])

        #Adds the round description to the sublist that is separated by round
        roundList.append(roundTup[5])

        index=index+1

        #Compares what the round number was for the previous description to see whether the round has advanced
        prevRound=roundInfo[index-1][2]

    return descList, namesList

def readRoundResults(db, battleID):
    """
    Reads the overall results of the round and adds to a list that be interpreted by jinja
    """
    #Overall list that contains a list of rounds with each "round list" containing lists that include the killer and the victim
    killedByList = []
    #List to separate the results by round
    roundList=[]

    prevRound=1

    #Retrieves information about who killed who
    deathInfo = db.retrieveKillInfo(battleID)

    index=0
    #Iterates through the the retrieved information which contains killer and victims
    for deathEventTup in deathInfo:
        #Contains killer and victim
        pairList=[]

        #If the round is different, a new sublist is created for the new round
        if deathEventTup[1] != prevRound:
            killedByList.append(roundList)
            roundList=[]

        #If is is the last round, the round description is added to the list which is then added to the overall list
        if deathEventTup == deathInfo[-1]:
            pairList.append(deathEventTup[3])
            pairList.append(deathEventTup[4])
            roundList.append(pairList)
            killedByList.append(roundList)
            break

        #Adds the two names to a list that is added to the round sublist
        pairList.append(deathEventTup[3])
        pairList.append(deathEventTup[4])
        roundList.append(pairList)

        index=index+1

        #Compares what the round number was for the previous description to see whether the round has advanced
        prevRound=deathInfo[index-1][1]

    #Stores the overall battle winner
    if len(killedByList) == 4:
        winner = killedByList[-1][0][0]
    else:
        winner = "None"

    return killedByList, winner

def readBattleResults(db):
    """
    Reads the kill count from the battle and return to be interpreted by jinja
    """
    #List of lists with each of the smaller lists containing a player and their kill count
    killsList=[]

    playerInfo = db.retrievePlayerInfo()

    for playerTup in playerInfo:
        #Contains player and kill count
        tempList=[]
        tempList.append(playerTup[1])
        tempList.append(playerTup[6])

        #Overall list
        killsList.append(tempList)

    #Sorts list in descending order based on kill counts
    killsList.sort(key=lambda x: x[1], reverse=True)

    return killsList



class Results(object):
    def __init__(self, db, battleRoyale,roundDescDriver):
        self.db = db
        self.battleRoyale = battleRoyale

        self.battleID = battleRoyale.battleID

        self.roundDescDriver = roundDescDriver

        self.beforeChecksum = self.db.getChecksum("Round")

        self.roundChecksums = []

        self.roundChecksums.append(self.beforeChecksum)

        self.checksumChange = False


    def verifyChecksum(self):
        #checksum = self.db.getChecksum("Round")

        #if self.roundChecksums[-1] != checksum:
                #self.checksumChange = True
                #self.roundResultsDriver.get("http://127.0.0.1:8080/roundResults")
        self.roundDescDriver.get("http://127.0.0.1:8080/roundResults")
        #else:
            #self.checksumChange = False
        #self.roundChecksums.append(checksum)
        #reload after each get

    def showScoreboard(self):
        self.roundDescDriver.get("http://127.0.0.1:8080/battleResults")

    def showHomePage(self):
        self.roundDescDriver.get("http://127.0.0.1:8080/index")


    @cherrypy.expose
    def index(self):
        template = env.get_template("home.html")

        return template.render()


    @cherrypy.expose
    def battleResults(self):
        killsList = readBattleResults(self.db)

        template = env.get_template("battleResults.html")

        return template.render(killResults =  killsList)


    @cherrypy.expose
    def roundDescriptions(self):
        #A list containing sublists of rounds which contain sublists of statements where each element is a word
        descList, namesList = readRoundDesc(self.db,  self.battleID)

        template = env.get_template("roundDesc.html")

        return template.render(descResults = descList, playerNames=namesList, checksumChange=json.dumps(self.checksumChange))


    @cherrypy.expose
    def roundResults(self):
        killedByList, winner = readRoundResults(self.db, self.battleID)

        template = env.get_template("roundResults.html")

        return template.render(killedByResults = killedByList, winner=winner, checksumChange=json.dumps(self.checksumChange))


def main():
    #Creating Database object
    db = Database("127.0.0.1", "root", "NitrotheGreat22!", "playerDB")

    #Connecting to database
    db.connectDB()

    #Creating tables for database
    db.createDB()

    #Creates overseer object
    battleRoyale = BattleRoyale(db)

    #roundResultsDriver = webdriver.Chrome()
    roundDescDriver = webdriver.Chrome()


    #Generates webpage
    resultsWebpage = Results(db, battleRoyale, roundDescDriver)

    #Creating process that will open the web page; staging the server
    process = WebProcess(db, battleRoyale, resultsWebpage, roundDescDriver)

    process.start()

    #roundResultsDriver.get("http://127.0.0.1:8080/roundResults")
    roundDescDriver.get("http://127.0.0.1:8080/index")

    #Opens GUI - allows user to input attribute information
    app=mainMenu.App(db, battleRoyale, resultsWebpage)

    app.exec_()

    #Close the web page when the app closes
    process.terminate()

    app.quit()


if(__name__ == "__main__"):
    main()
