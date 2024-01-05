import minimalmodbus
import serial

# 配置串口
ser = serial.Serial(port='COM4', baudrate=9600, bytesize=8, parity='N', stopbits=1)

# 設定 Modbus RTU 連接
instrument = minimalmodbus.Instrument(ser, slaveaddress=1)


# 讀取保持寄存器的值
value = instrument.read_register(0, functioncode=3)  # 0是寄存器地址，3是功能碼

print("Read successful:", value)
