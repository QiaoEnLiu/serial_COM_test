#zh-tw 

import minimalmodbus

# 定義Modbus裝置的串口及地址
instrument = minimalmodbus.Instrument('COM4', 0, mode='rtu')  # 第一個參數是串口，第二個參數是Modbus地址

# 設定串口波特率，Parity和Stop bits（這些參數需與Modbus設備一致）
instrument.serial.baudrate = 9600
instrument.serial.parity = minimalmodbus.serial.PARITY_NONE
instrument.serial.stopbits = 1

# 讀取保持寄存器（holding register）中的數據，地址為1
register_address = 3

# 逐個設備進行讀取
for device_address in range(0, 248):  # Modbus 地址通常在 1 到 247 之間
    try:
        value_read = instrument.read_register(register_address, functioncode=4)
        print(f"成功讀取設備 {device_address} 的數據：{value_read}")
    except Exception as e:
        print(f"讀取設備 {device_address} 時發生錯誤：{e}")
