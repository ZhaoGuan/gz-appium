# -*- coding: utf-8 -*-
# __author__ = 'Gz'


import os
import time
import unittest
import requests
from appium import webdriver
from golable_function.HTMLTestRunner import HTMLTestRunner
from golable_function.appium_set import AppiumConfig
from golable_function.extend import AppiumExtend
from golable_function.basefunction import BaseFunction
from appium.webdriver.common.touch_action import TouchAction
from golable_function.Golable_function import report
from golable_function.image_recognition import ocr_text

appium_config = AppiumConfig()
udid = appium_config.get_device_udid()
appium = appium_config.get_appium_set()
DEVICE_CONFIG = udid[0]


# APPIUM_CONFIG = appium[0]


# 因为使用Messenger为载体所以其中选择发送对象需要根据运行的手机做配置
# 脚本维护的时候也要将messenger对应环境准备好(各种权限的允许)
class InputApp(unittest.TestCase):
    def __init__(self, method_name='runTest', device=DEVICE_CONFIG):
        unittest.TestCase.__init__(self, method_name)
        self.device = device
        # self.device = "84B5T15A09001724"
        self.APPIUM_CONFIG = appium_config.get_appium_set()[self.device]

    def setUp(self):
        print('Test start')
        desired_caps = {}
        desired_caps['automationName'] = "appium"  # Appium,UiAutomator2,XCUITest,YouiEngine
        desired_caps['platformName'] = 'Android'
        desired_caps['deviceName'] = self.device
        desired_caps['udid'] = self.device
        # 超时时间设置
        desired_caps['newCommandTimeout'] = 180
        # 要启动的应用
        desired_caps['appPackage'] = 'com.nut.inc.meme'
        desired_caps['appActivity'] = '.view.activity.SplashActivity'
        # desired_caps['appPackage'] = 'com.tencent.mm'
        # desired_caps['appActivity'] = '.ui.LauncherUI'
        # 隐藏键盘
        # desired_caps['resetKeyboard'] = 'True'
        # 使用appium键盘
        # desired_caps['unicodeKeyboard'] = 'True'
        # 不重置应用状态
        desired_caps["noReset"] = True
        # 密码解锁
        desired_caps["unlockType"] = "password"
        desired_caps["unlockKey"] = "0000"

        # self.d = webdriver.Remote('http://%s:%s/wd/hub' % (self.APPIUM_CONFIG[0], self.APPIUM_CONFIG[1]), desired_caps)
        self.d = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
        self.d.unlock()
        self.extend = AppiumExtend(self.d)
        self.BF = BaseFunction(self, self.d)
        self.d.get_window_size()
        time.sleep(5)

    def test(self):
        self.BF.random_click("id", "com.nut.inc.meme:id/image", "click", "id",
                             "com.nut.inc.meme:id/button_meme_it")
        time.sleep(10)

    def tearDown(self):
        print('Test end')
        self.d.quit()


if __name__ == "__main__":
    # 编辑用例
    # suite = Suit()
    suite = unittest.TestSuite()
    suite.addTest(InputApp("test", '84B5T15A09001724'))
    # 执行用例
    runner = unittest.TextTestRunner()
    # filename = '%s' % report('gz')
    # fp = open(filename, 'wb')
    # runner = HTMLTestRunner(stream=fp, title='自动化测试报告', description='自动化测试报告')
    runner.run(suite)
