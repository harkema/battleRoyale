#!/usr/bin/env python3

import cherrypy
import os, os.path

import pymysql
import sys

import mainMenu
import matchUps

import webbrowser

from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader('/home/kiha6349/Dropbox/battleRoyale/templates'))

class BattleRoyale(object):
    def __init__(self):
        self.playerName = ""
        self.strength=0
        self.charisma=0
        self.intelligence=0
        self.dexterity=0

        self.db = pymysql.connect("127.0.0.1", "root", "NitrotheGreat22!", "playerDB")

        self.db.autocommit(True)

        self.cur = self.db.cursor()



        self.insertStmt = ("INSERT INTO Player (PlayerName, Strength, Charisma, Intelligence, Dexterity)" "Values(%s, %s, %s, %s, %s)")
        self.retrieveAllStmt = ("SELECT * FROM Player")

    def connectDB(self):
        self.db = pymysql.connect("127.0.0.1", "root", "NitrotheGreat22!", "playerDB")

        self.db.autocommit(True)

        self.cur = self.db.cursor()

    def disconnect(self):
        self.db.close()

    def retrievePlayerInfo(self):
        """
        Gets all row from the player db
        """
        self.cur.execute(self.retrieveAllStmt)
        self.playerSelect = self.cur.fetchall()

        return self.playerSelect


    def readPlayerInfo(self):
        """
        Reads the player information provided through the GUI and adds it to the database
        """
        with open("playerInfo.txt", mode = "r") as playerInfo:

            for playerLine in playerInfo.readlines():
                if playerLine != "":

                    playerList = playerLine.split(":")

                    self.playerName = playerList[0]
                    self.strength = int(playerList[1])
                    self.charisma = int(playerList[2])
                    self.intelligence = int(playerList[3])
                    self.dexterity = int(playerList[4])

                    #Adding each player to database
                    data = (self.playerName, self.strength, self.charisma, self.intelligence, self.dexterity)
                    self.cur.execute(self.insertStmt, data)
                    self.db.commit()



        playerInfo.close()
        open("playerInfo.txt", "w").close()

    def deletePlayer(self, pid):
        """
        Option to delete player from the database
        """
        deleteStmt="DELETE FROM Player WHERE PersonalId = '%d'"
        self.cur.execute(deleteStmt % pid)

    def createMatch(self):
        """
        Creates a match object that lets the battle begin
        """
        #Generates matchups using player database
        match=matchUps.Match()
        playersRemaining = match.storePlayerInfo()

        #Clears the results from the previous round
        open("RoundResults.txt", "w").close()

        #Clears the descriptions from the previous round
        open("RoundDescriptions.txt", "w").close()

        #Rounds proceed until there is a winner
        while playersRemaining != 1:
            playersRemaining = match.battleCycle()
            #Writes both winners and the activities to their own files
            match.writeRoundResults()

        #Writes the kill counts to file
        match.writeBattleResults()

    def startWebApp(self):
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
        cherrypy.quickstart(Results(), '/', conf)
        webbrowser.open("http://127.0.0.1:8080")

def readRoundDesc():
    """
    Reads the round desc from file and adds to a list that can be interpreted by jinja
    """
    descList=[]
    roundList=[]

    with open("RoundDescriptions.txt", mode="r") as roundDesc:
        for line in roundDesc.readlines():
            if line == "\n":
                descList.append(roundList)
                roundList=[]
                continue

            line=line.strip()

            roundList.append(line)

        return roundList

def readRoundResults():
    """
    Reads the overall results of the round and adds to a list that be interpreted by jinja
    """
    #Overall list that contains a list of rounds with each "round list" containing lists that include the killer and the victim
    killedByList = []
    #List to separate the results by round
    roundList=[]

    with open("RoundResults.txt", mode="r") as roundResults:
        for line in roundResults.readlines():
            #Signifies the end of a round
            if line == "\n":
                killedByList.append(roundList)
                roundList=[]
                continue

            line=line.strip()
            lineList = line.split(": ")

            rowList = []
            rowList.append(lineList[0])#killer
            rowList.append(lineList[1])#victim

            roundList.append(rowList)

    winner = killedByList[-1][-1][0]

    return killedByList, winner

def readBattleResults():
    """
    Reads the kill count from the battle and return to be interpreted by jinja
    """
    #List of lists with each of the smaller lists containing a player and their kill count
    killsList=[]

    with open("Kills.txt", mode="r") as battleResults:
        for line in battleResults.readlines():
            line=line.strip()
            lineList=line.split(": ")

            rowList = []
            rowList.append(lineList[0])
            rowList.append(int(lineList[1]))

            killsList.append(rowList)
            killsList.sort(key=lambda x: x[1], reverse=True)

    return killsList

class Results(object):
    @cherrypy.expose
    def index(self):
        template = env.get_template("home.html")

        return template.render()

    @cherrypy.expose
    def roundResults(self):
        killedByList, winner = readRoundResults()

        template = env.get_template("roundResults.html")

        return template.render(killedByResults = killedByList, winner=winner)

    @cherrypy.expose
    def battleResults(self):
        killsList = readBattleResults()

        template = env.get_template("battleResults.html")

        return template.render(killResults =  killsList)

    """
    @cherrypy.expose
    def roundDescriptions(self):
        Create a page to display the activites that happened between rounds with a delay animation for each line
    """


def main():
    #Creates overseer object
    battleRoyale = BattleRoyale()

    #Opens GUI - allows user to input attribute information
    app=mainMenu.App()
    app.exec_()
    app.quit()

    #Adds player info to db
    battleRoyale.readPlayerInfo()

    #Open web page
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
    cherrypy.quickstart(Results(), '/', conf)

if(__name__ == "__main__"):
    main()
