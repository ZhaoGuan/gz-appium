# -*- coding: utf-8 -*-
# __author__ = 'Gz'
from appium_listener.appium_listener import *
import daemon


def appium_listener_run():
    with daemon.DaemonContext():
        appium_linster()


if __name__ == '__main__':
    appium_listener_run()
