import minimalmodbus
import serial.tools.list_ports

# 取得可用的 COM 埠列表
available_ports = list(serial.tools.list_ports.comports())

# 列印每個可用的 COM 埠
for port in available_ports:
    print(f"Available Port: {port.name}")

port_name = input('通訊埠：')

# COM3 的串列埠設定
serial_settings = {
    'port': port_name,
    'baudrate': 9600,
    'bytesize': 8,
    'parity': 'N',
    'stopbits': 1,
    'timeout': 2
}

# 建立串列埠物件
serial_port = minimalmodbus.Instrument(port_name, 1)  # 1 是 Modbus 地址

try:
    # 0 是寄存器地址，3 是功能碼（根據模擬軟體的設定）
    value = serial_port.read_register(0, functioncode=3)

    # 處理讀取到的數據
    print(f'Read value: {value}')

except Exception as e:
    print(f'Error: {e}')
