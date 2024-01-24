#zh-tw
import minimalmodbus, traceback, time

address=[0,2,4,6]

try:
    # 定義Modbus裝置的串口及地址
    instrument = minimalmodbus.Instrument('COM4', 1)  
    # 第一個參數是串口，第二個參數是Modbus地址

    # 設定串口波特率，Parity和Stop bits（這些參數需與Modbus設備一致）
    instrument.serial.baudrate = 9600
    instrument.serial.parity = minimalmodbus.serial.PARITY_NONE
    instrument.serial.stopbits = 1

    while True:
        time.sleep(0.5)
        try:
            
            for i in address:
                value_read_float = instrument.read_float(i)
                print(f'Slaver Address {i}:',round(value_read_float,2))

        except minimalmodbus.NoResponseError as e:
            print(f"No response from the instrument: {e}")
            traceback.print_exc()
                
        register_address=int(input('Input Address: '))
        value_to_write=round(float(input('Input Value: ')),2)


        try:
            time.sleep(0.5)

            instrument.write_float(register_address, value_to_write)
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
