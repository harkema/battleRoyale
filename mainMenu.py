#!/usr/bin/python3

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys


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

        self.resize(200, 200)



class MainWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.mainLayout = QVBoxLayout(self)

        self.buttonLayout = QVBoxLayout()

        self.appFont = QFont("Arial", 14)

        #Button that opens quiz window for player to take
        self.newPlayerPushButton = QPushButton("Create a new player")
        self.buttonLayout.addWidget(self.newPlayerPushButton)

        #Starts battle w/ characters that were entered
        self.startPushbutton = QPushButton("Start battle!")
        self.buttonLayout.addWidget(self.startPushbutton)

        self.mainLayout.addLayout(self.buttonLayout)

        self.newPlayerPushButton.clicked.connect(self.showQuiz)

    def showQuiz(self):
        self.quizDialog = QuizDialog()
        self.quizDialog.show()

class ResponseLabel(QLabel):
    def __init__(self, text, layout, row):
        QLabel.__init__(self, text)
        self.baseLayout=layout
        self.row=row
        self.column=0
        #self.scrollArea = scroll
        self.baseLayout.addWidget(self, self.row, self.column)
        #self.scrollArea.setWidget(self)


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

        self.row=row
        self.column=1
        #self.scrollArea = scroll
        self.baseLayout.addWidget(self, self.row, 1)
        #self.scrollArea.setWidget(self)

    def currentRating(self):
        return self.currentIndex()

class QuizDialog(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setSpacing(25)

        #Layout w/ scenarios
        self.quizLayout = QGridLayout()
        self.quizLayout.setVerticalSpacing(25)

        #self.menuScrollArea = QScrollArea()
        #self.menuScrollArea.setWidgetResizable(True)

        #Default widget created -> scollAreaWidgetContents

        self.strengthCounter = 0;
        self.charismaCounter= 0;
        self.intelligenceCounter = 0;
        self.dexterityCounter = 0;

        self.appFont = QFont("Arial", 14)

        self.nameLineEdit = QLineEdit("Enter Name");

        self.infoLabel = QLabel("For each scenario, respond with the most\nlikely way in which you would respond.\nDo this by numbering each response 0-3,\n0 being the most unlikely and 3\nbeing the most likely way\nin which you would respond.")
        self.infoLabel.setFont(QFont("Arial", 14))

        self.mainLayout.addStretch()


        #######################
        #Question1
        ########################


        #Creating scenario labels
        self.qOneLabel = QuestionLabel("Question 1?", self.quizLayout, 0)

        #Creating Response labels and their combo boxes
        self.r1Label = ResponseLabel("R1", self.quizLayout, 1)
        self.numberComboBox1 = NumberComboBox(self.quizLayout, 1)



        self.r2label = ResponseLabel("R2", self.quizLayout, 2)
        self.numberComboBox2 = NumberComboBox(self.quizLayout, 2)


        self.r3label = ResponseLabel("R3", self.quizLayout, 3)
        self.numberComboBox3 = NumberComboBox(self.quizLayout, 3)


        self.r4label = ResponseLabel("R4", self.quizLayout, 4)
        self.numberComboBox4 = NumberComboBox(self.quizLayout, 4)


        #######################
        #Question2
        ########################
        #Creating scenario labels
        self.qTwoLabel = QuestionLabel("Question 2?", self.quizLayout, 5)

        #Creating Response labels and their combo boxes
        self.r5Label = ResponseLabel("R1", self.quizLayout, 6)
        self.numberComboBox5 = NumberComboBox(self.quizLayout, 6)

        self.r6label = ResponseLabel("R2", self.quizLayout, 8)
        self.numberComboBox6 = NumberComboBox(self.quizLayout, 8)

        self.r7label = ResponseLabel("R3", self.quizLayout, 10)
        self.numberComboBox7 = NumberComboBox( self.quizLayout,10)

        self.r8label = ResponseLabel("R4", self.quizLayout, 11)
        self.numberComboBox8 = NumberComboBox(self.quizLayout, 11)

        """
        #######################
        #Question3
        ########################
        #Creating scenario labels
        self.qTwoLabel = QuestionLabel("Question 3?", self.quizLayout, 12)

        #Creating Response labels and their combo boxes
        self.r5Label = ResponseLabel("R1", self.quizLayout, 13)
        self.numberComboBox = NumberComboBox(self.numberData, self.quizLayout, 13)

        self.r6label = ResponseLabel("R2", self.quizLayout, 14)
        self.numberComboBox = NumberComboBox(self.numberData, self.quizLayout, 14)

        self.r7label = ResponseLabel("R3", self.quizLayout, 15)
        self.numberComboBox = NumberComboBox(self.numberData, self.quizLayout, 15)

        self.r8label = ResponseLabel("R4", self.quizLayout, 16)
        self.numberComboBox = NumberComboBox(self.numberData, self.quizLayout, 16)
        """


        self.closePushButton = QPushButton("Close")
        self.closePushButton.clicked.connect(self.closeMe)

        self.finishPushButton = QPushButton("Finish and Submit")
        self.finishPushButton.clicked.connect(self.submitResponseAndWrite)
        self.finishPushButton.clicked.connect(self.closeMe)


        self.mainLayout.addWidget(self.infoLabel)
        self.mainLayout.addWidget(self.nameLineEdit)
        self.mainLayout.addLayout(self.quizLayout)
        self.mainLayout.addWidget(self.finishPushButton, alignment=Qt.AlignCenter)
        self.mainLayout.addWidget(self.closePushButton, alignment=Qt.AlignCenter)


    def closeMe(self):
        self.accept()

    def submitResponseAndWrite(self):
        self.name = self.nameLineEdit.text()

        self.strengthCounter+=self.numberComboBox1.currentRating()+self.numberComboBox5.currentRating()
        self.charismaCounter+=self.numberComboBox2.currentRating()+self.numberComboBox6.currentRating()
        self.intelligenceCounter+=self.numberComboBox3.currentRating()+self.numberComboBox7.currentRating()
        self.dexterityCounter+=self.numberComboBox4.currentRating()+self.numberComboBox8.currentRating()

        with open("playerInfo.txt", mode="a") as playerInfo:
            playerInfo.write(self.name + ":" + str(self.strengthCounter) + ":" + str(self.charismaCounter) + ":" +  str(self.intelligenceCounter) + ":" + str(self.dexterityCounter) + "\n")

        playerInfo.close()





def main():
    app=App()
    sys.exit(app.exec_())


if(__name__ == "__main__"):
    main()
