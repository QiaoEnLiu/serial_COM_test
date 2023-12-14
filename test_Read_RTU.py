#zh-tw

import minimalmodbus, serial, serial.tools.list_ports
from pymodbus.server.async_io import StartSerialServer

from serial import Serial

# 取得可用的 COM 埠列表
available_ports = list(serial.tools.list_ports.comports())

# 列印每個可用的 COM 埠
for port in available_ports:
    print(f"Available Port: {port.name}")

portName=input('通訊埠：')#COM3, COM4

# COM3 的串列埠設定
serial_settings = {
    'port': portName,
    'baudrate': 9600,
    'bytesize': 8,
    'parity': 'N',
    'stopbits': 1,
    'timeout': 2
}

# 建立串列埠物件
serial_port = Serial(**serial_settings)

# 啟動 Modbus RTU Serial Server
with StartSerialServer(serial_settings, framer=None, protocol=None, server=None, timeout=2, **serial_settings) as server:
    # 在這裡執行你的 Modbus Server 代碼
    # 例如，設定數據點、處理 Modbus 請求等等

    instrument = minimalmodbus.Instrument(portName, 1)

    try:
        # 0 是寄存器地址，3 是功能碼（根據模擬軟體的設定）
        value = instrument.read_register(0, functioncode=3)

        # 處理讀取到的數據
        print(f'Read value: {value}')

    except Exception as e:
        print(f'Error: {e}')

    pass

#這是com0com的載點：https://sourceforge.net/projects/com0com/