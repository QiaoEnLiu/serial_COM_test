import sys
import socket
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import QTimer

class NetworkInfo(QWidget):
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
    def initUI(self):
        self.status_label = QLabel('網路狀態：未知')
        self.hostname_label = QLabel('主機名稱：未知')
        self.ip_label = QLabel('IP地址：未知')
        self.netmask_label = QLabel('子網路遮罩：未知')
        self.gateway_label = QLabel('預設閘道：未知')
        
        layout = QVBoxLayout()
        layout.addWidget(self.status_label)
        layout.addWidget(self.hostname_label)
        layout.addWidget(self.ip_label)
        layout.addWidget(self.netmask_label)
        layout.addWidget(self.gateway_label)
        
        self.setLayout(layout)
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateNetworkStatus)
        self.timer.start(1000)  # 每1秒更新一次
        
        self.setWindowTitle('網路資訊')
        self.show()
        
    def get_network_info_linux(self, interface):
        try:
            ip = subprocess.getoutput(f"ip addr show {interface} | grep 'inet ' | awk '{{print $2}}'")
            netmask = subprocess.getoutput(f"ip addr show {interface} | grep 'inet ' | awk '{{print $4}}'")
            gateway = subprocess.getoutput("ip route | grep default | awk '{print $3}'")
            
            self.ip_label.setText(f'IP地址：{ip}')
            self.netmask_label.setText(f'子網路遮罩：{netmask}')
            self.gateway_label.setText(f'預設閘道：{gateway}')
            
        except Exception as e:
            print(f"Error getting network info: {e}")
            
    def get_network_info_windows(self):
        try:
            hostname = socket.gethostname()
            ip = socket.gethostbyname(hostname)
            
            self.hostname_label.setText(f'主機名稱：{hostname}')
            self.ip_label.setText(f'IP地址：{ip}')
            self.netmask_label.setText('子網路遮罩：未知')
            self.gateway_label.setText('預設閘道：未知')
            
        except Exception as e:
            print(f"Error getting network info: {e}")
            
    def updateNetworkStatus(self):
        if sys.platform.startswith('linux'):
            wired_status = subprocess.getoutput("cat /sys/class/net/eth0/carrier")
            wireless_status = subprocess.getoutput("cat /sys/class/net/wlan0/carrier")
            
            if wired_status == '1':
                self.status_label.setText('網路狀態：有線')
                self.get_network_info_linux('eth0')
            elif wireless_status == '1':
                self.status_label.setText('網路狀態：無線')
                self.get_network_info_linux('wlan0')
            else:
                self.status_label.setText('網路狀態：未連接')
                self.ip_label.setText('IP地址：未知')
                self.netmask_label.setText('子網路遮罩：未知')
                self.gateway_label.setText('預設閘道：未知')
                
        elif sys.platform.startswith('win32'):
            try:
                socket.create_connection(("www.google.com", 80))
                self.status_label.setText('網路狀態：有線')
                self.get_network_info_windows()
            except OSError:
                self.status_label.setText('網路狀態：無線')
                self.get_network_info_windows()
                
        else:
            self.status_label.setText('不支援此作業系統')
            self.hostname_label.setText('主機名稱：未知')
            self.ip_label.setText('IP地址：未知')
            self.netmask_label.setText('子網路遮罩：未知')
            self.gateway_label.setText('預設閘道：未知')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = NetworkInfo()
    sys.exit(app.exec_())
