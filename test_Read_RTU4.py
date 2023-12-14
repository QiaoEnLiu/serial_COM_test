#zh-tw

from pymodbus.server.async_io import StartSerialServer
from pymodbus.device import ModbusDeviceIdentification
from serial import Serial
import serial.tools.list_ports

# 取得可用的 COM 埠列表
available_ports = list(serial.tools.list_ports.comports())

# 列印每個可用的 COM 埠
for port in available_ports:
    print(f"Available Port: {port.name}")

port_name = input('通訊埠：')

# 確認 COM 埠存在
if port_name not in [port.name for port in available_ports]:
    print(f"指定的通訊埠 {port_name} 不存在。")
else:
    print(f"指定的通訊埠 {port_name} 存在。")

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
serial_port = Serial(**serial_settings)

# 啟動 Modbus RTU Serial Server
with StartSerialServer(serial_port, framer=None, protocol=None, server=None, timeout=2) as server:
    # 在這裡執行你的 Modbus Server 代碼
    # 例如，設定數據點、處理 Modbus 請求等等
    pass
