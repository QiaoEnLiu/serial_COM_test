import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QComboBox, QPushButton, QLabel
from PyQt5.QtCore import QTranslator, QLocale
from PyQt5.QtGui import QFont
font = QFont()
class LanguageSwitcher(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setFixedSize(800, 600)
        self.layout = QVBoxLayout()
        font.setPointSize(36)
        self.label = QLabel("Hello, World!", self)
        self.label.setFont(font)
        self.layout.addWidget(self.label)

        self.comboBox = QComboBox(self)
        self.comboBox.setFont(font)
        self.comboBox.addItem("English", "en")
        self.comboBox.addItem("中文", "zh")
        self.layout.addWidget(self.comboBox)

        self.button = QPushButton("Apply", self)
        self.button.setFont(font)
        self.button.clicked.connect(self.changeLanguage)
        self.layout.addWidget(self.button)

        self.setLayout(self.layout)

        self.translator = QTranslator()
        self.currentLanguage = 'en'

    def changeLanguage(self):
        selectedLanguage = self.comboBox.currentData()
        print("0")

        if self.currentLanguage != selectedLanguage:
            print("1")
            if selectedLanguage == 'zh':
                print("2")
                self.translator.load("lang/zh.qm")
            else:
                print("3")
                self.translator.load("lang/en.qm")

            QApplication.instance().installTranslator(self.translator)
            self.updateUI()
            self.currentLanguage = selectedLanguage

    def updateUI(self):
        print("4")
        self.label.setText(self.tr("Hello, World!"))
        self.button.setText(self.tr("Apply"))
        print("5")

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # 設置初始語言
    translator = QTranslator()
    translator.load("lang/en.qm")
    app.installTranslator(translator)

    ex = LanguageSwitcher()
    ex.setWindowTitle('Language Switcher')
    ex.show()

    sys.exit(app.exec_())
