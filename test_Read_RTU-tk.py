#zh-tw

import serial
import modbus_tk
import modbus_tk.defines as cst
from modbus_tk import modbus_rtu

# 創建Modbus RTU連接
master = modbus_rtu.RtuMaster(serial.Serial(port='COM4', baudrate=9600, bytesize=8, parity='N', stopbits=1))

# 開啟連接
master.open()

# 讀取保持寄存器的值
result = master.execute(2, cst.READ_HOLDING_REGISTERS, 0, 5)  # 1是從站地址，0是寄存器地址，1是要讀取的寄存器數量

print("Read successful:", result)

# 關閉連接
master.close()
