#!/usr/bin/env python3

import cherrypy
import os, os.path

import pymysql
import sys

import mainMenu
import matchUps

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
        self.cur.execute(self.retrieveAllStmt)
        self.playerSelect = self.cur.fetchall()

        return self.playerSelect


    def readPlayerInfo(self):
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



        playerInfo.close()
        open("playerInfo.txt", "w").close()

    #def readRoundResults(self):
        #Store round results and pass to html file

    def deletePlayer(self, pid):
        deleteStmt="DELETE FROM Player WHERE PersonalId = '%d'"
        self.cur.execute(deleteStmt % pid)

    def createMatch(self):
        #Generates matchups using player database
        print("here")
        match=matchUps.Match()
        playersRemaining = match.storePlayerInfo()


        while playersRemaining != 1:
            playersRemaining = match.battleCycle()
            match.writeRoundResults()

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






def readBattleResults():
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
        template = env.get_template("roundResults.html")

        return template.render()

    @cherrypy.expose
    def battleResults(self):
        killsList = readBattleResults()

        template = env.get_template("battleResults.html")

        return template.render(killResults =  killsList)




def main():
    #Creates overseer object
    battleRoyale = BattleRoyale()

    #Opens GUI - allows user to input attribute information
    app=mainMenu.App()
    app.exec_()
    app.quit()

    #Adds player info to db
    battleRoyale.readPlayerInfo()




if(__name__ == "__main__"):
    main()
