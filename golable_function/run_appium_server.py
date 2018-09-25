# -*- coding: utf-8 -*-
# __author__ = 'gz'
import subprocess
from multiprocessing import Process
from golable_function.appium_set import AppiumConfig
from golable_function.config_function import config_writer, config_reader
import os
import time
import psutil

appium_config = AppiumConfig()
appium = appium_config.get_appium_set()
APPINUM_CONFIG = list(appium.values())
PATH = os.path.dirname(os.path.abspath(__file__))
appium_config_file_path = PATH + '/../temp/appium_config_file.yml'


def run_appium(ip, appium_port, adb_port):
    a = subprocess.Popen(
        'appium --session-override -a {} -p {} -bp {}--session-override --no-reset '.format(ip, appium_port,
                                                                                            adb_port),
        shell=True)
    a.wait()
    return a.pid


def works():
    proc_record = []
    if APPINUM_CONFIG == ['udid list is None']:
        config_writer(None, appium_config_file_path)
        return proc_record
    else:
        print(appium)
        for config in APPINUM_CONFIG:
            ip = config[0]
            appium_port = config[1]
            adb_port = config[2]
            cmd = 'appium --session-override -a {} -p {} -bp {}--session-override --no-reset '.format(ip, appium_port,
                                                                                                      adb_port)
            p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
            proc_record.append(p.pid)
        config_writer(appium, appium_config_file_path)
        time.sleep(10)
    return proc_record


if __name__ == '__main__':
    print(works())
    print(psutil.pids())
    # print(config_reader(appium_config_file_path))
    time.sleep(10)
    # print(os.fork())
    print(psutil.pids())
    # time.sleep(60)
