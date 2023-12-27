#zh-tw 現在這個是寫入的程式碼，請把他改成讀取

import minimalmodbus

# 定義Modbus裝置的串口及地址
instrument = minimalmodbus.Instrument('COM4', 0)  # 第一個參數是串口，第二個參數是Modbus地址

# 設定串口波特率，Parity和Stop bits（這些參數需與Modbus設備一致）
instrument.serial.baudrate = 9600
instrument.serial.parity = minimalmodbus.serial.PARITY_NONE
instrument.serial.stopbits = 1

# 寫入保持寄存器（holding register）中的數據，地址為40001
register_address = 1
value_to_write = 1

# 使用write_register()方法寫入數據
instrument.write_register(register_address, value_to_write, functioncode=16)

print(f"寫入數據成功，地址：{register_address}，數值：{value_to_write}")
