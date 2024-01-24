#zh-tw 你可以把讀取程式碼建立成類似下列這種嗎？
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
        register_address=int(input('Input Address: '))
        value_to_write=round(float(input('Input Value: ')),2)

        # # 使用write_register()方法寫入整數數據
        # instrument.write_register(registeraddress=register_address, value = value_to_write,
        #                           functioncode=6)

        try:
            time.sleep(0.5)

            # # 使用write_register()方法寫入整數數據
            # instrument.write_register(registeraddress=register_address, value = value_to_write,
            #                           functioncode=6)

            # 使用write_float()方法寫入浮點數數據
            instrument.write_float(register_address, value_to_write) #functioncode=6 or 16
            print(f"Writing Success，地址：{register_address}，數值：{value_to_write}")
            time.sleep(0.5)
        except minimalmodbus.NoResponseError as e:
            print(f"No response from the instrument: {e}")
            traceback.print_exc()

    
except KeyboardInterrupt:
    # 當使用者按下Ctrl+C時結束
    print('Exiting...')

except Exception as e:
    print(f"Exception: {e}")
    traceback.print_exc()

finally:
    instrument.serial.close()
    print('Closed')
