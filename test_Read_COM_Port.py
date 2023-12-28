#zh-tw
# 先透過RTU成功開啟COM3，然後在Python用COM4讀取，COM埠交換也可以，誰先開啟不影響，但這兩個COM埠必需為成對關系。

"""
b'\x01\x06\x00\x01\x00\x00\xd8\n'
                ^       ^
             4001位址 傳輸值
"""
import serial

# COM埠設定
ser = serial.Serial() 
try:
    ser.port = 'COM4'  # 這裡的COM4是示例，請更改為你實際使用的COM埠
    ser.baudrate = 9600
    ser.timeout = 1

    ser.open()
    print('COM port opened:', ser.port)
    while True:
        # 讀取COM埠數據
        data = ser.readline()
        if data:
            # 顯示讀取到的數據
            print(f'Received data: {data}')


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