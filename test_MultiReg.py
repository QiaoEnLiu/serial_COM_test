import sys
import ProjectPublicVariable as PPV
from PyQt5.QtWidgets import QApplication, QLabel, QGridLayout, QLineEdit,QWidget,QPushButton,QDesktopWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

font=QFont()

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        # 取得螢幕解析度
        screen_resolution = QDesktopWidget().screenGeometry()
        screen_width, screen_height = screen_resolution.width(), screen_resolution.height()

        self.setFixedSize(480, 800)
        font.setPointSize(10)
        # 如果解析度為1920*1080，則全螢幕，否則使用固定解析度
        # if screen_width == 480 and screen_height == 800:
        #     font.setPointSize(10)
        #     self.showFullScreen()
        # else:
        #     font.setPointSize(24)
        #     self.setFixedSize(1920, 1080)

        mainLayout = QGridLayout()

        reg1={}
        reg3={}
        reg4={}

        reg1_title=QLabel('R1X')
        reg1_title.setFont(font)
        mainLayout.addWidget(reg1_title, 25, 0)
        for key,value in PPV.R1X_Mapping.items():
            defind=value
            defLabel=QLabel(defind)

            if defind =='':
                dataLabel=QLabel(defind)
            else:
                dataLabel=QLabel('1000.00')

            defLabel.setFont(font)
            defLabel.setStyleSheet("background-color: pink;")
            dataLabel.setFont(font)
            dataLabel.setStyleSheet("background-color: pink;")

            mainLayout.addWidget(defLabel, key + 26, 0)
            mainLayout.addWidget(dataLabel, key + 26, 1)

            defLabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            dataLabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

            temp=[defind,dataLabel]
            reg1[key]=temp


        reg3_title=QLabel('R3X')
        reg3_title.setFont(font)
        mainLayout.addWidget(reg3_title,0,0)
        for key,value in PPV.R3X_Mapping.items():
            defind=value
            defLabel=QLabel(defind)
            
            if defind =='':
                dataLabel=QLabel(defind)
            else:
                dataLabel=QLabel('1000.00')

            defLabel.setFont(font)
            defLabel.setStyleSheet("background-color: lightgreen;")
            dataLabel.setFont(font)
            dataLabel.setStyleSheet("background-color: lightgreen;")

            mainLayout.addWidget(defLabel, key + 1, 0)
            mainLayout.addWidget(dataLabel, key + 1, 1)

            defLabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            dataLabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

            temp=[defind,dataLabel]
            reg3[key]=temp

        reg4_title=QLabel('R4X')
        reg4_title.setFont(font)
        mainLayout.addWidget(reg4_title, 0 ,2)
        for key,value in PPV.R4X_Mapping.items():
            defind=value
            defLabel=QLabel(defind)
            if defind =='':
                dataLabel=QLabel(defind)
            else:
                dataLabel=QLabel('1000.00')
                inputBox=QLineEdit()
                send=QPushButton('Write')

            defLabel.setFont(font)
            defLabel.setStyleSheet("background-color: lightblue;")
            dataLabel.setFont(font)
            dataLabel.setStyleSheet("background-color: lightblue;")
            inputBox.setFont(font)
            send.setFont(font)

            mainLayout.addWidget(defLabel, key + 1, 2)
            mainLayout.addWidget(dataLabel, key + 1, 3)
            mainLayout.addWidget(inputBox, key + 1, 4)
            mainLayout.addWidget(send, key + 1, 5)

            defLabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            dataLabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            inputBox.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

            temp=[defind,dataLabel,inputBox,send]
            reg4[key]=temp

        mainLayout.setColumnStretch(0 ,1)
        mainLayout.setColumnStretch(1 ,1)
        mainLayout.setColumnStretch(2 ,1)
        mainLayout.setColumnStretch(3 ,1)
        # mainLayout.setColumnStretch(4 ,1)
        # mainLayout.setColumnStretch(5 ,1)
        # mainLayout.setColumnStretch(6 ,1)

        self.setLayout(mainLayout)

        self.setWindowTitle('PyQt5 Modbus Multi Reg')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())