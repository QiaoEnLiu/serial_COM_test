import minimalmodbus, traceback, time

try:
    # 定義Modbus裝置的串口及地址
    instrument = minimalmodbus.Instrument('COM4', 1)  
    # 第一個參數是串口，第二個參數是Modbus地址

    # 設定串口波特率，Parity和Stop bits（這些參數需與Modbus設備一致）
    instrument.serial.baudrate = 9600
    instrument.serial.parity = minimalmodbus.serial.PARITY_NONE
    instrument.serial.stopbits = 1

    while True:
        # 讀取浮點數值，地址為1
        register_address = int(input('Input Address: '))

        try:
            time.sleep(1)
            if register_address == 0:
                value_read = instrument.read_register(register_address)
                print(f"成功讀取浮點數值：{value_read}")
            elif register_address == 1:
                # 使用read_float()方法讀取數據
                value_read = instrument.read_float(register_address) #functioncode = 3 or 4
                print(f"成功讀取浮點數值：{round(value_read,2)}")
        except minimalmodbus.NoResponseError as e:
            print(f"No response from the instrument: {e}")
            traceback.print_exc()

        time.sleep(1)
    
except KeyboardInterrupt:
    # 當使用者按下Ctrl+C時結束
    print('Exiting...')

except Exception as e:
    print(f"Exception: {e}")
    traceback.print_exc()

finally:
    # 確保在程式退出時串口被正確關閉
    instrument.serial.close()
    print('Closed')