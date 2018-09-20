# -*- coding: utf-8 -*-
# __author__ = 'Gz'
from golable_function.run_appium_server import works
import daemon
import os


def appium_run():
    with daemon.DaemonContext():
        works()


if __name__ == '__main__':
    appium_run()
