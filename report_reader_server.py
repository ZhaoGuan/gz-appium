# -*- coding: utf-8 -*-
# __author__ = 'Gz'
import os
import daemon
import http.server

PATH = os.path.dirname(os.path.abspath(__file__))
os.chdir(PATH + '/Report')


def report_reader():
    os.popen('python3 -m http.server 8000')


if __name__ == '__main__':
    report_reader()
