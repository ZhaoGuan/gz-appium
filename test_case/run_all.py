# -*- coding: utf-8 -*-
# __author__ = 'Gz'
from multiprocessing import Process
import threading
import shutil
import os
from golable_function.Golable_function import report
import time
# 错误后再次运行的引入
from golable_function.suite_rerun import Suit
from golable_function.HTMLTestRunner import HTMLTestRunner
from test_case.ikey.input import InputApp
from test_case.ikey.messenger import *
from test_case.ikey.whatsapp import *
import os

PATH = os.path.dirname(os.path.abspath(__file__))


def run_suite(duid):
    suite = Suit()
    suite.addTest(InputApp('theme', device=duid))
    suite.addTest(InputApp('theme_change', device=duid))
    suite.addTest(InputApp('download_theme', device=duid))
    suite.addTest(InputApp('emoji_style_change', device=duid))
    suite.addTest(InputApp('emoji_style_download', device=duid))
    suite.addTest(InputApp('download_font', device=duid))
    suite.addTest(InputApp('pop_key', device=duid))
    suite.addTest(InputApp('keyboard_layout', device=duid))
    suite.addTest(InputApp('new_language', device=duid))
    # ISOTIMEFORMAT = '%Y%m%d_%X'
    filename = '%s' % report('Report' + duid + '_')
    fp1 = open(filename, 'wb')
    runner = HTMLTestRunner(stream=fp1, title='自动化测试报告' + duid, description='自动化测试报告1')
    runner.run(suite)
    fp1.close()


def run_suite1():
    suite1 = Suit()
    suite1.addTest(InputApp('test', device='HT441SF04451'))
    suite1.addTest(InputApp('test', device='HT441SF04451'))
    suite1.addTest(InputApp('test', device='HT441SF04451'))
    suite1.addTest(InputApp('test', device='HT441SF04451'))
    # ISOTIMEFORMAT = '%Y%m%d_%X'
    filename = '%s' % report('Report1')
    fp1 = open(filename, 'wb')
    runner1 = HTMLTestRunner(stream=fp1, title='自动化测试报告1', description='自动化测试报告1')
    runner1.run(suite1)
    fp1.close()


def run_suite2():
    suite2 = Suit()
    suite2.addTest(InputApp('test', device='HT54DSV00048'))
    suite2.addTest(InputApp('test', device='HT54DSV00048'))
    suite2.addTest(InputApp('test', device='HT54DSV00048'))
    suite2.addTest(InputApp('test', device='HT54DSV00048'))
    # ISOTIMEFORMAT = '%Y%m%d_%X'
    filename = '%s' % report('Report2')
    fp2 = open(filename, 'wb')
    runner2 = HTMLTestRunner(stream=fp2, title='自动化测试报告3', description='自动化测试报告1')
    runner2.run(suite2)
    fp2.close()


def run_suite3():
    suite3 = Suit()
    suite3.addTest(InputApp('test', device='5203adddfc7334c1'))
    suite3.addTest(InputApp('test', device='5203adddfc7334c1'))
    suite3.addTest(InputApp('test', device='5203adddfc7334c1'))
    suite3.addTest(InputApp('test', device='5203adddfc7334c1'))
    # ISOTIMEFORMAT = '%Y%m%d_%X'
    filename = '%s' % report('Report3')
    fp3 = open(filename, 'wb')
    runner3 = HTMLTestRunner(stream=fp3, title='自动化测试报告3', description='自动化测试报告1')
    runner3.run(suite3)
    fp3.close()


def work_Process():
    proc_record = []
    for i in appium_config.get_device_udid():
        print(i)
        th = Process(target=run_suite, args=(i,))
        th.start()
        proc_record.append(th)
    for e in proc_record:
        e.join()
        # p1 = Process(target=run_suite1)
        # p2 = Process(target=run_suite2)
        # p3 = Process(target=run_suite3)
        # p1.start()
        # p2.start()
        # p3.start()
        # p1.join()
        # p2.join()
        # p3.join()
    # 删除文件夹
    shutil.rmtree(PATH + '/../temp')
    shutil.rmtree(PATH + '/../fail_picture')
    # 创建文件夹
    os.makedirs(PATH + '/../temp')
    os.makedirs(PATH + '/../fail_picture')


def work_thread():
    for i in appium_config.get_device_udid():
        th = threading.Thread(target=run_suite, group=i)
        th.start()
        th.join()
        # t1 = threading.Thread(target=run_suite1)
        # t2 = threading.Thread(target=run_suite2)
        # t3 = threading.Thread(target=run_suite3)
        # t1.start()
        # t2.start()
        # t3.start()
        # t1.join()
        # t2.join()
        # t3.join()


if __name__ == "__main__":
    work_Process()
    # work_thread()
