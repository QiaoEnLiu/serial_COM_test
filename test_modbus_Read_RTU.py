#zh-tw 把此程式碼改成server端

from pymodbus.server import StartSerialServer
from pymodbus.device import ModbusDeviceIdentification

# COM埠設定
com_port = 'COM4'  # 這裡的COM3是示例，請更改為你實際使用的COM埠
baud_rate = 9600

# 啟動 Modbus RTU Serial Server
with StartSerialServer(
        port=com_port,
        identity=ModbusDeviceIdentification(),
        timeout=1) as server:
    
    # 在這裡處理 Modbus RTU Server 代碼
    # 例如，設定數據點、處理 Modbus 請求等等
    pass

