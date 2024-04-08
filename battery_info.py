import platform
import psutil
import wmi

def showBatteryInfo():
    system = platform.system()

    if system == "Linux":
        battery = psutil.sensors_battery()
        if battery:
            plugged = battery.power_plugged
            percent = battery.percent
            if not plugged:
                return f"電池未充電，目前電量: {percent}%"
            else:
                return "電源供應中，未使用電池"
        else:
            return "未找到電池資訊"

    elif system == "Windows":
        c = wmi.WMI()
        battery_info = c.Win32_Battery()
        # print(battery_info[0])
        if battery_info:
            battery_status = int(battery_info[0].BatteryStatus)
            # print(f"Debug: BatteryStatus = {battery_status}")  # 除錯信息

            status = ""
            remaining = battery_info[0].EstimatedChargeRemaining

            if battery_status == 1:
                status = "電池未接通"
                
            elif battery_status == 2:
                status = "電池已接通"
                
            elif battery_status == 3:
                status = "電池充電中"

            return [status, remaining, battery_info[0]]
            # return f"{status}, 電量: {remaining}%\n\r{battery_info[0]}"

        else:
            return "未找到電池資訊"