#zh-tw
# 先透過RTU成功開啟COM3，然後在Python用COM4讀取，COM埠交換也可以，誰先開啟不影響，但這兩個COM埠必需為成對關系。

"""
b'\x01\x06\x00\x01\x00\x00\xd8\n'
                ^       ^
             4001位址 傳輸值
"""
import serial

def modify_modbus_message(original_message, new_value):
    # 修改訊息的數值部分
    modified_message = original_message[:6] + new_value.to_bytes(2, byteorder='big') + original_message[8:]
    return modified_message

# 原始 Modbus RTU 訊息
original_message = b'\x01\x06\x00\x01\x00\x00\xd8\n'

# 設定新的數值
new_value = 2

# 修改訊息
modified_message = modify_modbus_message(original_message, new_value)

# COM埠設定
ser = serial.Serial() 
try:
    ser.port = 'COM4'
    ser.baudrate = 9600
    ser.timeout = 1

    ser.open()
    print('COM port opened:', ser.port)

    # 寫入修改後的訊息
    ser.write(modified_message)
    print('Writing Done')



except serial.SerialException as e:
    print(f"Serial Exception: {e}")

except KeyboardInterrupt:
    # 當使用者按下Ctrl+C時結束
    print('Exiting...')
    ser.close()

except Exception as e:
    print(f"Exception: {e}")

finally:
    ser.close()  # 確保在程式結束時關閉COM埠
    print('COM port closed')