import sys
import traceback
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import QTimer
from battery_info import showBatteryInfo

from imgResource import setButtonIcon, setLabelIcon, stateBatteryCharge_icons ,stateBattery_icons

class BatteryInfoApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('電池資訊')
        self.setGeometry(100, 100, 500, 600)  # 設定視窗大小和位置

        layout = QVBoxLayout()
        
        self.label = QLabel("取得電池資訊中...")
        layout.addWidget(self.label)

        self.setLayout(layout)
        
        # 使用 QTimer 定時刷新電池資訊
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateBatteryInfo)
        self.timer.start(1000)  # 每秒更新一次

        self.updateBatteryInfo()

    def updateBatteryInfo(self):
        try:
            battery_info = showBatteryInfo()
            self.label.setText(f"{battery_info[0]}, 電量: {battery_info[1]}%\n\r{battery_info[2]}")
            if battery_info[0]==2 or battery_info[0]==3:
                setLabelIcon(self.label, stateBatteryCharge_icons[5])
            else:

                if battery_info[1]<=10:
                    setLabelIcon(self.label, stateBatteryCharge_icons[0])
                elif battery_info[1]<=25:
                    setLabelIcon(self.label, stateBatteryCharge_icons[1])
                elif battery_info[1]<=50:
                    setLabelIcon(self.label, stateBatteryCharge_icons[2])
                elif battery_info[1]<=75:
                    setLabelIcon(self.label, stateBatteryCharge_icons[3])
                elif battery_info[1]<=100:
                    setLabelIcon(self.label, stateBatteryCharge_icons[4])

        except Exception as e:
            traceback.print_exc()
            self.label.setText(f"發生錯誤：{str(e)}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = BatteryInfoApp()
    ex.show()  # 顯示視窗
    sys.exit(app.exec_())
