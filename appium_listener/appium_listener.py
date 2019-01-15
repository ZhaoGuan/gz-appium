# -*- coding: utf-8 -*-
# __author__ = 'Gz'
import yaml
from golable_function.appium_set import AppiumConfig
import os
import time

PATH = os.path.dirname(os.path.abspath(__file__))


def configer_reader(yaml_file):
    yf = open(yaml_file)
    yx = yaml.load(yf)
    yf.close()
    return yx


def write_duid():
    AC = AppiumConfig()
    duid = AC.get_device_udid()
    duid_number = len(duid)
    with open(PATH + '/duid.yml', 'w') as w_duid:
        yaml.dump(duid_number, w_duid)
        # w_duid.write({'duid_number': t})


def restart_appium_server():
    write_duid()
    AC = AppiumConfig()
    duid = AC.get_device_udid()
    duid_number = len(duid)
    last_duid_number = configer_reader(PATH + '/duid.yml')
    if duid_number != last_duid_number:
        os.popen('ps -ef | grep "run_appium_server.py" | grep -v grep | cut -c 9-15 | xargs kill -s 9')
        os.popen('python3 run_appium_server.py')


def appium_linster():
    write_duid()
    while True:
        time.sleep(10)
        restart_appium_server()


if __name__ == '__main__':
    print(configer_reader(PATH + '/duid.yml'))
