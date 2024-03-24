import sys, minimalmodbus, threading, PySQL, platform
from PyQt5.QtWidgets import QApplication, QLabel, QGridLayout, QLineEdit,\
    QWidget, QPushButton, QDesktopWidget, QMessageBox
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont
import ProjectPublicVariable as PPV

font=QFont()

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        print(platform.system())

        # 取得螢幕解析度
        screen_resolution = QDesktopWidget().screenGeometry()
        screen_width, screen_height = screen_resolution.width(), screen_resolution.height()

        # self.setFixedSize(480, 800)
        # font.setPointSize(10)
        # 如果解析度為1920*1080，則全螢幕，否則使用固定解析度
        if screen_width == 800 and screen_height == 480:
            font.setPointSize(10)
            self.showFullScreen()
        else:
            font.setPointSize(24)
            self.setFixedSize(1920, 1080)

        mainLayout = QGridLayout()

        self.reg1={}
        self.reg3={}
        self.reg4={}

        reg1_title=QLabel('R1X')
        reg1_title.setFont(font)
        mainLayout.addWidget(reg1_title, 25, 0)
        for key,value in PPV.R1X_Mapping.items():
            defind=value
            defLabel=QLabel(defind)

            if defind =='':
                dataLabel=QLabel(defind)
            else:
                dataLabel=QLabel('NaN')

            defLabel.setFont(font)
            defLabel.setStyleSheet("background-color: pink;")
            dataLabel.setFont(font)
            dataLabel.setStyleSheet("background-color: pink;")

            dataLabel.setText(PySQL.selectSQL_Reg(1, key))

            mainLayout.addWidget(defLabel, key + 26, 0)
            mainLayout.addWidget(dataLabel, key + 26, 1)

            defLabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            dataLabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

            temp=[defind,dataLabel]
            self.reg1[key]=temp


        reg3_title=QLabel('R3X')
        reg3_title.setFont(font)
        mainLayout.addWidget(reg3_title,0,0)
        for key,value in PPV.R3X_Mapping.items():
            defind=value
            defLabel=QLabel(defind)
            
            if defind =='':
                dataLabel=QLabel(defind)
            else:
                dataLabel=QLabel('NaN')

            defLabel.setFont(font)
            defLabel.setStyleSheet("background-color: lightgreen;")
            dataLabel.setFont(font)
            dataLabel.setStyleSheet("background-color: lightgreen;")

            dataLabel.setText(PySQL.selectSQL_Reg(3, key))

            mainLayout.addWidget(defLabel, key + 1, 0)
            mainLayout.addWidget(dataLabel, key + 1, 1)

            defLabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            dataLabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

            temp=[defind,dataLabel]
            self.reg3[key]=temp

        reg4_title=QLabel('R4X')
        reg4_title.setFont(font)
        mainLayout.addWidget(reg4_title, 0 ,2)
        for key,value in PPV.R4X_Mapping.items():
            defind=value
            defLabel=QLabel(defind)
            if defind =='':
                dataLabel=QLabel(defind)
            else:
                dataLabel=QLabel('NaN')
                inputBox=QLineEdit()
                send=QPushButton('Write')

            defLabel.setFont(font)
            defLabel.setStyleSheet("background-color: lightblue;")
            dataLabel.setFont(font)
            dataLabel.setStyleSheet("background-color: lightblue;")

            dataLabel.setText(PySQL.selectSQL_Reg(4, key))
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
            self.reg4[key]=temp

        closeButton = QPushButton('Close')
        closeButton.clicked.connect(self.close)
        closeButton.setFont(font)


        mainLayout.addWidget(closeButton, 0, 5)

        mainLayout.setColumnStretch(0 ,1)
        mainLayout.setColumnStretch(1 ,1)
        mainLayout.setColumnStretch(2 ,1)
        mainLayout.setColumnStretch(3 ,1)
        # mainLayout.setColumnStretch(4 ,1)
        # mainLayout.setColumnStretch(5 ,1)
        # mainLayout.setColumnStretch(6 ,1)

        self.setLayout(mainLayout)

        # 使用 QTimer 定期更新 Modbus 數據
        # self.timer = QTimer(self)
        # self.timer.timeout.connect(self.modbusUpdate)
        # self.timer.start(1000)  # 更新頻率，每秒更新一次

        # print(self.reg1)
        # print(self.reg3)
        # print(self.reg4)

        self.setWindowTitle('PyQt5 Modbus Multi Reg')

    def modbusUpdate(self):
        try:
            def read_thread():
                try:
                    r1x = PPV.instrument_ID1.read_registers(0, 1, functioncode=3)


                    # 讀取地址範圍為 0 到 15 的保持寄存器值
                    r4x_0_to_15 = PPV.instrument_ID1.read_registers(0, 15, functioncode=3)

                    # 讀取地址範圍為 16 的浮點數值
                    r4x_16 = PPV.instrument_ID1.read_float(16, functioncode=3)

                    # 讀取地址範圍為 18 到 26 的保持寄存器值
                    r4x_18_to_26 = PPV.instrument_ID1.read_registers(18, 8, functioncode=3)

                    cache_R1X={}
                    for address, value in enumerate(r1x):
                        cache_R1X[address] = value



                    # 將讀取的保持寄存器值合併為一個字典
                    cache_R4X = {}
                    for address, value in enumerate(r4x_0_to_15):
                        cache_R4X[address] = value

                    # 將地址 16 加入字典並視為浮點數
                    cache_R4X[16] = r4x_16

                    for address, value in enumerate(r4x_18_to_26, start=18):
                        cache_R4X[address] = value

                    for key, value in cache_R1X.items():
                        if value != int(PySQL.selectSQL_Reg(regDF=1, regKey=key)):
                            PPV.instrument_ID1.write_register(key, int(PySQL.selectSQL_Reg(regDF=1, regKey=key)), functioncode=6)

                    # 將讀取的保持寄存器值與暫存資料表進行比對
                    for key, value in cache_R4X.items():
                        # 由於離線時有更動暫存資料表，恢復連線後與modbus比對數值不一致，則將暫存資料表的值寫進modbus
                        if key == 16:
                            if PPV.instrument_ID1.read_float(key, functioncode=3) != float(PySQL.selectSQL_Reg(regDF=4, regKey=key)):
                                PPV.instrument_ID1.write_float(key, float(PySQL.selectSQL_Reg(regDF=4, regKey=key)), functioncode=6)
                        else:
                            if value != int(PySQL.selectSQL_Reg(regDF=4, regKey=key)):
                                PPV.instrument_ID1.write_register(key, int(PySQL.selectSQL_Reg(regDF=4, regKey=key)), functioncode=6)
                    
                except minimalmodbus.NoResponseError as e:
                    print(f'(Connect Error) No response from the instrument: {e}')
                    # self.message_text(f'(Connect Error) No response from the instrument: {e}')
                except AttributeError as e: # 略過無法取得裝置變數的錯誤（因沒有埠號）
                    pass
                except Exception as e:
                    print(f'Exception: {e}')
            # 建立一個新的執行緒並啟動
            modbus_thread = threading.Thread(target=read_thread)
            modbus_thread.start()
            

        except Exception as e:
            print(f'(Reading Exception) Exception: {e}')
            # self.message_text(f'(Reading Exception) Exception: {e}')
            
    # def readR3x(self):
    #     try:
    #         def read_thread():
    #             try:
    #                 read = PPV.instrument_3x.read_registers(0,20,functioncode=4)
    #                 print(read)
    #             except minimalmodbus.NoResponseError as e:
    #                 print(f'(Connect Error) No response from the instrument: {e}')
    #                 # self.message_text(f'(Connect Error) No response from the instrument: {e}')
    #             except Exception as e:
    #                 print(f'Exception: {e}')
    #         # 建立一個新的執行緒並啟動
    #         modbus_thread = threading.Thread(target=read_thread)
    #         modbus_thread.start()
            

    #     except Exception as e:
    #         print(f'(Reading Exception) Exception: {e}')
    #         # self.message_text(f'(Reading Exception) Exception: {e}')
            
    #region 關閉程式警告視窗
    def close(self):
        # 顯示確認對話框
        reply = QMessageBox.question(self, '程式關閉', '確定要關閉程式嗎？',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            # 如果用戶選擇 "Yes"，則關閉應用程式
            # response.close()
            QApplication.quit()

    #endregion

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())