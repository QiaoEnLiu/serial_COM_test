import sys, minimalmodbus, threading, PySQL, platform, traceback
from PyQt5.QtWidgets import QApplication, QLabel, QGridLayout, QLineEdit,\
    QWidget, QPushButton, QDesktopWidget, QMessageBox, QCheckBox
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont
import ProjectPublicVariable as PPV

font=QFont()
r4x_SQL_Cache={}
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
            font.setPointSize(20)
            self.setFixedSize(1920, 1080)

        mainLayout = QGridLayout()

        # self.reg1={}
        # self.reg3={}
        # self.reg4={}

        self.r1xLabel={}
        self.r3xLabel={}
        self.r4xLabel={}

        reg1_title=QLabel('R1X')
        reg1_title.setFont(font)
        reg1_act=QPushButton('Write_R1X')
        reg1_act.setFont(font)
        reg1_act.clicked.connect(self.sqlUpdateR1X)
        mainLayout.addWidget(reg1_title, 25, 0)
        mainLayout.addWidget(reg1_act, 25, 2)
        self.r1x_Checkbox={}
        for key,value in PPV.R1X_Mapping.items():
            defind=value
            defLabel=QLabel(defind)
            activate=QCheckBox()

            if defind =='':
                dataLabel=QLabel(defind)
                
            else:
                dataLabel=QLabel('NaN')

            self.r1xLabel[key]=dataLabel
            self.r1x_Checkbox[key]=activate

            defLabel.setFont(font)
            defLabel.setStyleSheet("background-color: pink;")
            dataLabel.setFont(font)
            dataLabel.setStyleSheet("background-color: pink;")
            activate.setFont(font)
            activate.setStyleSheet("background-color: pink;")

            dataLabel.setText(PySQL.selectSQL_Reg(1, key))
            if PySQL.selectSQL_Reg(1, key) == '1':
                # self.r1x_Checkbox[key].setText("Disable")
                self.r1x_Checkbox[key].setChecked(True)
            else:
                # self.r1x_Checkbox[key].setText("Enable")
                self.r1x_Checkbox[key].setChecked(False)

            mainLayout.addWidget(defLabel, key + 26, 0)
            mainLayout.addWidget(dataLabel, key + 26, 1)
            mainLayout.addWidget(activate, key + 26, 2)

            defLabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            dataLabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            # activate.setAlignment(Qt.AlignRight | Qt.AlignVCenter)


            # temp=[defind,dataLabel]
            # self.reg1[key]=temp


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
                self.r3xLabel[key]=dataLabel

            defLabel.setFont(font)
            defLabel.setStyleSheet("background-color: lightgreen;")
            dataLabel.setFont(font)
            dataLabel.setStyleSheet("background-color: lightgreen;")

            dataLabel.setText(PySQL.selectSQL_Reg(3, key))

            mainLayout.addWidget(defLabel, key + 1, 0)
            mainLayout.addWidget(dataLabel, key + 1, 1)

            defLabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            dataLabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

            # temp=[defind,dataLabel]
            # self.reg3[key]=temp

        reg4_title=QLabel('R4X')
        reg4_title.setFont(font)
        mainLayout.addWidget(reg4_title, 0 ,3)
        
        # inputBoxes={}
        # writeBtns={}

                
        for key,value in PPV.R4X_Mapping.items():
            defind=value
            defLabel=QLabel(defind)
            if defind =='':
                dataLabel=QLabel(defind)
            else:
                dataLabel=QLabel('NaN')
                inputBox=QLineEdit()
                send=QPushButton('Write_R4X')
                # inputBoxes[key]=inputBox
                # writeBtns[key]=send

                dataLabel.setText(PySQL.selectSQL_Reg(4, key))
                self.r4xLabel[key]=dataLabel
                send.clicked.connect(lambda checked, key = key, input=inputBox: self.sqlUpdateR4X(key ,input))

            defLabel.setFont(font)
            defLabel.setStyleSheet("background-color: lightblue;")
            dataLabel.setFont(font)
            dataLabel.setStyleSheet("background-color: lightblue;")

            dataLabel.setText(PySQL.selectSQL_Reg(4, key))
            inputBox.setFont(font)
            send.setFont(font)

            mainLayout.addWidget(defLabel, key + 1, 3)
            mainLayout.addWidget(dataLabel, key + 1, 4)
            mainLayout.addWidget(inputBox, key + 1, 5)
            mainLayout.addWidget(send, key + 1, 6)

            defLabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            dataLabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            inputBox.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

            # temp=[defind,dataLabel,inputBox,send]
            # self.reg4[key]=temp

        closeButton = QPushButton('Close')
        closeButton.clicked.connect(self.close)
        closeButton.setFont(font)


        mainLayout.addWidget(closeButton, 0, 6)

        mainLayout.setColumnStretch(0 ,1)
        mainLayout.setColumnStretch(1 ,1)
        mainLayout.setColumnStretch(2 ,1)
        mainLayout.setColumnStretch(3 ,1)
        # mainLayout.setColumnStretch(4 ,1)
        # mainLayout.setColumnStretch(5 ,1)
        # mainLayout.setColumnStretch(6 ,1)

        self.setLayout(mainLayout)

        # 使用 QTimer 定期更新 Modbus 數據
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.modbusUpdate)
        self.timer.start(1000)  # 更新頻率，每秒更新一次

        # print(self.reg1)
        # print(self.reg3)
        # print(self.reg4)

        self.setWindowTitle('PyQt5 Modbus Multi Reg')

    #region 
                

    def modbusUpdate(self):
      
        try:
            def read_thread():
                try:
                    #region Label讀取暫存SQL
                    for address, dataLabel in self.r1xLabel.items():
                        dataLabel.setText(PySQL.selectSQL_Reg(1, address))
                    for address, dataLabel in self.r3xLabel.items():
                        dataLabel.setText(PySQL.selectSQL_Reg(3, address))
                    for address, dataLabel in self.r4xLabel.items():
                        dataLabel.setText(PySQL.selectSQL_Reg(4, address))
                    #endregion

                    # print(PPV.instrument_ID1.read_bit(0,functioncode=1))

                    #region 讀取R1X（只要讀bit就好）
                    r1x = PPV.instrument_ID1.read_bits(0, 2, functioncode=1)

                    cache_R1X={}
                    for address, value in enumerate(r1x):
                        cache_R1X[address] = value

                    for address, value in cache_R1X.items():
                        if value != int(PySQL.selectSQL_Reg(regDF=1, regKey=address)): # modbus值與暫存SQL不一致，將暫存SQL寫入modbus
                            # PySQL.updateSQL_Reg(1, address, value)
                            PPV.instrument_ID1.write_bit(address, int(PySQL.selectSQL_Reg(regDF=1, regKey=address)))


                    #endregion

                    #region 讀取R3X
                    r3x_0_to_14={}
                    for address in PPV.R3X_Mapping:
                        if address < 16:
                            r3x_0_to_14[address]=PPV.instrument_ID1.read_float(address, functioncode=4)

                    r3x_16_to_20={i: None for i in range(16, 21)}
                    r3x_16_to_20_values=PPV.instrument_ID1.read_registers(min(r3x_16_to_20.keys()), len(r3x_16_to_20), 4)
                    for i, address in enumerate(r3x_16_to_20.keys()):
                        r3x_16_to_20[address] = r3x_16_to_20_values[i]

                    cache_R3X={**r3x_0_to_14, **r3x_16_to_20}
                    for address, value in cache_R3X.items():
                        # modbus值與暫存SQL不一致，將modbus值寫入暫存SQL
                        if address < 16 and value != float(PySQL.selectSQL_Reg(regDF=3, regKey=address)): 
                            PySQL.updateSQL_Reg(3, address, value)  
                        if address >= 16 and value != int(PySQL.selectSQL_Reg(regDF=3, regKey=address)):
                            PySQL.updateSQL_Reg(3, address, value)      

                    #endregion

                    #region 讀取R4X
                    # 讀取地址範圍為 0 到 15 的保持寄存器值
                    r4x_0_to_15 = PPV.instrument_ID1.read_registers(0, 15, functioncode=3)
                    # 讀取地址範圍為 16 的浮點數值
                    r4x_16 = PPV.instrument_ID1.read_float(16, functioncode=3)
                    # 讀取地址範圍為 18 到 26 的保持寄存器值
                    r4x_18_to_26 = PPV.instrument_ID1.read_registers(18, 8, functioncode=3)

                    # 將讀取的保持寄存器值合併為一個字典
                    cache_R4X = {}
                    for address, value in enumerate(r4x_0_to_15):
                        cache_R4X[address] = value

                    # 將地址 16 加入字典並視為浮點數
                    cache_R4X[16] = r4x_16

                    for address, value in enumerate(r4x_18_to_26, start=18):
                        cache_R4X[address] = value

                    # 將讀取的保持寄存器值與暫存資料表進行比對
                    for address, value in cache_R4X.items():
                        # modbus值與暫存SQL不一致，將暫存SQL值寫入modbus
                        # 由於離線時有更動暫存資料表，恢復連線後與modbus比對數值不一致，則將暫存資料表的值寫進modbus
                        if address == 16:
                            if PPV.instrument_ID1.read_float(address, functioncode=3) != float(PySQL.selectSQL_Reg(regDF=4, regKey=address)):
                                PPV.instrument_ID1.write_float(address, float(PySQL.selectSQL_Reg(regDF=4, regKey=address)), functioncode=6)
                        else:
                            if value != int(PySQL.selectSQL_Reg(regDF=4, regKey=address)):
                                PPV.instrument_ID1.write_register(address, int(PySQL.selectSQL_Reg(regDF=4, regKey=address)), functioncode=6) # 改成write_registers（functioncode =16）
                    #endregion
                    
                except minimalmodbus.NoResponseError as e:
                    print(f'(Connect Error) No response from the instrument: {e}')
                    # self.message_text(f'(Connect Error) No response from the instrument: {e}')
                except AttributeError as e: # 略過無法取得裝置變數的錯誤（因沒有埠號）
                    pass
                except Exception as e:
                    # print(f"An error occurred: {e}")
                    traceback.print_exc()
                    # print(f'Exception: {e}')
            # 建立一個新的執行緒並啟動
            modbus_thread = threading.Thread(target=read_thread)
            modbus_thread.start()
            
        except Exception as e:
            # print(f'(Reading Exception) Exception: {e}')
            traceback.print_exc()
            # self.message_text(f'(Reading Exception) Exception: {e}')
    #endregion

    def sqlUpdateR1X(self):
        print('R1X_Write')
        for address, checkBox in self.r1x_Checkbox.items():
            if checkBox.isChecked():
                PySQL.updateSQL_Reg(regDF=1, regKey= address, updateValue=1)
            else:
                PySQL.updateSQL_Reg(regDF=1, regKey= address, updateValue=0)
        

    def sqlUpdateR4X(self, key, input):
        PySQL.updateSQL_Reg(regDF=4, regKey= key, updateValue=input.text())
        # print(input.text())

   
            

            
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