# importing libraries
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
from VilgaxUART import *


class Window(QMainWindow):
    def __init__(self, image1):
        super().__init__()
        self.image1 = image1

        # setting title
        self.setWindowTitle("Module6-7 G.9")

        # setting geometry
        self.setGeometry(100, 100, 1280, 720)
        self.setStyleSheet("background-image: url(blackground.jpg)")

        # calling method
        self.UiComponents()

        # showing all the widgets
        self.show()


    def getName(self):
        print(self.image1)

        # method for widgets

    def UiComponents(self):

        # creating a push button
        # button_Connect = QPushButton("Connect", self)
        # # setting geometry of button
        # button_Connect.setGeometry(900, 100, 200, 40)
        # # adding action to a button
        # button_Connect.clicked.connect(self.click_Connect)

        # button_Connect.setStyleSheet("color: white")

        # creating a push button
        button_Home = QPushButton("Home/Stop", self)
        # setting geometry of button
        button_Home.setGeometry(900, 100, 200, 40)
        # adding action to a button
        button_Home.clicked.connect(self.click_Home)


        # creating a push button
        button_FindParts = QPushButton("Find Parts", self)
        # setting geometry of button
        button_FindParts.setGeometry(900, 150, 200, 40)
        # adding action to a button
        button_FindParts.clicked.connect(self.click_FindParts)


        # creating a push button
        button_Start = QPushButton("Start", self)
        # setting geometry of button
        button_Start.setGeometry(900, 200, 200, 40)
        # adding action to a button
        button_Start.clicked.connect(self.click_Start)


        # creating a push button
        button_Stop = QPushButton("Run", self)
        # setting geometry of button
        button_Stop.setGeometry(900, 250, 200, 40)
        # adding action to a button
        button_Stop.clicked.connect(self.click_Run)

        # creating a push button
        button_Stop = QPushButton("+", self)
        # setting geometry of button
        button_Stop.setGeometry(900, 300, 200, 40)
        # adding action to a button
        button_Stop.clicked.connect(self.up)

        # creating a push button
        button_Stop = QPushButton("-", self)
        # setting geometry of button
        button_Stop.setGeometry(900, 350, 200, 40)
        # adding action to a button
        button_Stop.clicked.connect(self.down)

        # creating a push button
        button_Showimg = QPushButton("Show", self)
        # setting geometry of button
        button_Showimg.setGeometry(900, 400, 200, 40)
        # adding action to a button
        button_Showimg.clicked.connect(self.Showimg)

        # show image
        # creating the check-box
        self.checkbox = QCheckBox('Geek ?', self)
        # setting geometry of check box
        self.checkbox.setGeometry(100, 100, 600, 600)
        # setting stylesheet
        # adding background image to indicator of check box
        # and changing with and height of indicator
        self.checkbox.setStyleSheet("QCheckBox::indicator"
                                    "{"
                                    "background-image : url(" + self.image1 + ".jpg);"
                                                                                         "width :600px;"
                                                                                         "height : 600px;"
                                                                                         "}")

        # action method

    def click_Home(self):
        self.image1 = "Home"
        self.checkbox.setGeometry(100, 100, 600, 600)
        self.checkbox.setStyleSheet("QCheckBox::indicator"
                                    "{"
                                    "background-image : url(Pic/" + self.image1 + ".jpg);"
                                                                                         "width :600px;"
                                                                                         "height : 600px;"
                                                                                         "}")
        self.getName()
        self.UiComponents()
        self.show()
        SetHome()

    def click_FindParts(self):
        cap = cv2.VideoCapture(0 + cv2.CAP_DSHOW)
        cap.set(3, 1280)  # set the resolution
        cap.set(4, 720)
        cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)
        ret, img = cap.read()
        cv2.imwrite('fieldimages/myfielddemo.png', img)
        cv2.imwrite('fieldimages/myfielddemo.jpg', img)
    def up(self):
        SetPositionZ(40, 70, 0)

    def down(self):
        SetPositionZ(10, 70, 0)

    def Showimg(self):
        self.image1 = "myfielddemo"
        self.checkbox.setGeometry(100, 100, 600, 600)
        self.checkbox.setStyleSheet("QCheckBox::indicator"
                                    "{"
                                    "background-image : url( fieldimages/" + self.image1 + ".jpg);"
                                                                                         "width :600px;"
                                                                                         "height : 600px;"
                                                                                         "}")
        self.getName()
        self.UiComponents()
        self.show()

    def click_Start(self):
        # print("Start")
        SetPositionZ(40, 70, 1)
        time.sleep(4)
        Capture()
        

    def click_Run(self):
        # print("Run")
        positionZ, anglesZ = PathFinder(x)

    def change_pic_sethome(self, Image1):
        self.image1 = Image1
        self.checkbox.setGeometry(100, 100, 600, 600)
        self.checkbox.setStyleSheet("QCheckBox::indicator"
                                    "{"
                                    "background-image : url(ImageForUI/" + self.image1 + ".jpg);"
                                                                                         "width :600px;"
                                                                                         "height : 600px;"
                                                                                         "}")
        self.getName()
        self.UiComponents()
        self.show()


# create pyqt5 app
App = QApplication(sys.argv)

# create the instance of our Window
window = Window("Home")

# start the app
sys.exit(App.exec())