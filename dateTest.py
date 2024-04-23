import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QDateEdit, QCalendarWidget
from PyQt5.QtCore import QDate

class DateEditExample(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('QDateEdit Example')

        layout = QVBoxLayout()

        # 創建一個QDateEdit小部件
        self.dateEdit = QDateEdit(self)
        
        # 啟用彈出日曆功能
        self.dateEdit.setCalendarPopup(True)
        
        # 使用自定義的日曆小部件
        calendar = QCalendarWidget(self)
        self.dateEdit.setCalendarWidget(calendar)
        
        # 設置日期為當前日期
        self.dateEdit.setDate(QDate.currentDate())

        layout.addWidget(self.dateEdit)
        layout.addStretch()
        self.setLayout(layout)
        
        # 設置視窗大小
        self.resize(400, 250)


        # 連接日期更改信號到自定義的槽函數
        # self.dateEdit.dateChanged.connect(self.dateChanged)

    # def dateChanged(self, date):
    #     print(f'Date changed: {date}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DateEditExample()
    window.show()
    sys.exit(app.exec_())
