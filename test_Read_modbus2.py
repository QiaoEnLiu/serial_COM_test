from pymodbus.server import StartSerialServer
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore.store import ModbusSlaveContext, ModbusServerContext
from pymodbus.transaction import FifoTransactionManager
from pymodbus.transaction import ModbusRtuFramer
from pymodbus.client import ModbusSerialClient as ModbusClient
import logging

# 設定 Modbus RTU 串口相關參數
COM_PORT = 'COM4'  # 根據實際情況更改
BAUDRATE = 9600
PARITY = 'N'
STOPBITS = 1
BYTESIZE = 8

# 定義 Modbus RTU 伺服器資料存儲
store = ModbusSlaveContext(
    di=ModbusSequentialDataBlock.create(),
    co=ModbusSequentialDataBlock.create(),
    hr=ModbusSequentialDataBlock.create(),
    ir=ModbusSequentialDataBlock.create()
)
context = ModbusServerContext(slaves=store, single=True)

# 定義 Modbus RTU 伺服器識別信息
identity = ModbusDeviceIdentification()
identity.VendorName = 'Pymodbus'
identity.ProductCode = 'PM'
identity.VendorUrl = 'http://github.com/riptideio/pymodbus/'
identity.ProductName = 'Pymodbus Server'
identity.ModelName = 'Pymodbus Server'
identity.MajorMinorRevision = '2.3.0'

# 定義 Modbus RTU 伺服器
server = StartSerialServer(
    context,
    framer=ModbusRtuFramer,
    identity=identity,
    port=COM_PORT,
    baudrate=BAUDRATE,
    bytesize=BYTESIZE,
    parity=PARITY,
    stopbits=STOPBITS,
)

# 啟動 Modbus RTU 伺服器
try:
    print("Modbus RTU Server is running...")
    server.serve_forever()

except KeyboardInterrupt:
    print("Modbus RTU Server is shutting down...")
    server.shutdown()
    server.server_close()
