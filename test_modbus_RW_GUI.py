#zh-tw 
import minimalmodbus, threading
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit
from PyQt5.QtCore import QTimer, Qt, QObject, pyqtSignal


# 初始化 Modbus 裝置
instrument = minimalmodbus.Instrument('COM4', 1)
instrument.serial.baudrate = 9600
instrument.serial.parity = minimalmodbus.serial.PARITY_NONE
instrument.serial.stopbits = 1
instrument.serial.timeout = 1.0 # 設定串口通信的超時時間，單位是秒

class ModbusReaderApp(QWidget):
    # 定義一個信號，用於將 Modbus 值傳遞到主線程更新 UI
    update_signal = pyqtSignal(float)
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Modbus Reader')
        self.setGeometry(100, 100, 1080, 750)

        # 創建 QLabel 用於顯示 Modbus 數據
        self.label = QLabel('Modbus Value: N/A', self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("font-size: 48px;")

        # 創建 QLineEdit 用於輸入
        self.input_line_edit = QLineEdit(self)
        self.input_line_edit.setPlaceholderText('Enter value for Slaver')
        self.input_line_edit.setStyleSheet("font-size: 36px;")

        # 創建 QPushButton 用於觸發傳送值至 Slaver
        self.send_button = QPushButton('Send to Slaver', self)
        self.send_button.clicked.connect(self.send_value_to_slaver)
        self.send_button.setStyleSheet("font-size: 36px;")
        
        self.text_edit=QTextEdit(self)
        self.text_edit.setStyleSheet("font-size: 24px;")

        # 設置布局
        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.input_line_edit)
        layout.addWidget(self.send_button)
        layout.addWidget(self.text_edit)

        # 使用 QTimer 定期更新 Modbus 數據
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_modbus_data)
        self.timer.start(1000)  # 更新頻率，每秒更新一次

        # 連接信號和槽
        self.update_signal.connect(self.update_modbus_ui)

    def update_modbus_data(self):
        try:
            def read_thread():
                try:
                    # 讀取浮點數值，地址為1
                    register_address = 2
                    value_read_float = instrument.read_float(register_address)
                    self.update_signal.emit(value_read_float)

                except minimalmodbus.NoResponseError as e:
                    print(f'(Connect Error) No response from the instrument: {e}')
                    self.message_text(f'(Connect Error) No response from the instrument: {e}')
                except Exception as e:
                    print(f'Exception: {e}')
            # 建立一個新的執行緒並啟動
            modbus_thread = threading.Thread(target=read_thread)
            modbus_thread.start()
            

        except Exception as e:
            print(f'(Reading Exception) Exception: {e}')
            self.message_text(f'(Reading Exception) Exception: {e}')

    def send_value_to_slaver(self):
        try:
            # 從 QLineEdit 中獲取值，並將其轉換為浮點數
            value_to_send = float(self.input_line_edit.text())
            # 寫入 Modbus 設備，地址為2（假設這是 Slaver 接收數據的地址）
            register_address = 2
            instrument.write_float(register_address, value_to_send)
            print(f'Successfully sent value to Slaver: {value_to_send}')
            self.message_text(f'Successfully sent value to Slaver: {value_to_send}')
        except ValueError:
            print('Invalid input. Please enter a valid float value.')
            self.message_text('Invalid input. Please enter a valid float value.')
        except minimalmodbus.NoResponseError as e:
            print(f'(Connect Error) No response from the instrument: {e}')
            self.message_text(f'(Connect Error) No response from the instrument: {e}')
        except Exception as e:
            print(f'(Writing Exception) Exception: {e}')
            self.message_text(f'(Writing Exception) Exception: {e}')


    def message_text(self,text):
        self.text_edit.append(text)

    def update_modbus_ui(self, value):
        self.label.setText(f'Modbus Value: {value:.2f}')
        print(f'Modbus Value: {value:.2f}')
        self.message_text(f'Modbus Value: {value:.2f}')


if __name__ == '__main__':
    app = QApplication([])
    window = ModbusReaderApp()
    window.show()
    app.exec_()
