#!/usr/bin/python3

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys
import overseer
import webbrowser

class App(QApplication):
    def __init__(self, db, battleRoyale, resultsWebpage):
        """
        Main application
        """
        QApplication.__init__(self, sys.argv)
        self.db = db
        self.setApplicationName("Battle Royale")
        self.mainWindow = MainWindow(self.db, battleRoyale, resultsWebpage)
        self.mainWindow.show()

class MainWindow(QMainWindow):
    def __init__(self, db, battleRoyale, resultsWebpage):
        """
        Main Window w/ option to enter a new player and start the battle"
        """

        QMainWindow.__init__(self)
        self.setWindowTitle("Main Menu")

        self.db = db

        self.mainWidget = MainWidget(self.db, battleRoyale, resultsWebpage)
        self.setCentralWidget(self.mainWidget)

        self.resize(200, 500)

class MainWidget(QWidget):
    def __init__(self, db, battleRoyale, resultsWebpage):
        """
        Lets user manipulate player database and start the battle
        """
        QWidget.__init__(self)

        self.mainLayout = QVBoxLayout(self)

        self.buttonLayout = QVBoxLayout()

        self.appFont = QFont("Arial", 14)

        self.db = db

        self.battleRoyale = battleRoyale

        self.results = resultsWebpage

        self.searchResults = self.db.retrievePlayerInfo()

        #Welcome label
        self.welcomeLabel = QLabel("Welcome to the Battle Royale!")
        self.welcomeLabel.setFont(QFont("Arial", 20))


        #Button that opens quiz window for player to take
        self.newPlayerPushButton = QPushButton("Create a New Player")
        self.buttonLayout.addWidget(self.newPlayerPushButton)

        #Starts battle w/ characters that were entered
        self.startPushButton = QPushButton("Start battle!")

        #Shows table of all players currently in db
        self.viewPushButton = QPushButton("View All Players")
        self.buttonLayout.addWidget(self.viewPushButton)
        self.viewPushButton.clicked.connect(self.showView)

        #Show all players that can be deleted and delete
        self.deletePushButton = QPushButton("Delete Player")
        self.buttonLayout.addWidget(self.deletePushButton)
        self.deletePushButton.clicked.connect(self.deletePlayer)

        #Show all players that can be edited and edit
        self.editPushButton = QPushButton("Edit Player")
        self.buttonLayout.addWidget(self.editPushButton)
        self.editPushButton.clicked.connect(self.editPlayer)

        #Opens webpage
        self.openResultsPushButton = QPushButton("View Scoreboard")
        self.buttonLayout.addWidget(self.openResultsPushButton)
        self.openResultsPushButton.clicked.connect(self.openWebBrowser)
        self.openResultsPushButton.setEnabled(False)

        #Shows events of past battle
        self.historyPushButton = QPushButton("View Past Battle History")
        self.buttonLayout.addWidget(self.historyPushButton)
        self.historyPushButton.clicked.connect(self.showHistory)


        #Creating menu bar
        self.menuBar = QMenuBar()

        #Creating player menu
        self.playerMenu=QMenu("Player")
        self.menuBar.addMenu(self.playerMenu)

        #Create new player option
        self.newPlayerAction = QAction("New...", self.playerMenu)
        self.playerMenu.addAction(self.newPlayerAction)
        self.newPlayerAction.triggered.connect(self.showAttributes)

        #Delete player option
        self.deletePlayerAction = QAction("Delete...", self.playerMenu)
        self.playerMenu.addAction(self.deletePlayerAction)
        self.deletePlayerAction.triggered.connect(self.deletePlayer)

        #View all players option
        self.viewPlayersAction = QAction("View...", self.playerMenu)
        self.playerMenu.addAction(self.viewPlayersAction)
        self.viewPlayersAction.triggered.connect(self.showView)


        #Creatings results menu
        self.resultsMenu = QMenu("Results")
        self.menuBar.addMenu(self.resultsMenu)

        #Creating view home option
        self.homeAction = QAction("View home page...", self.resultsMenu)
        self.resultsMenu.addAction(self.homeAction)
        self.homeAction.triggered.connect(self.openHomePage)

        #Creating view scoreboad option
        self.scoreboardAction = QAction("View scoreboard...", self.resultsMenu)
        self.resultsMenu.addAction(self.scoreboardAction)
        self.scoreboardAction.triggered.connect(self.openWebBrowser)

        #Adding Picture
        self.shieldLabel = QLabel()
        self.shieldPixmap = QPixmap("/home/kiha6349/Dropbox/battleRoyale/public/images/shield.png")
        self.shieldLabel.setPixmap(self.shieldPixmap)


        self.mainLayout.addWidget(self.menuBar)
        self.mainLayout.addWidget(self.welcomeLabel, alignment=Qt.AlignCenter)
        self.mainLayout.addStretch(1)
        self.mainLayout.addLayout(self.buttonLayout)
        self.mainLayout.addStretch(1)
        self.mainLayout.addWidget(self.shieldLabel)
        self.mainLayout.addWidget(self.startPushButton)

        self.newPlayerPushButton.clicked.connect(self.showAttributes)
        self.startPushButton.clicked.connect(self.startBattle)

    def showHistory(self):
        """
        Opens dialog window that lets user enter a battle id and get results from that battle
        """

        self.historyDialog = HistoryDialog(self.db)
        self.historyDialog.show()

    def editPlayer(self):
        """
        Opens dialog window that lets user select player to edit
        """
        self.editDialog = EditDialog(self.searchResults, self.db,)
        self.editDialog.show()

    def openHomePage(self):
        """
        Opens the home page of the results webpage
        """

        self.results.showHomePage()
    def openWebBrowser(self):
        """
        Opens results of each round and the battle in a webpage
        """
        self.results.showScoreboard()

    def showAttributes(self):
        """
        Opens dialog window that lets user select attributes for their player
        """
        self.attributeDialog = AttributeDialog(self.db)
        self.attributeDialog.show()

    def showView(self):
        """
        Opens dialog window that displays all players in the database
        """
        self.searchResults = self.db.retrievePlayerInfo()

        self.viewDialog = ViewDialog(self.searchResults)
        self.viewDialog.show()

    def deletePlayer(self):
        """
        Opens dialog window that lets user select player(s) to delete
        """
        self.searchResults = self.db.retrievePlayerInfo()

        self.deleteDialog = DeleteDialog(self.searchResults, self.db)
        self.deleteDialog.show()


    def startBattle(self):
        """
        Opens dialog window that lets user view players before starting battle
        """
        self.startDialog = StartDialog(self.searchResults, self.db, self.battleRoyale, self.results)
        self.startDialog.show()
        self.openResultsPushButton.setEnabled(True)

class ResponseLabel(QLabel):
    def __init__(self, text, layout, row):
        """
        Custom class for labels that go w/ attribute combo box
        """
        QLabel.__init__(self, text)
        self.baseLayout=layout
        self.row=row
        self.column=0

        self.baseLayout.addWidget(self, self.row, self.column)

class QuestionLabel(QLabel):
    def __init__(self, text, layout, row):
        """
        Custom class for labeled descriptions
        """
        QLabel.__init__(self, text)
        self.setFont(QFont("Arial", 14))
        self.baseLayout=layout
        self.row=row
        self.column=0
        #self.scrollArea = scroll
        self.baseLayout.addWidget(self, self.row, self.column)
        #self.scrollArea.setWidget(self)

class NumberComboBox(QComboBox):
    def __init__(self, layout, row,):
        """
        Custom class for combo boxes used to select attributes
        """
        QComboBox.__init__(self)

        self.baseLayout = layout
        self.numberData =  []

        self.addItem("0", self.numberData)
        self.addItem("1", self.numberData)
        self.addItem("2", self.numberData)
        self.addItem("3", self.numberData)
        self.addItem("4", self.numberData)
        self.addItem("5", self.numberData)
        self.addItem("6", self.numberData)
        self.addItem("7", self.numberData)
        self.addItem("8", self.numberData)
        self.addItem("9", self.numberData)
        self.addItem("10", self.numberData)
        self.addItem("11", self.numberData)
        self.addItem("12", self.numberData)
        self.addItem("13", self.numberData)
        self.addItem("14", self.numberData)
        self.addItem("15", self.numberData)
        self.addItem("16", self.numberData)
        self.addItem("17", self.numberData)
        self.addItem("18", self.numberData)
        self.addItem("19", self.numberData)
        self.addItem("20", self.numberData)

        self.row=row
        self.column=1

        self.baseLayout.addWidget(self, self.row, 1)


    def currentRating(self):
        return self.currentIndex()

class ViewHistoryDialog(QDialog):
    def __init__(self, db, battleID):
        """
        Shows record of who killed who during a given battle
        """
        QDialog.__init__(self)
        self.mainLayout = QVBoxLayout(self)

        self.db = db
        self.battleID = battleID

        self.trackRound = 1

        self.closePushButton = QPushButton("Close")
        self.closePushButton.clicked.connect(self.close)

        #Creating tab bar and tabs
        self.battleTabBar = QTabWidget()
        self.killsTab = QWidget()
        self.playTab = QWidget()

        #Addings tabs to tab bar
        self.battleTabBar.addTab(self.killsTab, "Kills")
        #self.battleTabBar.addTab(self.playTab, "Play-by-Play")

        #Adding kills tab layout
        self.killsTab.layout = QVBoxLayout()
        self.killsTab.setLayout(self.killsTab.layout)

        #Adding play-by-play tab layout
        self.playTab.layout = QVBoxLayout()
        #self.playTab.setLayout(self.playTab.layout)

        #Getting battle kill and play-by-play info
        self.battleKills = self.db.retrieveKillInfo(self.battleID)
        self.playInfo = self.db.retrieveRoundInfo(self.battleID)

        #Labels rounds
        self.roundLabel = QLabel(str(self.trackRound))
        self.roundLabel.setFont(QFont("Arial", 16))

        #Adding round label to the kill tab layout
        self.killsTab.layout.addWidget(self.roundLabel, alignment = Qt.AlignCenter)

        #Adding scroll area for play-by-play
        self.scrollArea = QScrollArea()
        self.scrollLayout = QVBoxLayout()

        self.scrollArea.setFrameShape(QFrame.Box)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scrollArea.setWidgetResizable(True)
        #self.playTab.layout.addWidget(self.scrollArea)

        self.scrollArea.setLayout(self.playTab.layout)

        #Adding kill information to labels for the kill tab
        for row in self.battleKills:
            #Accounting for round label
            if row[1] != self.trackRound:
                self.trackRound=self.trackRound+1
                self.roundLabel = QLabel(str(self.trackRound))
                self.roundLabel.setFont(QFont("Arial", 16))
                self.killsTab.layout.addWidget(self.roundLabel, alignment = Qt.AlignCenter)

            self.killLabel = QLabel(row[3] + " killed " + row[4])
            self.killsTab.layout.addWidget(self.killLabel)



        """
        #Adding play by play info to labels for the play tab
        for row in self.playInfo:
            if row[2] != self.trackRound:
                self.trackRound=self.trackRound+1
                self.roundLabel = QLabel(str(self.trackRound))
                self.roundLabel.setFont(QFont("Arial", 16))
                self.playTab.layout.addWidget(self.roundLabel, alignment = Qt.AlignCenter)

            self.playLabel = QLabel(row[5])
            self.playTab.layout.addWidget(self.playLabel)

        """


        #Adding tab bar to layout
        self.mainLayout.addWidget(self.battleTabBar)
        self.mainLayout.addWidget(self.closePushButton)

        def close(self):
            self.accept()

class HistoryDialog(QDialog):
    def __init__(self, db):
        """
        Prompts user to enter a battle ID and show record of kills from that battle
        """
        QDialog.__init__(self)
        self.mainLayout = QVBoxLayout(self)
        self.historyLayout = QVBoxLayout()

        self.db = db

        self.historyLabel = QLabel("Enter your Battle ID to view results")
        self.historyLabel.setFont(QFont("Arial, 16"))
        self.historyLayout.addWidget(self.historyLabel)

        self.battleIDLineEdit = QLineEdit("Enter ID")
        self.historyLayout.addWidget(self.battleIDLineEdit)

        self.seeHistoryPushButton = QPushButton("See Battle History")
        self.seeHistoryPushButton.clicked.connect(self.seeHistory)

        self.closePushButton=QPushButton("Close")
        self.closePushButton.clicked.connect(self.close)

        self.mainLayout.addLayout(self.historyLayout)
        self.mainLayout.addWidget(self.seeHistoryPushButton)
        self.mainLayout.addWidget(self.closePushButton)

    def close(self):
        self.accept()

    def seeHistory(self):
        self.battleID = int(self.battleIDLineEdit.text())

        if self.db.checkBattleID(self.battleID):
            self.viewHistoryDialog  =  ViewHistoryDialog(self.db, self.battleID)
            self.viewHistoryDialog.show()

        else:
            title="Error: Battle ID Doesn't Exist"
            msg="Please Enter a Valid Battle ID and Try Again"

            QMessageBox.information(self, title, msg)

class BattleDialog(QDialog):
    def __init__(self, battleRoyale, resultsWebpage):
        """
        Dialog box that allows the user to proceed through battle
        """
        QDialog.__init__(self)
        self.mainLayout = QVBoxLayout(self)

        self.battleRoyale = battleRoyale

        self.roundNumber = 0

        self.resultsWebpage = resultsWebpage

        self.welcomeLabel = QLabel("Battle has started! Click on the button below to advance to the next round")
        self.battleIDLabel = QLabel("Your Battle ID is %s" % battleRoyale.battleID)
        self.welcomeLabel.setFont(QFont("Arial", 16))
        self.battleIDLabel.setFont(QFont("Arial", 16))
        self.mainLayout.addWidget(self.welcomeLabel, alignment = Qt.AlignCenter)
        self.mainLayout.addWidget(self.battleIDLabel, alignment = Qt.AlignCenter)

        #Generates matchups using player database
        self.match, self.playersRemaining = self.battleRoyale.createMatch()

        self.nextRoundPushButton = QPushButton("Next Round")
        self.nextRoundPushButton.clicked.connect(self.nextRound)
        self.mainLayout.addWidget(self.nextRoundPushButton)

        self.shieldLabel = QLabel()
        self.shieldLabel.resize(50, 50)
        self.shieldPixmap = QPixmap("/home/kiha6349/Dropbox/battleRoyale/public/images/shield.png")
        self.shieldPixmap.scaledToHeight(50)
        self.shieldPixmap.scaledToWidth(50)
        self.shieldLabel.setPixmap(self.shieldPixmap)
        self.mainLayout.addWidget(self.shieldLabel)


        self.closePushButton = QPushButton("Close")
        self.closePushButton.clicked.connect(self.close)
        self.mainLayout.addWidget(self.closePushButton)



    def nextRound(self):
        """
        Retrieves information as the database is updated with results from a given round
        """
        self.roundNumber=self.roundNumber+1

        self.playersRemaining = self.match.battleCycle(self.roundNumber)

        #DB change prompts webpage to refresh
        self.match.addRoundResultsDB()
        self.resultsWebpage.verifyChecksum()

        if self.playersRemaining == 1:
            self.match.addBattleResultsDB()
            self.nextRoundPushButton.setEnabled(False)

            title="Battle Complete!"
            msg="Battle Complete! See the Battle webpage to view overall results, play-by-play action, and updated kill counts"

            self.completeMessageBox = QMessageBox.information(self, title, msg)


    def close(self):
        self.accept()

class StartDialog(QDialog):
    def __init__(self, results, db, battleRoyale, resultsWebpage):
        """
        Dialog box that shows user players before being able to start battle
        """
        QDialog.__init__(self)
        self.mainLayout = QVBoxLayout(self)

        self.startPushButton  = QPushButton("Start")
        self.closePushButton = QPushButton("Close")

        #Player information retrieved from db
        self.results = results

        self.db = db

        self.battleRoyale = battleRoyale

        self.resultsWebpage = resultsWebpage

        #Creating Label
        self.questionLabel = QLabel("Start Battle With Following Players?")
        self.mainLayout.addWidget(self.questionLabel)

        #Creating table with player information displayed
        self.playerTable = QTableWidget()

        self.playerTable.setColumnCount(5)
        self.playerTable.setHorizontalHeaderLabels(["Name", "Strength", "Charisma", "Intelligence", "Dexterity"])

        self.playerTable.setRowCount(len(self.results))

        self.mainLayout.addWidget(self.playerTable)

        colCount=0
        rowCount=0

        #Filling table
        for row in self.results:
            for col in row:
                if col == row[0]:
                    continue

                self.cellWidget=QTableWidgetItem()
                self.cellWidget.setText(str(col))
                self.playerTable.setItem(rowCount, colCount, self.cellWidget)

                colCount+=1

                if colCount==6:
                    colCount=0
                    rowCount+=1


        self.startPushButton.clicked.connect(self.start)
        self.closePushButton.clicked.connect(self.close)
        self.mainLayout.addWidget(self.startPushButton, alignment=Qt.AlignCenter)
        self.mainLayout.addWidget(self.closePushButton, alignment = Qt.AlignCenter)

    def close(self):
        self.accept()

    def start(self):
        """
        Starts match
        """
        self.battleDialog = BattleDialog(self.battleRoyale, self.resultsWebpage)
        self.battleDialog.show()
        self.accept()

class PlayerAttDialog(QDialog):
    def __init__(self, selectedPlayer, db):
        """
        Shows player attributes and allows for edits to be made
        """
        QDialog.__init__(self)
        self.mainLayout = QVBoxLayout(self)
        self.editLayout = QVBoxLayout()

        self.selectedPlayerPID = selectedPlayer

        self.db = db

        self.playerInfo = self.db.retrieveSinglePlayerInfo(self.selectedPlayerPID)

        self.genLabel = QLabel("Edit Attributes")
        self.genLabel.setFont(QFont("Arial", 16))
        self.editLayout.addWidget(self.genLabel)

        #Edit Name
        self.nameLabel = QLabel("Name")
        self.nameLineEdit = QLineEdit(self.playerInfo[1])
        self.editLayout.addWidget(self.nameLabel)
        self.editLayout.addWidget(self.nameLineEdit)

        #Edit Strength
        self.strengthLabel = QLabel("Strength")
        self.strengthLineEdit = QLineEdit(str(self.playerInfo[2]))
        self.editLayout.addWidget(self.strengthLabel)
        self.editLayout.addWidget(self.strengthLineEdit)

        #Edit Charisma
        self.charismaLabel = QLabel("Charisma")
        self.charismaLineEdit = QLineEdit(str(self.playerInfo[3]))
        self.editLayout.addWidget(self.charismaLabel)
        self.editLayout.addWidget(self.charismaLineEdit)

        #Edit Intelligence
        self.intelligenceLabel = QLabel("Intelligence")
        self.intelligenceLineEdit = QLineEdit(str(self.playerInfo[4]))
        self.editLayout.addWidget(self.intelligenceLabel)
        self.editLayout.addWidget(self.intelligenceLineEdit)

        #Edit Dexterity
        self.dexterityLabel = QLabel("Dexterity")
        self.dexterityLineEdit  = QLineEdit(str(self.playerInfo[5]))
        self.editLayout.addWidget(self.dexterityLabel)
        self.editLayout.addWidget(self.dexterityLineEdit)

        self.saveEditsPushButton = QPushButton("Save Changes")
        self.saveEditsPushButton.clicked.connect(self.saveEdits)
        self.saveEditsPushButton.clicked.connect(self.close)


        self.closePushButton = QPushButton("Close")
        self.closePushButton.clicked.connect(self.close)

        self.mainLayout.addLayout(self.editLayout)
        self.mainLayout.addWidget(self.saveEditsPushButton)
        self.mainLayout.addWidget(self.closePushButton)


    def close(self):
        self.accept()

    def saveEdits(self):
        title="Save Changes"
        msg="Save current changes?"

        reply=QMessageBox.question(self, title, msg)

        if reply == QMessageBox.Yes:

            if self.nameLineEdit.isModified():
                changedValue = self.nameLineEdit.text()
                att = "PlayerName"

                self.db.editPlayer(att, changedValue, self.selectedPlayerPID)

            if self.strengthLineEdit.isModified():
                changedValue =int(self.strengthLineEdit.text())
                att = "Strength"

                self.db.editPlayer(att, changedValue, self.selectedPlayerPID)

            if self.charismaLineEdit.isModified():
                changedValue = int(self.charismaLineEdit.text())
                att = "Charisma"

                self.db.editPlayer(att, changedValue, self.selectedPlayerPID)

            if self.intelligenceLineEdit.isModified():
                changedValue = int(self.intelligenceLineEdit.text())
                att= "Intelligence"

                self.db.editPlayer(att, changedValue, self.selectedPlayerPID)

            if self.dexterityLineEdit.isModified():
                changedValue = int(self.dexterityLineEdit.text())
                att= "Dexterity"

                self.db.editPlayer(att, changedValue, self.selectedPlayerPID)

            totalPoints = int(self.strengthLineEdit.text())+int(self.charismaLineEdit.text())+int(self.intelligenceLineEdit.text())+int(self.dexterityLineEdit.text())

            print("Points", totalPoints)

            if totalPoints != 20:
                pointTitle = "Points not allocated correctly"
                msg = "Error: Total points do not equal 20. Please reallocate points."

                QMessageBox.information(self, pointTitle, msg)

class EditDialog(QDialog):
    def __init__(self, searchResults, db):
        """
        Dialog window for user to select player to edit
        """
        QDialog.__init__(self)
        self.mainLayout = QVBoxLayout(self)
        self.selectionLayout = QVBoxLayout()

        self.results = searchResults

        self.db = db

        self.genLabel = QLabel("Select Player You Would Like to Edit")
        self.mainLayout.addWidget(self.genLabel)

        self.closePushButton = QPushButton("Close")

        self.editPushButton=QPushButton("Edit")

        self.boxList = []

        #Verifies only one checkbox is selected
        self.firstCheck=False

        #Creating message box
        for row in self.results:
            checkBoxTxt=""
            checkBoxTxt=str(row[0])+ " " + str(row[1])
            self.checkBox=QCheckBox(checkBoxTxt)
            self.boxList.append(self.checkBox)

        for self.box in self.boxList:
            self.selectionLayout.addWidget(self.box)
            self.box.toggled.connect(self.disableBoxes)

        self.mainLayout.addLayout(self.selectionLayout)
        self.mainLayout.addWidget(self.editPushButton, alignment=Qt.AlignCenter)
        self.mainLayout.addWidget(self.closePushButton, alignment=Qt.AlignCenter)

        self.closePushButton.clicked.connect(self.closeMe)
        self.editPushButton.clicked.connect(self.showAtt)
        self.editPushButton.clicked.connect(self.closeMe)

    def disableBoxes(self):
        for self.disableBox in self.boxList:
            if not self.disableBox.isChecked():
                self.disableBox.setEnabled(False)

    def closeMe(self):
        self.accept()

    def showAtt(self):
        """
        Show selected players attributes to be edited
        """
        title="Edit Player?"
        name=""

        for self.box in self.boxList:
            #Checks that the box is checked and the first check has not already been made
            if self.box.isChecked():
                name = self.box.text()
                self.checkedBox = self.box

        msg="Edit " + name + "?"
        reply=QMessageBox.question(self, title, msg)

        if reply == QMessageBox.Yes:
            pid = int(self.checkedBox.text().split(" ")[0])
            self.playerAttDialog = PlayerAttDialog(pid, self.db)
            self.playerAttDialog.show()

class DeleteDialog(QDialog):
    def __init__(self, searchResults, db):
        """
        Dialog window for user to select players to delete
        """
        QDialog.__init__(self)
        self.mainLayout = QVBoxLayout(self)
        self.selectionLayout = QVBoxLayout()

        self.results = searchResults

        self.db = db

        self.genLabel=QLabel("Select Player(s) You Would Like to Delete\n")
        self.mainLayout.addWidget(self.genLabel)

        self.closePushButton=QPushButton("Close")

        self.deletePushButton=QPushButton("Delete")

        self.boxList=[]

        #Creating message box
        for row in self.results:
            checkBoxTxt=""
            checkBoxTxt=str(row[0])+ " " + str(row[1])
            self.checkBox=QCheckBox(checkBoxTxt)
            self.boxList.append(self.checkBox)

        for self.box in self.boxList:
            self.selectionLayout.addWidget(self.box)

        self.mainLayout.addLayout(self.selectionLayout)
        self.mainLayout.addWidget(self.deletePushButton, alignment=Qt.AlignCenter)
        self.mainLayout.addWidget(self.closePushButton, alignment=Qt.AlignCenter)

        self.closePushButton.clicked.connect(self.closeMe)
        self.deletePushButton.clicked.connect(self.deleteSelections)

    def closeMe(self):
        self.accept()

    def deleteSelections(self):
        """
        Message Box that allows user to delete the player
        """
        title="Delete Player?"

        for self.box in self.boxList:
            if self.box.isChecked():
                msg="Delete " + self.box.text() +"?"
                reply=QMessageBox.question(self, title, msg)

                if reply == QMessageBox.Yes:
                    pid = int(self.box.text().split(" ")[0])
                    self.db.deletePlayer(pid)
        self.close()

class ViewDialog(QDialog):
    def __init__(self, searchResults):
        """
        Dialog window containing table that shows all players currently in the database
        """
        QDialog.__init__(self)
        self.mainLayout = QVBoxLayout(self)
        self.results = searchResults

        self.closePushButton = QPushButton("Close")

        self.playerTable = QTableWidget()

        self.playerTable.setColumnCount(5)
        self.playerTable.setHorizontalHeaderLabels(["Name", "Strength", "Charisma", "Intelligence", "Dexterity"])

        self.playerTable.setRowCount(len(self.results))

        self.mainLayout.addWidget(self.playerTable)

        colCount=0
        rowCount=0

        #Creating table
        for row in self.results:
            for col in row:
                if col == row[0]:
                    continue

                self.cellWidget=QTableWidgetItem()
                self.cellWidget.setText(str(col))
                self.playerTable.setItem(rowCount, colCount, self.cellWidget)

                colCount+=1

                if colCount==6:
                    colCount=0
                    rowCount+=1


        self.closePushButton.clicked.connect(self.close)
        self.mainLayout.addWidget(self.closePushButton, alignment=Qt. AlignCenter)

    def close(self):
        self.accept()

class AttributeDialog(QDialog):
    def __init__(self, db):
        """
        Dialog box that allows user to select attributes for player
        """
        QDialog.__init__(self)
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setSpacing(25)

        self.db  = db

        #Layout w/ attributes
        self.attLayout = QGridLayout()
        self.attLayout.setVerticalSpacing(25)

        self.strengthCounter = 0;
        self.charismaCounter= 0;
        self.intelligenceCounter = 0;
        self.dexterityCounter = 0;

        self.appFont = QFont("Arial", 14)

        self.nameLineEdit = QLineEdit("Enter Name");

        self.infoLabel = QLabel("Distribute your attribute points!\nYou are given 20 points to assign to four categories.\n")
        self.infoLabel.setFont(QFont("Arial", 14))

        self.mainLayout.addStretch()


        #######################
        #Strength
        ########################
        #Creating attribute labels
        self.strengthLabel = QuestionLabel("Strength", self.attLayout, 0)

        #Creating Response labels and their combo boxes
        self.r1Label = ResponseLabel("Points", self.attLayout, 1)
        self.numberComboBox1 = NumberComboBox(self.attLayout, 1)


        #######################
        #Charisma
        ########################
        #Creating attribute labels
        self.qTwoLabel = QuestionLabel("Charisma", self.attLayout, 5)

        #Creating Response labels and their combo boxes
        self.r2Label = ResponseLabel("Points", self.attLayout, 6)
        self.numberComboBox2 = NumberComboBox(self.attLayout, 6)

        #######################
        #Intelligence
        ########################
        #Creating attribute labels
        self.qThreeLabel = QuestionLabel("Intelligence", self.attLayout, 12)

        #Creating Response labels and their combo boxes
        self.r3Label = ResponseLabel("Points", self.attLayout, 13)
        self.numberComboBox3 = NumberComboBox(self.attLayout, 13)

        ####################
        #Dexterity
        ####################
        #Creating attribute labels
        self.qFourLabel = QuestionLabel("Dexterity", self.attLayout, 14)

        #Creating Response labels and their combo boxes
        self.r4Label = ResponseLabel("Points", self.attLayout, 15)
        self.numberComboBox4 = NumberComboBox(self.attLayout, 15)


        self.closePushButton = QPushButton("Close")
        self.closePushButton.clicked.connect(self.closeMe)

        self.finishPushButton = QPushButton("Finish and Submit")
        self.finishPushButton.clicked.connect(self.submitResponseAndWrite)
        self.finishPushButton.clicked.connect(self.closeMe)


        self.mainLayout.addWidget(self.infoLabel)
        self.mainLayout.addWidget(self.nameLineEdit)
        self.mainLayout.addLayout(self.attLayout)
        self.mainLayout.addWidget(self.finishPushButton, alignment=Qt.AlignCenter)
        self.mainLayout.addWidget(self.closePushButton, alignment=Qt.AlignCenter)


    def closeMe(self):
        self.accept()

    def submitResponseAndWrite(self):
        """
        Uses attributes to enter new player into the database
        """
        self.name = self.nameLineEdit.text()

        self.strengthCounter+=self.numberComboBox1.currentRating()
        self.charismaCounter+=self.numberComboBox2.currentRating()
        self.intelligenceCounter+=self.numberComboBox3.currentRating()
        self.dexterityCounter+=self.numberComboBox4.currentRating()

        self.totalCounter=int(self.strengthCounter+self.charismaCounter+self.intelligenceCounter+self.dexterityCounter)

        #Checking that only 20 points were allocated among the four attribute categories
        if self.totalCounter != 20:
            msg = "Error: Total points do not equal 20. Please reallocate points.\n"
            title = "Points not allocated correctly"
            QMessageBox.information(self, title, msg)

        #Adds player to the database by writing the information to a file that will then be read by the overseer
        else:
            msg = "Adding %s to player database...\n" % self.name
            title = "Player added!"
            QMessageBox.information(self, title, msg)

            self.db.insertPlayer(self.name, self.strengthCounter, self.charismaCounter, self.intelligenceCounter, self.dexterityCounter)





def main():
    app=App()
    sys.exit(app.exec_())


if(__name__ == "__main__"):
    main()
