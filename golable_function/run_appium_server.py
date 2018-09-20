# -*- coding: utf-8 -*-
# __author__ = 'gz'
import subprocess
from multiprocessing import Process
from golable_function.appium_set import AppiumConfig

appium_config = AppiumConfig()
appium = appium_config.get_appium_set()
APPINUM_CONFIG = appium.values()


def run_appium(ip, appium_port, adb_port):
    a = subprocess.Popen(
        'appium --session-override -a {} -p {} -bp {}--session-override --no-reset '.format(ip, appium_port,
                                                                                            adb_port),
        shell=True)
    a.wait()


def works():
    proc_record = []
    for config in APPINUM_CONFIG:
        print(config)
        # p = Process(target=run_appium, args=(config[0],config[1], config[2]))
        p = Process(target=run_appium, args=config)
        p.start()
        proc_record.append(p)
    for p in proc_record:
        p.join()


if __name__ == '__main__':
    works()