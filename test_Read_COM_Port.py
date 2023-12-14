#zh-tw
#先透過RTU成功開啟COM3，然後在Python用COM4讀取，COM埠交換也可以，誰先開啟不影響，但這兩個COM埠必需為成對關系。

import serial

# COM埠設定
ser = serial.Serial() 
print('Prot:',ser.port)
try:
    ser.port = 'COM4'  # 這裡的COM4是示例，請更改為你實際使用的COM埠
    ser.baudrate = 9600
    ser.timeout = 1
    print('Prot:',ser.port)


    ser.open()
    while True:
        # 讀取COM埠數據
        data = ser.readline()
        
        # 顯示讀取到的數據
        print(f'Received data: {data}')

except KeyboardInterrupt:
    # 當使用者按下Ctrl+C時結束
    print('Exiting...')
    ser.close()
finally:
    ser.close()  # 確保在程式結束時關閉COM埠