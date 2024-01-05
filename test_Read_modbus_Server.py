#zh-tw
from pymodbus.server.async_io import StartSerialServer
from pymodbus.transaction import ModbusRtuFramer
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusSlaveContext, ModbusServerContext
from pymodbus.payload import BinaryPayloadDecoder
from twisted import internet
import traceback

# COM埠設定
ser_port = 'COM4'  # 這裡的COM4是示例，請更改為你實際使用的COM埠
baud_rate = 9600
data_bits = 8
stop_bits = 1  # 1 表示 One Stop Bit
parity = 'N'
timeout = 5

reg_address = 2

# 創建 Modbus Server 的資料存儲
hr = ModbusSequentialDataBlock(0, [0] * 100)
store = ModbusSlaveContext(
    di=ModbusSequentialDataBlock.create(),
    co=ModbusSequentialDataBlock.create(),
    hr=hr,  # 100 個保持寄存器的起始地址從 0 開始
    ir=ModbusSequentialDataBlock.create()
)

context = ModbusServerContext(slaves=store, single=True)
print(context)

try:
    print('Before StartSerialServer')
    # 使用 Twisted 框架的 reactor 啟動 Modbus RTU Server
    factory = StartSerialServer(context=context, framer=ModbusRtuFramer)
    print('Pass0')
    internet.reactor.listenSerial(port=ser_port, baudrate=baud_rate, bytesize=data_bits, parity=parity, stopbits=stop_bits, factory=factory)
    internet.reactor.run()

    print('After StartSerialServer')
    print('Pass1')

    # 使用 Modbus RTU client 進行讀取操作
    result = context[0].getValues(3, reg_address, count=1, unit=0x00)
    print('Pass2')
    decoder = BinaryPayloadDecoder.fromRegisters(result, byteorder='big')
    print('Pass3')
    temperature_unit_code = decoder.decode_16bit_uint()

    if temperature_unit_code == 0:
        temperature_unit = 'Celsius'
    elif temperature_unit_code == 1:
        temperature_unit = 'Fahrenheit'
    else:
        temperature_unit = 'Unknown'
    print(f"Temperature Unit ({reg_address}): {temperature_unit}")

except KeyboardInterrupt:
    # 當使用者按下 Ctrl+C 時結束
    print('Exiting...')
    internet.reactor.stop()

except Exception as e:
    print(f"Exception: {type(e)} - {e}")
    traceback.print_exc()

finally:
    print('Modbus RTU Server closed')
