#zh-tw
from pymodbus.client import ModbusSerialClient as ModbusClient
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.exceptions import ModbusException
import traceback

# COM埠設定
ser_port = 'COM4'  # 這裡的COM4是示例，請更改為你實際使用的COM埠
baud_rate = 9600
timeout = 1

# 建立 Modbus RTU client
modbus_client = ModbusClient(method='rtu', port=ser_port, baudrate=baud_rate, timeout=timeout)
modbus_client.connect()

try:
    # 使用 Modbus RTU client 進行讀取操作
    result = modbus_client.read_holding_registers(4001, 1, unit=0x01)

    if not result.isError():
        
        decoder = BinaryPayloadDecoder.fromRegisters(result.registers, byteorder='big')
        temperature_unit_code = decoder.decode_16bit_uint()

        if temperature_unit_code == 0:
            temperature_unit = 'Celsius'
        elif temperature_unit_code == 1:
            temperature_unit = 'Fahrenheit'
        else:
            temperature_unit = 'Unknown'
        print(f"Temperature Unit (4001): {temperature_unit}")
    else:
        print('Error:',result.isError())
        print("Failed to read Temperature Unit (4001)")

except KeyboardInterrupt:
    # 當使用者按下Ctrl+C時結束
    print('Exiting...')
    modbus_client.close()

except Exception as e:
    print(f"Exception: {e}")
    traceback.print_exc()

finally:
    modbus_client.close()  # 關閉 Modbus RTU 通信
    print('Modbus RTU client closed')
