import minimalmodbus
import time

# 定義Modbus裝置的串口通訊埠和地址
# 請根據實際情況更改這些參數
PORT = 'COM4'  # 更改為你的串口通訊埠
ADDRESS = 1  # 更改為你的Modbus裝置地址

# 創建ModbusInstrument物件
instrument = minimalmodbus.Instrument(PORT, ADDRESS, mode=minimalmodbus.MODE_RTU)

# 設置通訊參數（波特率、奇偶校驗等）
instrument.serial.baudrate = 9600
instrument.serial.bytesize = 8
instrument.serial.parity = minimalmodbus.serial.PARITY_NONE
instrument.serial.stopbits = 1
instrument.serial.timeout = 5  # 1秒的超時

# 讀取Modbus暫存寄存器（Read from Holding Register）
register_address = 0x01

# 等待一些時間，模擬寫入數據
time.sleep(5)

read_value = instrument.read_register(register_address)
print(f"Read value from register {register_address}: {read_value}")