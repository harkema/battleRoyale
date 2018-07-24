#!/usr/bin/python3

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys
import overseer


class App(QApplication):
    def __init__(self):
        """
        Main application
        """
        QApplication.__init__(self, sys.argv)
        self.setApplicationName("Battle Royale")
        self.mainWindow = MainWindow()
        self.mainWindow.show()

class MainWindow(QMainWindow):
    def __init__(self):
        """
        Main Window w/ option to enter a new player and start the battle"
        """

        QMainWindow.__init__(self)
        self.setWindowTitle("Main Menu")

        self.mainWidget = MainWidget()
        self.setCentralWidget(self.mainWidget)

        self.resize(200, 500)

class MainWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.mainLayout = QVBoxLayout(self)

        self.buttonLayout = QVBoxLayout()

        self.appFont = QFont("Arial", 14)


        #Button that opens quiz window for player to take
        self.newPlayerPushButton = QPushButton("Create a New Player")
        self.buttonLayout.addWidget(self.newPlayerPushButton)

        #Starts battle w/ characters that were entered
        self.startPushButton = QPushButton("Start battle!")

        self.viewPushButton = QPushButton("View All Players")
        self.buttonLayout.addWidget(self.viewPushButton)
        self.viewPushButton.clicked.connect(self.showView)

        self.deletePushButton = QPushButton("Delete Player")
        self.buttonLayout.addWidget(self.deletePushButton)
        self.deletePushButton.clicked.connect(self.deletePlayer)

        self.mainLayout.addLayout(self.buttonLayout)
        self.mainLayout.addStretch(0)
        self.mainLayout.addWidget(self.startPushButton)

        self.newPlayerPushButton.clicked.connect(self.showAttributes)
        self.startPushButton.clicked.connect(self.startBattle)

    def showAttributes(self):
        self.attributeDialog = AttributeDialog()
        self.attributeDialog.show()

    def showView(self):
        self.searchResults = overseer.BattleRoyale().retrievePlayerInfo()

        self.viewDialog = ViewDialog(self.searchResults)
        self.viewDialog.show()

    def deletePlayer(self):
        self.searchResults = overseer.BattleRoyale().retrievePlayerInfo()

        self.deleteDialog = DeleteDialog(self.searchResults)
        self.deleteDialog.show()

    def startBattle(self):
        self.searchResults = overseer.BattleRoyale().retrievePlayerInfo()

        self.startDialog = StartDialog(self.searchResults)
        self.startDialog.show()

class ResponseLabel(QLabel):
    def __init__(self, text, layout, row):
        QLabel.__init__(self, text)
        self.baseLayout=layout
        self.row=row
        self.column=0

        self.baseLayout.addWidget(self, self.row, self.column)

class QuestionLabel(QLabel):
    def __init__(self, text, layout, row):
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
        #self.scrollArea = scroll
        self.baseLayout.addWidget(self, self.row, 1)
        #self.scrollArea.setWidget(self)

    def currentRating(self):
        return self.currentIndex()

class StartDialog(QDialog):
    def __init__(self, results):
        QDialog.__init__(self)
        self.mainLayout = QVBoxLayout(self)

        self.startPushButton  = QPushButton("Start")
        self.closePushButton = QPushButton("Close")

        self.results = results

        self.questionLabel = QLabel("Start Battle With Following Players?")
        self.mainLayout.addWidget(self.questionLabel)

        self.playerTable = QTableWidget()

        self.playerTable.setColumnCount(5)
        self.playerTable.setHorizontalHeaderLabels(["Name", "Strength", "Charisma", "Intelligence", "Dexterity"])

        self.playerTable.setRowCount(len(self.results))

        self.mainLayout.addWidget(self.playerTable)

        colCount=0
        rowCount=0

        for row in self.results:
            for col in row:
                if col == row[0]:
                    continue

                self.cellWidget=QTableWidgetItem()
                self.cellWidget.setText(str(col))
                self.playerTable.setItem(rowCount, colCount, self.cellWidget)

                colCount+=1

                if colCount==5:
                    colCount=0
                    rowCount+=1


        self.startPushButton.clicked.connect(overseer.BattleRoyale().startBattle)
        self.closePushButton.clicked.connect(self.close)
        self.mainLayout.addWidget(self.startPushButton, alignment=Qt.AlignCenter)
        self.mainLayout.addWidget(self.closePushButton, alignment = Qt.AlignCenter)

    def close(self):
        self.accept()

class DeleteDialog(QDialog):
    def __init__(self, searchResults):
        QDialog.__init__(self)
        self.mainLayout = QVBoxLayout(self)
        self.selectionLayout = QVBoxLayout()

        self.results = searchResults

        self.genLabel=QLabel("Select Player(s) You Would Like to Delete\n")
        self.mainLayout.addWidget(self.genLabel)

        self.closePushButton=QPushButton("Close")

        self.deletePushButton=QPushButton("Delete")

        self.boxList=[]

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
        title="Delete Player?"

        for self.box in self.boxList:
            if self.box.isChecked():
                msg="Delete " +self.box.text()+"?"
                reply=QMessageBox.question(self, title, msg)

                if reply == QMessageBox.Yes:
                    pid = int(self.box.text().split(" ")[0])
                    overseer.BattleRoyale().deletePlayer(pid)
        self.close()

class ViewDialog(QDialog):
    def __init__(self, searchResults):
        QDialog.__init__(self)
        self.mainLayout = QVBoxLayout(self)
        self.results = searchResults

        self.resize(600, 500)

        self.closePushButton = QPushButton("Close")

        self.playerTable = QTableWidget()

        self.playerTable.setColumnCount(5)
        self.playerTable.setHorizontalHeaderLabels(["Name", "Strength", "Charisma", "Intelligence", "Dexterity"])

        self.playerTable.setRowCount(len(self.results))

        self.mainLayout.addWidget(self.playerTable)

        colCount=0
        rowCount=0

        for row in self.results:
            for col in row:
                if col == row[0]:
                    continue

                self.cellWidget=QTableWidgetItem()
                self.cellWidget.setText(str(col))
                self.playerTable.setItem(rowCount, colCount, self.cellWidget)

                colCount+=1

                if colCount==5:
                    colCount=0
                    rowCount+=1


        self.closePushButton.clicked.connect(self.close)
        self.mainLayout.addWidget(self.closePushButton, alignment=Qt. AlignCenter)

    def close(self):
        self.accept()

class AttributeDialog(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setSpacing(25)

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


    def closeMe(self):
        self.accept()

    def submitResponseAndWrite(self):
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

            with open("playerInfo.txt", mode="a") as playerInfo:
                playerInfo.write(self.name + ":" + str(self.strengthCounter) + ":" + str(self.charismaCounter) + ":" +  str(self.intelligenceCounter) + ":" + str(self.dexterityCounter) + "\n")

            playerInfo.close()


def main():
    app=App()
    sys.exit(app.exec_())


if(__name__ == "__main__"):
    main()
