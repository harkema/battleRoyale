#!/usr/bin/python3

import pymysql
import sys

import mainMenu

class BattleRoyale(object):
    def __init__(self):
        self.playerName = ""
        self.strength=0
        self.charisma=0
        self.intelligence=0
        self.dexterity=0

        self.insertStmt = ("INSERT INTO Player (PlayerName, Strength, Charisma, Intelligence, Dexterity)" "Values(%s, %s, %s, %s, %s)")

    def connectDB(self):
        self.db = pymysql.connect("127.0.0.1", "root", "NitrotheGreat22!", "playerDB")

        self.db.autocommit(True)

        self.cur = self.db.cursor()

    def readPlayerInfo(self):
        with open("playerInfo.txt", mode = "r") as playerInfo:

            for line in playerInfo:
                if line != "":
                    player = playerInfo.readline()
                    playerList = player.split(":")

                    self.playerName = playerList[0]
                    self.strength = int(playerList[1])
                    self.charisma = int(playerList[2])
                    self.intelligence = int(playerList[3])
                    self.dexterity = int(playerList[4])

                    #Adding each player to database
                    data = (self.playerName, self.strength, self.charisma, self.intelligence, self.dexterity)
                    self.cur.execute(self.insertStmt, data)

        playerInfo.close()



def main():
    app=mainMenu.App()
    app.exec_()
    app.quit()
    battleRoyale = BattleRoyale()
    battleRoyale.connectDB()
    battleRoyale.readPlayerInfo()

if(__name__ == "__main__"):
    main()
