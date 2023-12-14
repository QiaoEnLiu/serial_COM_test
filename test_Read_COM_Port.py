import serial

# COM埠設定
ser = serial.Serial()  # 這裡的COM3和9600是示例，請更改為你實際使用的COM埠和波特率
print('Prot:',ser.port)
try:
    ser.port = 'COM3'  # 這裡的COM3是示例，請更改為你實際使用的COM埠
    ser.baudrate = 9600
    ser.timeout = 1
    print('Prot:',ser.port)


    ser.open()
    while True:
        # 讀取COM埠數據
        data = ser.readline().decode('utf-8').strip()
        
        # 顯示讀取到的數據
        print(f'Received data: {data}')

except KeyboardInterrupt:
    # 當使用者按下Ctrl+C時結束
    print('Exiting...')
    ser.close()
finally:
    ser.close()  # 確保在程式結束時關閉COM埠