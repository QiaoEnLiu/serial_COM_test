#zh-tw
import minimalmodbus, traceback

try:
    # 定義Modbus裝置的串口及地址
    instrument = minimalmodbus.Instrument('COM4', 0)  # 第一個參數是串口，第二個參數是Modbus地址

    # 設定串口波特率，Parity和Stop bits（這些參數需與Modbus設備一致）
    instrument.serial.baudrate = 9600
    instrument.serial.parity = minimalmodbus.serial.PARITY_NONE
    instrument.serial.stopbits = 1

    while True:

        # 寫入保持寄存器（holding register）中的數據，地址為40001
        # register_address=int(input('Input Address: '))
        register_address=2
        value_to_write=int(input('Input Value: '))
        # 使用write_register()方法寫入數據
        instrument.write_register(registeraddress=register_address, value=value_to_write, functioncode=6)

        print(f"Writing Success，地址：{register_address}，數值：{value_to_write}")
    
except KeyboardInterrupt:
    # 當使用者按下Ctrl+C時結束
    print('Exiting...')

except Exception as e:
    print(f"Exception: {e}")
    traceback.print_exc()

finally:
    print('Closed')
