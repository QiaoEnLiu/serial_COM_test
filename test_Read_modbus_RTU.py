#zh-tw 

"""
b'\x01\x06\x00\x01\x00\x00\xd8\n'
                ^       ^
             4001位址 傳輸值

"""


import minimalmodbus, time, traceback

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

try:
    while True:
        # 讀取Modbus暫存寄存器（Read from Holding Register）
        register_address = 4001

        # # 等待一些時間，模擬寫入數據
        # time.sleep(5)

        read_value = instrument.read_register(register_address,functioncode=3, signed=True)
        print(f"Read value from register {register_address}: {read_value}")

# except serial.SerialException as e:
#     print(f"Serial Exception: {e}")

except KeyboardInterrupt:
    # 當使用者按下Ctrl+C時結束
    print('Exiting...')

except Exception as e:
    print(f"Exception: {e}")
    traceback.print_exc()

finally:
    instrument.serial.close()
    print('COM port closed')    

