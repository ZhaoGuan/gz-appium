# -*- coding: utf-8 -*-
# __author__ = 'Gz'
import socket
import os
import signal
import subprocess
import psutil
import time
from golable_function.config_function import config_writer, config_reader

PATH = os.path.dirname(os.path.abspath(__file__))
planned_devices_data_path = PATH + '/../temp/PlannedDevicesData.yml'
running_appium_service_path = PATH + '/../temp/RunningAppiumService.yml'


class AppiumService:
    def __init__(self):
        self.server_ip = '127.0.0.1'
        self.begin_p = 4700
        self.begin_bp = 4800

    def check_p_port(self, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((self.server_ip, int(port)))
        sock.close()
        if result == 0:
            return True
        else:
            return False

    def provide_port(self):
        p = self.begin_p
        bp = self.begin_bp
        while True:
            if self.check_p_port(p):
                break
            else:
                p += 1
                bp += 1
        return {'p': p, 'bp': bp}

    def get_devices(self):
        cmd_result = os.popen("adb devices").read()
        b = (cmd_result.split("\n"))[1:-2]
        devices = []
        for i in b:
            devices.append(i.split("\t")[0])
        return devices

    def device_to_p_bp(self):
        result = {}
        devices = self.get_devices()
        for device in devices:
            device_result = self.provide_port()
            result.update({device: device_result})
        return result

    def record_devices(self):
        devices_data = self.device_to_p_bp()
        try:
            config_writer(devices_data, planned_devices_data_path)
            return True
        except Exception as E:
            print(E)
            return False

    def run_appiun_service(self, p, bp, wait_time=10):
        while True:
            if self.check_p_port(p):
                p += 1
                bp += 1
            else:
                break
        cmd = 'appium --session-override -a {} -p {} -bp {}--session-override --no-reset '.format(self.server_ip, p, bp)
        process = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        pid = process.pid
        time.sleep(wait_time)
        return {'p': p, 'bp': bp, 'pid': pid}

    def run_device_appium_sever(self, device):
        planned_device_data = config_reader(planned_devices_data_path)
        running_appium_service = config_reader(running_appium_service_path)
        if device not in str(running_appium_service):
            try:
                data = planned_device_data[device]
                p = data['p']
                bp = data['bp']
                run_result = self.run_appiun_service(p, bp)
                if running_appium_service != None:
                    running_appium_service.update({device: run_result})
                else:
                    running_appium_service = {device: run_result}
                config_writer(running_appium_service, running_appium_service_path)
                return {'result': True, 'msg': 'ok'}
            except Exception as E:
                print(E)
                return {'result': False, 'msg': E}
        else:
            msg = device + '已经启动'
            return {'result': False, 'msg': msg}

    def process_kill(self, device):
        running_appium_service = config_reader(running_appium_service_path)
        pid = running_appium_service[device]['pid']
        try:
            os.kill(pid, signal.SIGKILL)
            running_appium_service.pop(device)
            config_writer(running_appium_service, running_appium_service_path)
            return {'result': True, 'msg': 'ok'}
        except Exception as E:
            print(E)
            return {'result': False, 'msg': E}
