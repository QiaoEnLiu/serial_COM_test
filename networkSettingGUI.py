import sys
import netifaces
import subprocess
import platform
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QPushButton, QMessageBox
from PyQt5.QtCore import QTimer

class NetworkConfig(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('網路設定')

        # 左側網絡接口信息
        self.network_info_label = QLabel('網絡接口信息：')
        self.network_info_text = QLabel(self.get_network_interfaces())

        left_layout = QVBoxLayout()
        left_layout.addWidget(self.network_info_label)
        left_layout.addWidget(self.network_info_text)

        # 右側輸入框、按鈕和自動取得按鈕
        self.ipv4_label = QLabel('IPv4:')
        self.ipv4_edit = QLineEdit()

        self.subnet_label = QLabel('子網路遮罩:')
        self.subnet_edit = QLineEdit()

        self.gateway_label = QLabel('預設閘道:')
        self.gateway_edit = QLineEdit()

        self.hostname_label = QLabel('主機名稱:')
        self.hostname_edit = QLineEdit()

        self.save_button = QPushButton('儲存設定')
        self.save_button.clicked.connect(self.save_config)

        self.auto_button = QPushButton('自動取得')
        self.auto_button.clicked.connect(self.set_auto_config)

        self.result_label = QLabel('')
        self.update_connection_status()

        right_layout = QVBoxLayout()
        right_layout.addWidget(self.ipv4_label)
        right_layout.addWidget(self.ipv4_edit)
        right_layout.addWidget(self.subnet_label)
        right_layout.addWidget(self.subnet_edit)
        right_layout.addWidget(self.gateway_label)
        right_layout.addWidget(self.gateway_edit)
        right_layout.addWidget(self.hostname_label)
        right_layout.addWidget(self.hostname_edit)
        right_layout.addWidget(self.save_button)
        right_layout.addWidget(self.auto_button)
        right_layout.addWidget(self.result_label)

        # 主布局
        main_layout = QHBoxLayout()
        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)

        self.setLayout(main_layout)

    def update_connection_status(self):
        if platform.system() == 'Windows':
            connected_status = self.check_windows_connection()
        elif platform.system() == 'Linux':
            connected_status = self.check_linux_connection()
        else:
            connected_status = '不支援的操作系統'

        self.result_label.setText(connected_status)

    def check_windows_connection(self):
        try:
            output = subprocess.check_output('ping 8.8.8.8 -n 1', shell=True)
            # print(output)
            decoded_output = output.decode('utf-8')
            
            if "Reply from 8.8.8.8:" in decoded_output:
                return '已連線'
            else:
                return '未連線'
        except subprocess.CalledProcessError:
            return '未連線'

    def check_linux_connection(self):
        try:
            output = subprocess.check_output('ping -c 1 8.8.8.8', shell=True)
            if b"bytes from" in output:
                return '已連線'
            else:
                return '未連線'
        except subprocess.CalledProcessError:
            return '未連線'

    def get_network_interfaces(self):
        interfaces_info = ''
        interfaces = netifaces.interfaces()
        for interface in interfaces:
            interfaces_info += f'Interface: {interface}\n'
            
            addresses = netifaces.ifaddresses(interface)
            
            try:
                ipv4_address = addresses[netifaces.AF_INET][0]['addr']
                interfaces_info += f'  IPv4 Address: {ipv4_address}\n'
            except KeyError:
                interfaces_info += '  No IPv4 address\n'

            try:
                mac_address = addresses[netifaces.AF_LINK][0]['addr']
                interfaces_info += f'  MAC Address: {mac_address}\n'
            except KeyError:
                interfaces_info += '  No MAC address\n'

            try:
                netmask = addresses[netifaces.AF_INET][0]['netmask']
                interfaces_info += f'  Subnet Mask: {netmask}\n'
            except KeyError:
                interfaces_info += '  No subnet mask\n'

            interfaces_info += '-' * 40 + '\n'

        return interfaces_info

    def save_config(self):
        self.result_label.setText('連線中...')
        self.save_button.setEnabled(False)
        self.auto_button.setEnabled(False)

        QTimer.singleShot(2000, self.apply_save_config)

    def apply_save_config(self):
        ipv4 = self.ipv4_edit.text()
        subnet = self.subnet_edit.text()
        gateway = self.gateway_edit.text()
        hostname = self.hostname_edit.text()

        if platform.system() == 'Windows':
            result = self.set_network_config_windows(ipv4, subnet, gateway, hostname)
            connected_status = '已連線' if '成功' in result else '未連線'
        elif platform.system() == 'Linux':
            result = self.set_network_config_linux(ipv4, subnet, gateway, hostname)
            connected_status = '已連線' if '設定成功' in result else '未連線'
        else:
            result = '不支援的操作系統'
            connected_status = '未知'

        self.result_label.setText(f'{result} ({connected_status})')
        self.save_button.setEnabled(True)
        self.auto_button.setEnabled(True)

    def set_auto_config(self):
        self.result_label.setText('連線中...')
        self.save_button.setEnabled(False)
        self.auto_button.setEnabled(False)

        QTimer.singleShot(2000, self.apply_set_auto_config)

    def apply_set_auto_config(self):
        if platform.system() == 'Windows':
            command = 'netsh interface ip set address name="乙太網路" source=dhcp'
            subprocess.run(command, shell=True)
            self.result_label.setText('已切換為自動取得 IP (已連線)')
        elif platform.system() == 'Linux':
            command = 'sudo dhclient eth0'
            subprocess.run(command, shell=True)
            self.result_label.setText('已切換為自動取得 IP (已連線)')
        else:
            self.result_label.setText('不支援的操作系統')

        self.save_button.setEnabled(True)
        self.auto_button.setEnabled(True)

    def set_network_config_windows(self, ipv4, subnet, gateway, hostname):
        command = f"netsh interface ip set address name='乙太網路' static {ipv4} {subnet} {gateway}"
        hostname_command = f"net config server /srvcomment:\"{hostname}\""
        
        try:
            subprocess.run(command, check=True, shell=True)
            subprocess.run(hostname_command, check=True, shell=True)
            return '設定成功'
        except subprocess.CalledProcessError as e:
            return f'設定失敗：{e}'

    def set_network_config_linux(self, ipv4, subnet, gateway, hostname):
        try:

            # 設定IP地址和子網遮罩
            command = f"sudo ifconfig eth0 {ipv4} netmask {subnet}"
            subprocess.run(command, check=True, shell=True)
            
            # 檢查網關地址是否可達
            gateway_check_command = f"ping -c 1 -W 2 {gateway}"
            subprocess.run(gateway_check_command, check=True, shell=True)
            
            # 設定預設閘道
            gateway_command = f"sudo route add default gw {gateway}"
            subprocess.run(gateway_command, check=True, shell=True)
            
            # 設定有線網路主機名稱
            hostname_command = f"sudo hostname {hostname}"
            subprocess.run(hostname_command, check=True, shell=True)
            
            # 更新 /etc/hosts 檔案
            hosts_command = f"echo '127.0.1.1\t{hostname}' | sudo tee -a /etc/hosts"
            subprocess.run(hosts_command, check=True, shell=True)
            
            # 更新 /etc/hostname 檔案
            hostname_file_command = f"echo {hostname} | sudo tee /etc/hostname"
            subprocess.run(hostname_file_command, check=True, shell=True)

            
            return '設定成功'
        except subprocess.CalledProcessError as e:
            return f'設定失敗：{e}'
    # # 切換回DHCP模式
            # dhcp_command = "sudo dhclient -r eth0 && sudo dhclient eth0"
            # subprocess.run(dhcp_command, check=True, shell=True)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = NetworkConfig()
    window.show()
    sys.exit(app.exec_())
