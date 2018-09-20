# -*- coding: utf-8 -*-
# __author__ = 'Gz'
import os

# from report_reader_server import report_reader
# from appium_linster import appium_listener_run
# from run_appium_server import appium_run

PATH = os.path.dirname(os.path.abspath(__file__))
# os.chdir(PATH)
print(PATH)
os.popen('ps -ef | grep "python3 -m http.server 8000" | grep -v grep | cut -c 9-15 | xargs kill -s 9')
os.popen('ps -ef | grep "appium" | grep -v grep | cut -c 9-15 | xargs kill -s 9')
os.popen('python3 '+PATH+'/run_appium_server.py')
print('server')
os.popen('ps -ef | grep "appium_linster.py" | grep -v grep | cut -c 9-15 | xargs kill -s 9')
os.popen('python3 '+PATH+'/appium_linster.py')
print('linster')
os.popen('python3 '+PATH+'/report_reader_server.py')
print('report reader')
