#zh-tw 
import sys
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QComboBox, QHBoxLayout, QVBoxLayout, QWidget, QPushButton
from PyQt5.QtGui import QFont

class ModbusRTUConfigurator(QMainWindow):
    def __init__(self):
        super().__init__()

        self.serial_port = QSerialPort(self)  # 初始化 QSerialPort 實例

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Modbus RTU Configurator')
        self.setGeometry(100, 100, 960, 780)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        # COM Port
        com_layout = QHBoxLayout()
        com_label = QLabel('COM Port:')
        self.com_combo = QComboBox()
        self.populate_com_ports()
        com_layout.addWidget(com_label)
        com_layout.addWidget(self.com_combo)
        layout.addLayout(com_layout)

        # Baud Rate
        baud_layout = QHBoxLayout()
        baud_label = QLabel('Baud Rate:')
        self.baud_combo = QComboBox()
        self.baud_combo.addItems(['1200', '2400', '4800', '9600', '19200', '38400', '57600', '115200'])
        # 設定預設選項為 '9600'
        default_baud_rate = '9600'
        default_baud_index = self.baud_combo.findText(default_baud_rate)
        self.baud_combo.setCurrentIndex(default_baud_index)
        baud_layout.addWidget(baud_label)
        baud_layout.addWidget(self.baud_combo)
        layout.addLayout(baud_layout)

        # Data Bits
        data_bits_layout = QHBoxLayout()
        data_bits_label = QLabel('Data Bits:')
        self.data_bits_combo = QComboBox()
        self.data_bits_combo.addItems(['5', '6', '7', '8'])
        # 設定預設選項為 '8'
        default_data_bits = '8'
        default_data_bits_index = self.data_bits_combo.findText(default_data_bits)
        self.data_bits_combo.setCurrentIndex(default_data_bits_index)
        data_bits_layout.addWidget(data_bits_label)
        data_bits_layout.addWidget(self.data_bits_combo)
        layout.addLayout(data_bits_layout)

        # Stop Bits
        stop_bits_layout = QHBoxLayout()
        stop_bits_label = QLabel('Stop Bits:')
        self.stop_bits_combo = QComboBox()
    
        stop_bits_mapping = {
            '1': QSerialPort.OneStop,
            '1.5': QSerialPort.OneAndHalfStop,
            '2': QSerialPort.TwoStop,
        }
        for stop_bit, stop_bits_enum in stop_bits_mapping.items():
            self.stop_bits_combo.addItem(stop_bit, stop_bits_enum)
        # 設定預設選項為 '1'
        default_stop_bit = '1'
        default_stop_bit_index = self.stop_bits_combo.findText(default_stop_bit)
        self.stop_bits_combo.setCurrentIndex(default_stop_bit_index)
        
        stop_bits_layout.addWidget(stop_bits_label)
        stop_bits_layout.addWidget(self.stop_bits_combo)
        layout.addLayout(stop_bits_layout)

        # Parity
        parity_layout = QHBoxLayout()
        parity_label = QLabel('Parity:')
        self.parity_combo = QComboBox()
        self.parity_combo.addItems(['None', 'Even', 'Odd', 'Mark', 'Space'])
        # 設定預設選項為 'None'
        default_parity = 'None'
        default_parity_index = self.parity_combo.findText(default_parity)
        self.parity_combo.setCurrentIndex(default_parity_index)
        parity_layout.addWidget(parity_label)
        parity_layout.addWidget(self.parity_combo)
        layout.addLayout(parity_layout)

        # Connect Button
        self.connect_btn = QPushButton('Connect', self)
        self.connect_btn.clicked.connect(self.connect_serial)
        self.connect_btn.setVisible(True)
        layout.addWidget(self.connect_btn)

        # Disconnect Button (隱藏)
        self.disconnect_btn = QPushButton('Disconnect', self)
        self.disconnect_btn.clicked.connect(self.disconnect_serial)
        self.disconnect_btn.setVisible(False)
        layout.addWidget(self.disconnect_btn)

        central_widget.setLayout(layout)

        # 調整字型大小
        self.adjust_font_size()

    def populate_com_ports(self):
        com_ports = [port.portName() for port in QSerialPortInfo.availablePorts()]
        self.com_combo.addItems(com_ports)

    def connect_serial(self):
        com_port = self.com_combo.currentText()
        baud_rate = int(self.baud_combo.currentText())
        data_bits = int(self.data_bits_combo.currentText())
        stop_bits = self.stop_bits_combo.currentData()
        parity_text = self.parity_combo.currentText()
        parity = getattr(QSerialPort, f'Parity_{parity_text}' if parity_text != 'None' else 'NoParity')

        self.serial_port.setPortName(com_port)
        self.serial_port.setBaudRate(baud_rate)
        self.serial_port.setDataBits(data_bits)
        self.serial_port.setStopBits(stop_bits)
        self.serial_port.setParity(parity)

        if self.serial_port.open(QSerialPort.ReadWrite):
            print(f'Serial port {com_port} connected successfully!')
            self.connect_btn.setVisible(False)
            self.disconnect_btn.setVisible(True)
        else:
            print(f'Failed to connect to serial port {com_port}.')

    def adjust_font_size(self):
        font = QFont()
        font.setPointSize(36)  # 設置字型大小

        for widget in self.findChildren(QLabel):
            widget.setFont(font)

        for widget in self.findChildren(QPushButton):
            widget.setFont(font)

        for widget in self.findChildren(QComboBox):
            widget.setFont(font)

    def disconnect_serial(self):
        self.serial_port.close()
        print('Port Disconnect.')
        self.connect_btn.setVisible(True)
        self.disconnect_btn.setVisible(False)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ModbusRTUConfigurator()
    window.show()
    sys.exit(app.exec_())
